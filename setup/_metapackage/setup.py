import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-base_product_mass_addition',
        'odoo12-addon-packaging_uom',
        'odoo12-addon-product_assortment',
        'odoo12-addon-product_bom_revision',
        'odoo12-addon-product_brand',
        'odoo12-addon-product_category_active',
        'odoo12-addon-product_code_mandatory',
        'odoo12-addon-product_code_unique',
        'odoo12-addon-product_cost_security',
        'odoo12-addon-product_dimension',
        'odoo12-addon-product_firmware_version',
        'odoo12-addon-product_logistics_uom',
        'odoo12-addon-product_manufacturer',
        'odoo12-addon-product_multi_category',
        'odoo12-addon-product_multi_price',
        'odoo12-addon-product_pricelist_direct_print',
        'odoo12-addon-product_pricelist_revision',
        'odoo12-addon-product_pricelist_supplierinfo',
        'odoo12-addon-product_priority',
        'odoo12-addon-product_product_template_navigation',
        'odoo12-addon-product_restricted_type',
        'odoo12-addon-product_secondary_unit',
        'odoo12-addon-product_sequence',
        'odoo12-addon-product_standard_price_tax_included',
        'odoo12-addon-product_state',
        'odoo12-addon-product_stock_state',
        'odoo12-addon-product_supplierinfo_for_customer',
        'odoo12-addon-product_supplierinfo_revision',
        'odoo12-addon-product_template_tags',
        'odoo12-addon-product_uom_use_type',
        'odoo12-addon-product_variant_inactive',
        'odoo12-addon-product_weight',
        'odoo12-addon-stock_production_lot_firmware_version',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
