from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    precio_etd_id = fields.Many2one(
        'product.pricelist', string='Ubicación', ondelete='restrict',
        help="Relación con la tarifa para actualizar el precio de venta y la tarifa.")

    def update_sale_price(self):
        for record in self:
            if record.precio_etd_id:
                linea = self.env["product.pricelist.item"].search([("pricelist_id", "=", record.precio_etd_id.id)])
                record.list_price = linea.fixed_price
            else:
                record.list_price = 0

    @api.model
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'precio_etd_id' in vals:
            products_to_update = self.search([('precio_etd_id', '=', vals['precio_etd_id'])])
            products_to_update.update_sale_price()
        return res

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _mail_post_access = 'read'

    precio_etd_id = fields.Many2one(
        'product.pricelist', string='Ubicación', ondelete='restrict',
        help="Relación con la tarifa para actualizar el precio de venta y la tarifa.")
    
    lst_price = fields.Float(
        'Sales Price', default=1.0,
        digits='Product Price',
        help="Base price to compute the customer price. Sometimes called the catalog price.",
        track_visibility='onchange'
    )

    def update_sale_price(self):
        for record in self:
            if record.precio_etd_id:
                linea = self.env["product.pricelist.item"].search([("pricelist_id", "=", record.precio_etd_id.id)])
                record.lst_price = linea.fixed_price
            else:
                record.lst_price = 0

    def _update_parent_template(self, precio_etd_id):
        for record in self:
            record.product_tmpl_id.write({'precio_etd_id': precio_etd_id})

    @api.model
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if 'precio_etd_id' in vals:
            products_to_update = self.search([('precio_etd_id', '=', vals['precio_etd_id'])])
            products_to_update.update_sale_price()
            self._update_parent_template(vals['precio_etd_id'])
        return res

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    def _update_related_product_prices(self):
        for pricelist in self:
            products_to_update = self.env['product.product'].search([('precio_etd_id', '=', pricelist.id)])
            for product in products_to_update:
                product.update_sale_price()

    def write(self, vals):
        res = super(ProductPricelist, self).write(vals)
        if 'item_ids' in vals:
            self._update_related_product_prices()
        return res

class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    def write(self, vals):
        res = super(ProductPricelistItem, self).write(vals)
        if 'fixed_price' in vals and self.applied_on == '0_product_variant':
            self.pricelist_id._update_related_product_prices()
        return res
