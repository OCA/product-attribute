odoo.define("product_attribute_groupby.PatchFavoriteItem", function (require) {
    "use strict";

    const ControlPanelModelExtension = require("web/static/src/js/control_panel/control_panel_model_extension.js");

    const originalCreateNewFavorite =
        ControlPanelModelExtension.prototype.createNewFavorite;

    ControlPanelModelExtension.prototype.createNewFavorite = async function (
        preFilter
    ) {
        const attrIds = this._pagAttributeIds || {};

        if (!Object.keys(attrIds).length) {
            return originalCreateNewFavorite.call(this, preFilter);
        }

        const originalUserContext = Object.assign({}, this.env.session.user_context);
        Object.assign(this.env.session.user_context, attrIds);
        try {
            return await originalCreateNewFavorite.call(this, preFilter);
        } finally {
            for (const key of Object.keys(attrIds)) {
                delete this.env.session.user_context[key];
            }
            Object.assign(this.env.session.user_context, originalUserContext);
        }
    };
});
