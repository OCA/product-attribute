odoo.define('product_lifecycle.replacement_product', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var field_registry = require('web.field_registry');
    var QWeb = core.qweb;

    var ShowReplacementProduct = AbstractField.extend({
        _render: function(){
            this._super.apply(this, arguments);
            var info = JSON.parse(this.value);

            this.$el.html(QWeb.render('ProductReplacement', {
                'replaced_by': info.replaced_by || "No product found.",
                'state': info.state || 'Obsoleted',
                'product_qty': info.product_qty || '0',
            }));
        },
    });

    field_registry.add('replacement_product', ShowReplacementProduct);
});
