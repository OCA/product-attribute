import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-product_assortment>=16.0dev,<16.1dev',
        'odoo-addon-product_attribute_archive>=16.0dev,<16.1dev',
        'odoo-addon-product_attribute_company_favorite>=16.0dev,<16.1dev',
        'odoo-addon-product_category_active>=16.0dev,<16.1dev',
        'odoo-addon-product_category_code>=16.0dev,<16.1dev',
        'odoo-addon-product_code_unique>=16.0dev,<16.1dev',
        'odoo-addon-product_cost_security>=16.0dev,<16.1dev',
        'odoo-addon-product_dimension>=16.0dev,<16.1dev',
        'odoo-addon-product_expiry_configurable>=16.0dev,<16.1dev',
        'odoo-addon-product_logistics_uom>=16.0dev,<16.1dev',
        'odoo-addon-product_manufacturer>=16.0dev,<16.1dev',
        'odoo-addon-product_multi_category>=16.0dev,<16.1dev',
        'odoo-addon-product_net_weight>=16.0dev,<16.1dev',
        'odoo-addon-product_packaging_dimension>=16.0dev,<16.1dev',
        'odoo-addon-product_pricelist_revision>=16.0dev,<16.1dev',
        'odoo-addon-product_pricelist_simulation>=16.0dev,<16.1dev',
        'odoo-addon-product_pricelist_simulation_margin>=16.0dev,<16.1dev',
        'odoo-addon-product_route_mto>=16.0dev,<16.1dev',
        'odoo-addon-product_secondary_unit>=16.0dev,<16.1dev',
        'odoo-addon-product_sequence>=16.0dev,<16.1dev',
        'odoo-addon-product_state>=16.0dev,<16.1dev',
        'odoo-addon-product_supplierinfo_for_customer>=16.0dev,<16.1dev',
        'odoo-addon-product_template_has_one_variant>=16.0dev,<16.1dev',
        'odoo-addon-product_uom_measure_type>=16.0dev,<16.1dev',
        'odoo-addon-product_uom_updatable>=16.0dev,<16.1dev',
        'odoo-addon-sale_product_template_tags>=16.0dev,<16.1dev',
        'odoo-addon-stock_production_lot_expired_date>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
