from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    precio_etd_id = fields.Many2one(
        'product.pricelist', string='Ubicación', ondelete='restrict',
        help="Relación con la tarifa para actualizar el precio de venta y la tarifa.")

    @api.onchange('precio_etd_id')
    def _update_sale_price(self):
        
        linea=self.env["product.pricelist.item"].search([("pricelist_id","=",self.precio_etd_id.id)])
        if self.precio_etd_id:
            self.lst_price = linea.fixed_price
        else:
            self.lst_price = 0
