odoo.define('product_lifecycle.replacement_product', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var field_registry = require('web.field_registry');
    var QWeb = core.qweb;
    var _t = core._t;

    var ShowReplacementProduct = AbstractField.extend({
        _render: function(){
            this._super.apply(this, arguments);
            var info = JSON.parse(this.value);
            var state = _t('obsolete');
            switch (info.state){
                case 'obsolete':
                    state = _t('obsolete');
                    break;
                case 'end':
                    state = _t('in the end of lifecycle');
                    break;
            }
            this.$el.html(QWeb.render('ProductReplacement', {
                'replaced_by': info.replaced_by || _t("No product found"),
                'state': state,
                'product_qty': info.product_qty || '0',
            }));
        },
    });

    field_registry.add('replacement_product', ShowReplacementProduct);
});
