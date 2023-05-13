from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    @api.onchange('lst_price')
    def _onchange_lst_price(self):
        for template in self:
            if template.lst_price:
                self.env["price.history"].create(
                    {
                        "product_template_id":template.id,
                        "old_price":template.lst_price
                    }
                )


class PriceHistory(models.Model):
    _name = 'price.history'
    _description = 'Price History'

    product_template_id = fields.Many2one('product.template', string='Product Template', ondelete='cascade')
    old_price = fields.Float(string='Old Price')
    new_price = fields.Float(string='New Price')
    date = fields.Datetime(string='Date', default=lambda self: fields.Datetime.now())
