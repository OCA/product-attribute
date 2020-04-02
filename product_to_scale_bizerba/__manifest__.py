# Copyright (C) 2016-Today GRAP (http://www.grap.coop)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Products - Send to Scales',
    'summary': 'Synchronize Odoo database with Scales',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'description': """
=============================================
Synchronize Odoo database with Bizerba Scales
=============================================

Roadmap / Know Issues
---------------------

* It should be great to split this module into many modules, with some generic
  features in a module named product_to_scale and some specifics features
  for each scales system. 'product_to_scale_bizerba',
  'product_to_scale_metler_toledo', etc.

""",
    'author': 'GRAP, Druidoo',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'pos_sale',
    ],
    'data': [
        'security/ir_module_category.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_config_parameter.xml',
        'data/ir_cron.xml',
        'views/view_product_product.xml',
        'views/view_product_uom.xml',
        'views/view_product_scale_system.xml',
        'views/view_product_scale_group.xml',
        'views/view_product_scale_log.xml',
        'wizard/confirm_update_wizard_view.xml',
    ],
    'demo': [
        'demo/res_users.xml',
        'demo/product_scale_system.xml',
        'demo/product_scale_system_product_line.xml',
        'demo/product_scale_group.xml',
        'demo/product_product.xml',
        'demo/decimal_precision.xml',
    ],
}
