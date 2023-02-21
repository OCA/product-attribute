// @TODO: create yet another linking module for website_sale and product_pricelist_items_menu?
odoo.define("product_pricelist_items_menu.website", function (require) {
    "use strict";
    require("website_sale.website_sale");
    const Mixin = require("product_pricelist_items_menu.mixin");
    var sAnimations = require("website.content.snippets.animation");

    sAnimations.registry.WebsiteSale.include(Mixin);
});

odoo.define("ooops_dimenstions.ProductConfiguratorFormRenderer", function (require) {
    "use strict";

    const Mixin = require("product_pricelist_items_menu.mixin");
    const ProductConfiguratorFormRenderer = require("sale_product_configurator.ProductConfiguratorFormRenderer");

    ProductConfiguratorFormRenderer.include(Mixin);
    return ProductConfiguratorFormRenderer;
});
