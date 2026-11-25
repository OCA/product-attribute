odoo.define("product_attribute_groupby.ProductAttributeGroupBy", function (require) {
    "use strict";
    const DropdownMenuItem = require("web.DropdownMenuItem");
    const GroupByMenu = require("web.GroupByMenu");
    const patchMixin = require("web.patchMixin");
    const {useModel} = require("web/static/src/js/model.js");
    const {onWillStart, useState} = owl.hooks;
    const MAX_SLOTS = 3;

    class ProductAttributeGroupBy extends DropdownMenuItem {
        constructor() {
            super(...arguments);
            this.model = useModel("searchModel");
            this._resModel = this.model.config.modelName;
        }
        setup() {
            super.setup();
            this.state = useState({open: false, attributes: [], selectedId: null});
            onWillStart(async () => {
                if (this._resModel !== "product.product") return;
                try {
                    const attrs = await this.env.services.rpc({
                        model: "product.product",
                        method: "get_groupby_attribute_fields",
                        args: [],
                        kwargs: {context: {}},
                    });
                    this.state.attributes = attrs;
                    if (attrs.length) this.state.selectedId = attrs[0].id;
                } catch (e) {
                    console.error("[ProductAttributeGroupBy] RPC error:", e);
                }
            });
        }
        _onChangeSelect(ev) {
            this.state.selectedId = parseInt(ev.target.value, 10);
        }

        _activeSlotFor(attrId) {
            const filters = this.model.get("filters") || [];
            for (let slot = 1; slot <= MAX_SLOTS; slot++) {
                const pag = filters.find(
                    (f) =>
                        f.type === "filter" &&
                        f.description === "__groupby_attr_" + slot
                );
                if (!pag) continue;
                const ctx = pag.context || {};
                if (ctx["groupby_attribute_id_" + slot] === attrId) return slot;
            }
            return null;
        }

        _nextFreeSlot() {
            const filters = this.model.get("filters") || [];
            for (let slot = 1; slot <= MAX_SLOTS; slot++) {
                const pag = filters.find(
                    (f) =>
                        f.type === "filter" &&
                        f.description === "__groupby_attr_" + slot
                );
                if (!pag) return slot;
            }
            return null;
        }

        _removeSlot(slot) {
            const filters = this.model.get("filters") || [];
            const groupBy = filters.find(
                (f) => f.type === "groupBy" && f.name === "attribute_group_by_" + slot
            );
            if (groupBy) this.model.dispatch("deleteSearchItem", groupBy.id);
            const pag = filters.find(
                (f) => f.type === "filter" && f.description === "__groupby_attr_" + slot
            );
            if (pag) this.model.dispatch("deleteSearchItem", pag.id);
            const ctx = Object.assign({}, this.model.config.context);
            delete ctx["groupby_attribute_id_" + slot];
            this.model.config.context = ctx;
        }

        _onApply() {
            const selected = this.state.attributes.find(
                (a) => a.id === this.state.selectedId
            );
            if (!selected) return;

            const activeSlot = this._activeSlotFor(selected.id);
            if (activeSlot !== null) {
                this._removeSlot(activeSlot);
                this.state.open = false;
                return;
            }

            const slot = this._nextFreeSlot();
            if (slot === null) return;

            const fieldName = "attribute_group_by_" + slot;
            const ctxKey = "groupby_attribute_id_" + slot;
            const field = this.model.config.fields[fieldName];
            if (!field) return;

            this.model.config.context = Object.assign({}, this.model.config.context, {
                [ctxKey]: selected.id,
            });
            this.model.dispatch("createNewFilters", [
                {
                    type: "filter",
                    description: "__groupby_attr_" + slot,
                    domain: "[]",
                    context: {["groupby_attribute_id_" + slot]: selected.id},
                },
            ]);
            this.model.dispatch("createNewGroupBy", {
                ...field,
                description: selected.label,
                name: fieldName,
                string: selected.label,
            });

            this.state.open = false;
        }
    }
    ProductAttributeGroupBy.template =
        "product_attribute_groupby.ProductAttributeGroupBy";
    const PatchedProductAttributeGroupBy = patchMixin(ProductAttributeGroupBy);
    GroupByMenu.components = Object.assign({}, GroupByMenu.components, {
        ProductAttributeGroupBy: PatchedProductAttributeGroupBy,
    });
    return PatchedProductAttributeGroupBy;
});

odoo.define("product_attribute_groupby.PatchFacets", function (require) {
    "use strict";

    const ControlPanelModelExtension = require("web/static/src/js/control_panel/control_panel_model_extension.js");

    const originalGetFacets = ControlPanelModelExtension.prototype._getFacets;

    ControlPanelModelExtension.prototype._getFacets = function () {
        return originalGetFacets.call(this).filter((facet) => {
            if (facet.type !== "filter") return true;
            return !facet.title.startsWith("__groupby_attr_");
        });
    };
});
