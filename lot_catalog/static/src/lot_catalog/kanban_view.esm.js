import {LotCatalogKanbanController} from "./kanban_controller.esm";
import {LotCatalogKanbanModel} from "./kanban_model.esm";
import {LotCatalogKanbanRenderer} from "./kanban_renderer.esm";
import {LotCatalogSearchPanel} from "./search/search_panel.esm";

import {kanbanView} from "@web/views/kanban/kanban_view";
import {registry} from "@web/core/registry";

export const lotCatalogKanbanView = {
    ...kanbanView,
    Controller: LotCatalogKanbanController,
    Model: LotCatalogKanbanModel,
    Renderer: LotCatalogKanbanRenderer,
    SearchPanel: LotCatalogSearchPanel,
};

registry.category("views").add("lot_kanban_catalog", lotCatalogKanbanView);
