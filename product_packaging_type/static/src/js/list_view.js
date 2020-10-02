
odoo.define('product_packaging_type.ListView', function (require) {
"use strict";

var ListView = require('web.ListView');

var ListView = ListView.List.include({
    init: function () {
        var self = this;
        this._super.apply(this, arguments);
     },

    // Natively supported in upper version. Hack minimize the diff
    // with the code in Odoo 12  and 13
    render_cell: function (record, column) {
        if (column.name === 'qty_per_type' && column.type === "html") {
            return record.get(column.id);
        } else {
            return this._super.apply(this, arguments);
        }
    }
});

});
