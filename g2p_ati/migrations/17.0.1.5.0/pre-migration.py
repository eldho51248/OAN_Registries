import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    if version == "17.0.1.3.0":
        env["ir.model.data"].search(
            [("model", "in", ("g2p.region", "g2p.zone", "g2p.woreda")), ("module", "=", "g2p_ati")]
        ).write({"noupdate": False})
