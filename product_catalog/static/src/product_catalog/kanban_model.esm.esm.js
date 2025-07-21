/** @odoo-module */

import rpc from "web.rpc";
import {Record, RelationalModel} from "@web/views/relational_model";

class ProductCatalogRecord extends Record {
    setup(config, data, options) {
        options = options || {};
        this.rpc = rpc;
        this.productCatalogData = data.productCatalogData;
        data = {...data};
        delete data.productCatalogData;
        super.setup(config, data, options);
    }
}

export class ProductCatalogKanbanModel extends RelationalModel {
    static get Record() {
        return ProductCatalogRecord;
    }

    async _loadData(params) {
        const result = await super._loadData(...arguments);
        if (!params.isMonoRecord && !params.groupBy.length) {
            const orderLinesInfo = await this.rpc(
                "/product/catalog/order_lines_info",
                this._getOrderLinesInfoParams(
                    params,
                    result.records.map((rec) => rec.id)
                )
            );
            for (const record of result.records) {
                record.productCatalogData = orderLinesInfo[record.id];
            }
        }
        return result;
    }

    _getOrderLinesInfoParams(params, productIds) {
        return {
            order_id: params.context.order_id,
            product_ids: productIds,
            res_model: params.context.product_catalog_order_model,
            child_field: params.context && params.context.child_field,
        };
    }
}
