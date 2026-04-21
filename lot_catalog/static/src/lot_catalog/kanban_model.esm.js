import {Record} from "@web/model/relational_model/record";
import {RelationalModel} from "@web/model/relational_model/relational_model";
import {rpc} from "@web/core/network/rpc";

class LotCatalogRecord extends Record {
    setup(config, data, options = {}) {
        this.lotCatalogData = data.lotCatalogData;
        // eslint-disable-next-line no-param-reassign
        data = {...data};
        delete data.lotCatalogData;
        super.setup(config, data, options);
    }
}

export class LotCatalogKanbanModel extends RelationalModel {
    static Record = LotCatalogRecord;

    async _loadData(params) {
        const result = await super._loadData(...arguments);
        if (!params.isMonoRecord && !params.groupBy.length) {
            const orderLinesInfo = await rpc(
                "/lot/catalog/order_lines_info",
                this._getOrderLinesInfoParams(
                    params,
                    result.records.map((rec) => rec.id)
                )
            );
            for (const record of result.records) {
                record.lotCatalogData = orderLinesInfo[record.id];
            }
        }
        return result;
    }

    _getOrderLinesInfoParams(params, lotIds) {
        return {
            order_id: params.context.order_id,
            lot_ids: lotIds,
            res_model: params.context.lot_catalog_order_model,
            child_field: params.context?.child_field,
        };
    }
}
