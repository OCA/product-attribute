import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-customer_pricing_in_product_view',
        'odoo10-addon-product_assortment',
        'odoo10-addon-product_brand',
        'odoo10-addon-product_categ_image',
        'odoo10-addon-product_code_remove',
        'odoo10-addon-product_code_unique',
        'odoo10-addon-product_country_restriction',
        'odoo10-addon-product_custom_info',
        'odoo10-addon-product_default_image',
        'odoo10-addon-product_dimension',
        'odoo10-addon-product_manufacturer',
        'odoo10-addon-product_multi_category',
        'odoo10-addon-product_multi_image',
        'odoo10-addon-product_pricelist_tier',
        'odoo10-addon-product_profile',
        'odoo10-addon-product_profile_example',
        'odoo10-addon-product_secondary_unit',
        'odoo10-addon-product_sequence',
        'odoo10-addon-product_service_duration',
        'odoo10-addon-product_special_type',
        'odoo10-addon-product_state',
        'odoo10-addon-product_supplierinfo_for_customer',
        'odoo10-addon-product_template_tags',
        'odoo10-addon-product_uom',
        'odoo10-addon-product_variant_inactive',
        'odoo10-addon-product_weight',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
