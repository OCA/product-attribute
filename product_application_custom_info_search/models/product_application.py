# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductApplication(models.Model):
    _inherit = 'product.application'

    def get_filtered_product_tmpl_ids(self, custom_property, value):
        # Get all product applications according previous selection:
        product_app_model = self.env.ref(
            'product_application.model_product_application')
        field_type = custom_property.field_type
        if field_type == 'bool':
            value_bool = 'f'
            if value.value_bool:
                value_bool = 't'
            where_value = 'AND prop.field_type = \'bool\''\
                ' AND val.value_bool = \'%s\'' % value_bool
        elif field_type == 'float':
            where_value = 'AND prop.field_type = \'float\''\
                ' AND val.value_float = %s' % value.value_float
        elif field_type == 'str':
            where_value = 'AND prop.field_type = \'str\''\
                ' AND val.value_str = \'%s\'' % value.value_str
        elif field_type == 'int':
            where_value = 'AND prop.field_type = \'int\''\
                ' AND val.value_int = %s' % value.value_int
        elif field_type == 'id':
            where_value = 'AND prop.field_type = \'id\''\
                ' AND val.value_id = %s' % value.value_id.id
        else:
            raise

        query = '''SELECT
    prod_app.product_tmpl_id
FROM
    custom_info_property prop,
    custom_info_template tmpl,
    custom_info_value val,
    product_application prod_app
WHERE
    tmpl.model_id = %s
    AND prop.template_id = tmpl.id
    AND val.property_id = prop.id
    AND prod_app.custom_info_template_id = tmpl.id
    AND prod_app.id = val.res_id
    AND prop.id = %s
'''
        query += where_value
        self.env.cr.execute(
            query, tuple([product_app_model.id, custom_property.id])
        )
        product_tmpl_ids = [row[0] for row in self.env.cr.fetchall()]
        return product_tmpl_ids
