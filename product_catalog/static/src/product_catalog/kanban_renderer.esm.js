/** @odoo-module **/

import {KanbanRenderer} from "@web/views/kanban/kanban_renderer";
import {ProductCatalogKanbanRecord} from "./kanban_record.esm";
import {useService} from "@web/core/utils/hooks";

export class ProductCatalogKanbanRenderer extends KanbanRenderer {
    setup() {
        super.setup();
        this.action = useService("action");
    }

    get createProductContext() {
        return {};
    }

    async createProduct() {
        await this.action.doAction(
            {
                type: "ir.actions.act_window",
                res_model: "product.product",
                target: "new",
                views: [[false, "form"]],
                view_mode: "form",
                context: this.createProductContext,
            },
            {
                onClose: () => this.props.list.model.load(),
            }
        );
    }
}
ProductCatalogKanbanRenderer.template = "ProductCatalogKanbanRenderer";
ProductCatalogKanbanRenderer.components = {
    ...KanbanRenderer.components,
    KanbanRecord: ProductCatalogKanbanRecord,
};
