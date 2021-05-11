import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-customer_pricing_in_product_view',
        'odoo8-addon-pricelist_item_generator',
        'odoo8-addon-pricelist_per_product',
        'odoo8-addon-product_attribute_multi_type',
        'odoo8-addon-product_attribute_priority',
        'odoo8-addon-product_brand',
        'odoo8-addon-product_categ_image',
        'odoo8-addon-product_code_builder',
        'odoo8-addon-product_code_builder_sequence',
        'odoo8-addon-product_custom_info',
        'odoo8-addon-product_dimension',
        'odoo8-addon-product_gtin',
        'odoo8-addon-product_m2mcategories',
        'odoo8-addon-product_manufacturer',
        'odoo8-addon-product_multi_image',
        'odoo8-addon-product_price_history',
        'odoo8-addon-product_pricelist_cache',
        'odoo8-addon-product_pricelist_fixed_price',
        'odoo8-addon-product_profile',
        'odoo8-addon-product_profile_example',
        'odoo8-addon-product_sale_tax_price_included',
        'odoo8-addon-product_sequence',
        'odoo8-addon-product_standard_price_tax_included',
        'odoo8-addon-product_supplierinfo_for_customer',
        'odoo8-addon-product_supplierinfo_for_customer_sale',
        'odoo8-addon-product_supplierinfo_tree_price_info',
        'odoo8-addon-product_variant_inactive',
        'odoo8-addon-product_weight',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
