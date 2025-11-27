from odoo import api, fields, models, _


class G2PFarmerAPIRequest(models.Model):
    _name = "g2p.farmer.api.request"
    _description = "Farmer Search API Request"
    _order = "create_date desc"  # uses built-in create_date

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store=True,
    )
    bg_request_id = fields.Char(
        string="Background Request ID",
        index=True,
    )
    correlation_id = fields.Char(
        string="Correlation ID",
        index=True,
    )

    batch_ids = fields.One2many(
        "g2p.farmer.api.batch",
        "request_id",
        string="Batches",
    )

    process_status = fields.Char(
        string="Process Status",
        default="PENDING",
    )
    response_status_code = fields.Integer(string="Response HTTP Status")
    attempt_count = fields.Integer(string="Attempt Count", default=0)
    processed_by = fields.Char(string="Processed By")
    error_message = fields.Text(string="Error Message")
    completed_at = fields.Datetime(string="Completed At")

    request_data = fields.Json(
        string="Request Payload",
        required=True,
    )
    response_data = fields.Json(
        string="Response Payload",
    )

    @api.depends("correlation_id", "bg_request_id")
    def _compute_name(self):
        for rec in self:
            if rec.correlation_id:
                rec.name = _("Req %(corr)s", corr=rec.correlation_id)
            elif rec.bg_request_id:
                rec.name = _("Req %(bg)s", bg=rec.bg_request_id)
            else:
                rec.name = _("Farmer API Request #%s") % rec.id


class G2PFarmerAPIBatch(models.Model):
    _name = "g2p.farmer.api.batch"
    _description = "Farmer Search API Batch"
    _order = "create_date desc, batch_number asc"  # use create_date, not created_at

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store=True,
    )

    request_id = fields.Many2one(
        "g2p.farmer.api.request",
        string="API Request",
        required=True,
        index=True,
        ondelete="cascade",
    )

    batch_number = fields.Integer(string="Batch Number", required=True)
    offset = fields.Integer(string="Offset", required=True)
    limit = fields.Integer(string="Limit", required=True)
    total_records = fields.Integer(string="Total Records")

    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("processed", "Processed"),
            ("failed", "Failed"),
        ],
        string="Status",
        default="pending",
        required=True,
        index=True,
    )
    retry_count = fields.Integer(string="Retry Count", default=0)
    error_response = fields.Text(string="Error Response")

    @api.depends("batch_number", "request_id.correlation_id", "request_id.bg_request_id")
    def _compute_name(self):
        for rec in self:
            base = _("Batch %(num)s", num=rec.batch_number or 0)
            if rec.request_id and rec.request_id.correlation_id:
                rec.name = _("%(base)s / Req %(corr)s", base=base, corr=rec.request_id.correlation_id)
            elif rec.request_id and rec.request_id.bg_request_id:
                rec.name = _("%(base)s / Req %(bg)s", base=base, bg=rec.request_id.bg_request_id)
            else:
                rec.name = base
