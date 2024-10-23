/** @odoo-module **/
import {KanbanController} from "@web/views/kanban/kanban_controller";
import {onWillStart} from "@odoo/owl";
import {useDebounced} from "@web/core/utils/timing";
import {useService} from "@web/core/utils/hooks";

export class ProductCatalogKanbanController extends KanbanController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.orm = useService("orm");
        this.orderId = this.props.context.order_id;
        this.orderResModel = this.props.context.product_catalog_order_model;
        this.backToQuotationDebounced = useDebounced(this.backToQuotation, 500);
        onWillStart(async () => this._defineButtonContent());
    }

    // Force the slot for the "Back to Quotation" button to always be shown.
    get canCreate() {
        return true;
    }

    async _defineButtonContent() {
        // Render the button content depending on the model.
        const text_button = await this.orm.read(
            this.orderResModel,
            [this.orderId],
            ["catalog_button_text"]
        );
        this.buttonString = text_button[0].catalog_button_text;
    }

    async backToQuotation() {
        // Restore the last form view from the breadcrumbs if breadcrumbs are available.
        // If, for some weird reason, the user reloads the page then the breadcrumbs are
        // lost, and we fall back to the form view ourselves.
        if (this.env.config.breadcrumbs.length > 1) {
            await this.action.restore();
        } else {
            await this.action.doAction({
                type: "ir.actions.act_window",
                res_model: this.orderResModel,
                views: [[false, "form"]],
                view_mode: "form",
                res_id: this.orderId,
            });
        }
    }
}
