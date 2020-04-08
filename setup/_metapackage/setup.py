import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-product_brand',
        'odoo11-addon-product_code_mandatory',
        'odoo11-addon-product_code_unique',
        'odoo11-addon-product_cost_security',
        'odoo11-addon-product_dimension',
        'odoo11-addon-product_end_of_life',
        'odoo11-addon-product_firmware_version',
        'odoo11-addon-product_manufacturer',
        'odoo11-addon-product_multi_category',
        'odoo11-addon-product_multi_price',
        'odoo11-addon-product_pricelist_direct_print',
        'odoo11-addon-product_pricelist_supplierinfo',
        'odoo11-addon-product_priority',
        'odoo11-addon-product_restricted_type',
        'odoo11-addon-product_secondary_unit',
        'odoo11-addon-product_sequence',
        'odoo11-addon-product_state',
        'odoo11-addon-product_supplierinfo_for_customer',
        'odoo11-addon-product_supplierinfo_revision',
        'odoo11-addon-product_template_tags',
        'odoo11-addon-product_weight',
        'odoo11-addon-product_weight_through_uom',
        'odoo11-addon-stock_production_lot_firmware_version',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
