/** @odoo-module **/

import {ProductCatalogKanbanController} from "./kanban_controller.esm";
import {ProductCatalogKanbanModel} from "./kanban_model.esm";
import {ProductCatalogSearchPanel} from "./search/search_panel.esm";
import {kanbanView} from "@web/views/kanban/kanban_view";
import {registry} from "@web/core/registry";

export const productCatalogKanbanView = {
    ...kanbanView,
    Controller: ProductCatalogKanbanController,
    Model: ProductCatalogKanbanModel,
    SearchPanel: ProductCatalogSearchPanel,
};

registry.category("views").add("product_kanban_catalog", productCatalogKanbanView);
