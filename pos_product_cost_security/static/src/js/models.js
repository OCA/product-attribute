odoo.define("pos_product_cost_security.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");

    // Extend the product model context so we can inject an aditionl context key
    var existing_models = models.PosModel.prototype.models;
    var product_index = _.findIndex(existing_models, function (model) {
        return model.model === "product.product";
    });
    var product_model = existing_models[product_index];
    var context =
        typeof product_model.context === "function"
            ? product_model.context()
            : product_model.context || {};
    const extended_context = _.extend(context, {pos_override_cost_security: true});
    product_model.context = function () {
        return extended_context;
    };
});
