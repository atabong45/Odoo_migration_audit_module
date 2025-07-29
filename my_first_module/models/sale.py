from odoo import models, fields

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    # Example of adding a new field
    custom_field = fields.Char(string='Custom Field')
    other_custom_field = fields.Char(string='Other Custom Field')
