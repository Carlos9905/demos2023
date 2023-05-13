from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('list_price')
    def _onchange_list_price(self):
        for template in self:
            if template.list_price:
                self.env["price.history"].create(
                    {
                        "product_template_id": template.id,
                        "old_price": template.list_price
                    }
                )


class PriceHistory(models.Model):
    _name = 'price.history'
    _description = 'Price History'

    product_template_id = fields.Many2one('product.template', string='Product Template', ondelete='cascade')
    old_price = fields.Float(string='Old Price')
    new_price = fields.Float(string='New Price')
    date = fields.Datetime(string='Date', default=lambda self: fields.Datetime.now())
    barcode = fields.Char(related='product_template_id.barcode', string='Barcode')
    default_code = fields.Char(related='product_template_id.default_code', string='Default Code')
