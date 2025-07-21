/** @odoo-module **/

import {ProductCatalogKanbanModel} from "./kanban_model";
import {ProductCatalogSearchPanel} from "./search/search_panel";
import {kanbanView} from "@web/views/kanban/kanban_view";
import {registry} from "@web/core/registry";

export const productCatalogKanbanView = {
    ...kanbanView,
    Model: ProductCatalogKanbanModel,
    SearchPanel: ProductCatalogSearchPanel,
};

registry.category("views").add("product_kanban_catalog", productCatalogKanbanView);
