/** @odoo-module */
import {KanbanDynamicRecordList, KanbanModel} from "@web/views/kanban/kanban_model";

export class ProductCatalogDynamicRecordList extends KanbanDynamicRecordList {
    async _loadRecords() {
        const records = await super._loadRecords();
        const orderLinesInfo = await this.model.rpc(
            "/product/catalog/order_lines_info",
            {
                order_id: this.context.order_id,
                product_ids: records.map((rec) => rec.resId),
                res_model: this.context.product_catalog_order_model,
            }
        );
        for (const record of records) {
            record.productCatalogData = orderLinesInfo[record.resId];
        }
        return records;
    }
}

export class ProductCatalogKanbanModel extends KanbanModel {
    async _loadData(params) {
        if (!params.isMonoRecord && !params.groupBy && !params.groupBy.length) {
            const orderLinesInfo = await this.rpc("/product/catalog/order_lines_info", {
                order_id: params.context.order_id,
                product_ids: this.root.records.map((rec) => rec.resId),
                res_model: params.context.product_catalog_order_model,
            });
            for (const record of this.root.records) {
                record.productCatalogData = orderLinesInfo[record.id];
            }
        }
    }
}
ProductCatalogKanbanModel.DynamicRecordList = ProductCatalogDynamicRecordList;
