import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info("Starting pre-migration for version 17.0-1.5.0")
