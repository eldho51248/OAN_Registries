import asyncio
import aiomysql
import asyncpg
import sqlite3
import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from datetime import datetime

# Logging setup
log_queue = Queue()
queue_handler = QueueHandler(log_queue)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
_logger.addHandler(queue_handler)
file_handler = logging.FileHandler('import.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
listener = QueueListener(log_queue, file_handler)
listener.start()

# Database Configurations
DATABASES = [
    {
        'name': "8028",
        'type': 'mysql',
        'host': '10.1.10.203',
        'port': 3306,
        'user': 'root',
        'password': 'ata@12345',
        'database': 'ATAIVRDB',
        'query': """
            SELECT id, phoneNum, callTime 
            FROM tblCaller 
            WHERE phoneNum IS NOT NULL AND phoneNum != ''
        """,
        "phone_field": "phoneNum"
    },

    {
        'name': "NMIS",
        'type': 'mysql',
        'host': '10.1.10.201',
        'port': 3306,
        'user': 'root',
        'password': 'nmis@12345',
        'database': 'NMISDB',
        'query': """
            SELECT id, phoneNum, callTime 
            FROM tblCaller 
            WHERE phoneNum IS NOT NULL AND phoneNum != ''
        """,
        "phone_field": "phoneNum"
    },
]

DESTINATION_DB = {
    'name': "ati",
    'host': 'localhost',
    'port': 5432,
    'user': 'teddy',
    'password': 'odoo',
    'database': 'ati'
}

INTERMEDIATE_DB = {
    'name': "ati_imports",
    'host': 'localhost',
    'port': 5432,
    'user': 'teddy',
    'password': 'odoo',
    'database': 'ati_imports'
}

SYNC_DB_PATH = "sync.db"


async def fetch_or_initialize_last_sync_time():
    conn = sqlite3.connect(SYNC_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_sync_time TIMESTAMP NOT NULL)""")

    cursor.execute("SELECT last_sync_time FROM sync_metadata ORDER BY last_sync_time DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        last_sync_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
    else:
        last_sync_time = datetime(1970, 1, 1).strftime("%Y-%m-%d %H:%M:%S")

    conn.close()
    return last_sync_time


async def get_connection_pool_mysql(db_config):
    return await aiomysql.create_pool(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['database'],
        minsize=1,
        maxsize=10
    )


async def get_connection_pool_pg(db_config):
    return await asyncpg.create_pool(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        min_size=1,
        max_size=10
    )


async def fetch_data_from_mysql(pool, db_config, last_sync_time):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = f"{db_config['query']}"
            await cursor.execute(query)
            records = await cursor.fetchall()
    return records


async def store_in_intermediate_db(pool, table_name, records, phone_field):
    async with pool.acquire() as conn:
        async with conn.transaction():
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    phone VARCHAR(50) UNIQUE,
                    create_date TIMESTAMP DEFAULT NOW(),
                    match VARCHAR(10) DEFAULT 'not_found'
                )
            """
            await conn.execute(create_table_query)

            insert_query = f"""
                INSERT INTO {table_name} (phone)
                VALUES ($1)
                ON CONFLICT (phone) DO NOTHING
            """
            await conn.executemany(
                insert_query, 
                [(rec[phone_field],) for rec in records]
            )
            _logger.info(f"Stored {len(records)} records in intermediate table {table_name}")


async def sync_databases():
    last_sync_time = "2020-12-10 00:00:00"
    _logger.info(f"Last sync time: {last_sync_time}")

    mysql_pools = [await get_connection_pool_mysql(db) for db in DATABASES]
    pg_intermediate_pool = await get_connection_pool_pg(INTERMEDIATE_DB)
    pg_destination_pool = await get_connection_pool_pg(DESTINATION_DB)

    try:
        all_records = []
        for db_config, pool in zip(DATABASES, mysql_pools):
            records = await fetch_data_from_mysql(pool, db_config, last_sync_time)
            all_records.extend(records)
            await store_in_intermediate_db(pg_intermediate_pool, db_config['database'], records, db_config['phone_field'])

        _logger.info(f"Total records fetched and stored in intermediate DB: {len(all_records)}")

        async with pg_intermediate_pool.acquire() as conn:
            common_query = """
                SELECT 
                NMISDB.phone AS phone,
                evoucher.first_name AS first_name,
                evoucher.fathers_name AS fathers_name,
                evoucher.last_name AS last_name,
                evoucher.region AS gender,
                evoucher.gender AS region
                    FROM NMISDB
                INNER JOIN ATAIVRDB ON NMISDB.phone = ATAIVRDB.phone
                INNER JOIN evoucher ON NMISDB.phone = evoucher.phone

            """
            common_records = await conn.fetch(common_query)

            _logger.info(f"Common records found: {len(common_records)}")

            common_phones = list(set(rec['phone'] for rec in common_records))

            # Update match column in all intermediate tables
            update_query = "UPDATE NMISDB SET match = 'found' WHERE phone = ANY($1)"
            update_8028_query = "UPDATE ATAIVRDB SET match = 'found' WHERE phone = ANY($1)"
            update_evoucher_query = "UPDATE evoucher SET match = 'found' WHERE phone = ANY($1)"

            await conn.execute(update_query, (common_phones,))
            await conn.execute(update_8028_query, (common_phones,))
            await conn.execute(update_evoucher_query, (common_phones,))

        async with pg_destination_pool.acquire() as conn:
            async with conn.transaction():
                insert_query = """
                    INSERT INTO g2p_imported_record (
                            phone, state, given_name, family_name, gf_name_eng,gender,region
                        ) 
                        VALUES ($1, $2, $3, $4, $5, $6, $7);
                """
                insert_data = [(record.get('phone'),
                                'draft',
                                record.get('first_name'),
                                record.get('fathers_name'),
                                record.get('last_name'),
                                record.get('region'),
                                record.get('gender')
                                ) for record in common_records]
                await conn.executemany(insert_query, insert_data)

        _logger.info(f"Total records inserted into destination DB: {len(common_records)}")

    finally:
        for pool in mysql_pools:
            pool.close()
            await pool.wait_closed()
        await pg_intermediate_pool.close()
        await pg_destination_pool.close()


if __name__ == "__main__":
    asyncio.run(sync_databases())
