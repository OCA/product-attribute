/** @odoo-module **/

import {KanbanRenderer} from "@web/views/kanban/kanban_renderer";
import {useService} from "@web/core/utils/hooks";

import {ProductCatalogKanbanRecord} from "./kanban_record.esm";

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

ProductCatalogKanbanRenderer.components = {
    ...KanbanRenderer.components,
    KanbanRecord: ProductCatalogKanbanRecord,
};
