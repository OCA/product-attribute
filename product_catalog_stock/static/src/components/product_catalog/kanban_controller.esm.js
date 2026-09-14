import {_t} from "@web/core/l10n/translation";
import {ProductCatalogKanbanController} from "@product/product_catalog/kanban_controller";
import {patch} from "@web/core/utils/patch";

patch(ProductCatalogKanbanController.prototype, {
    async _defineButtonContent() {
        if (this.orderResModel === "stock.picking") {
            this.buttonString = _t("Back to picking");
        } else {
            super._defineButtonContent();
        }
    },
});
