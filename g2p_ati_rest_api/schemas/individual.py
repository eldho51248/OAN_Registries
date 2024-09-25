from odoo.addons.g2p_registry_rest_api.schemas import individual


class UpdateIndividualInfoRequest(
    individual.UpdateIndividualInfoRequest, extends=individual.UpdateIndividualInfoRequest
):
    gf_name_eng: str | None
    given_name_am: str | None
    family_name_am: str | None
    addl_name_am: str | None


class UpdateIndividualInfoResponse(
    individual.UpdateIndividualInfoResponse, extends=individual.UpdateIndividualInfoResponse
):
    gf_name_eng: str | None = None
    given_name_am: str | None = None
    family_name_am: str | None = None
    addl_name_am: str | None = None
