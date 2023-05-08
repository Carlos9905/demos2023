odoo.define('barcode_price.pos_barcode_price', function (require) {
    "use strict";

    var core = require('web.core');
    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var BarcodeEvents = require('barcodes.BarcodeEvents');

    var _t = core._t;

    screens.PaymentScreenWidget.include({
        renderElement: function() {
            this._super();

            var self = this;
            var order = this.pos.get_order();

            var barcode_event = new BarcodeEvents();
            barcode_event.attachTo(self.$('.payment-numpad'));

            barcode_event.on('barcode_scanned', function(barcode) {
                rpc.query({
                    model: 'pos.barcode.price',
                    method: 'search_read',
                    domain: [['barcode', '=', barcode], ['config_id', '=', self.pos.config.id]],
                    fields: ['product_id', 'price'],
                    limit: 1,
                }).then(function(results) {
                    if (results.length > 0) {
                        var product = self.pos.db.get_product_by_id(results[0].product_id[0]);
                        var price = results[0].price;
                        if (product) {
                            order.add_product(product, {
                                price: price,
                            });
                        }
                    }
                });
            });
        },
    });

});
