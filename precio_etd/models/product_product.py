from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    precio_etd_id = fields.Many2one(
        'product.pricelist', string='Ubicación', ondelete='restrict',
        help="Relación con la tarifa para actualizar el precio de venta y la tarifa.")

    """@api.onchange('precio_etd_id')
    def _onchange_precio_etd_id(self):
        if self.precio_etd_id:
            self.list_price = self.precio_etd_id.get_product_price(self, 1, False)
        else:
            self.list_price = 0.0

    @api.onchange('list_price')
    def _onchange_list_price(self):
        if self.precio_etd_id:
            self.precio_etd_id.write({
                'item_ids': [(0, 0, {
                    'product_id': self.id,
                    'fixed_price': self.list_price
                })]
            })
"""