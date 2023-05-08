from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    precio_etd_id = fields.Many2one(
        'product.pricelist', string='Ubicación', ondelete='restrict',
        help="Relación con la tarifa para actualizar el precio de venta y la tarifa.")

    @api.onchange('precio_etd_id')
    def _update_sale_price(self):
        for record in self:
            linea=self.env["product.pricelist.item"].search([("pricelist_id","=",record.precio_etd_id.id)])
            if record.precio_etd_id:
                record.lst_price = linea.fixed_price
            else:
                record.lst_price = 0


    """@api.onchange('list_price')
    def _onchange_list_price(self):
        if self.precio_etd_id:
            self.precio_etd_id.write({
                'item_ids': [(0, 0, {
                    'product_id': self.id,
                    'fixed_price': self.list_price
                })]
            })
"""