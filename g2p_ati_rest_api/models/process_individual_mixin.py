from odoo import models

class ProcessIndividualMixin(models.AbstractModel):
    _inherit = "process_individual.rest.mixin"

    def _process_individual(self, individual):
        res = super()._process_individual(individual)
        if individual.model_dump().get("gf_name_eng", None):
            res["gf_name_eng"] = individual.gf_name_eng
        return res