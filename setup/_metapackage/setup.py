import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-pricelist_per_product',
        'odoo9-addon-product_attribute_priority',
        'odoo9-addon-product_brand',
        'odoo9-addon-product_custom_info',
        'odoo9-addon-product_dimension',
        'odoo9-addon-product_gtin',
        'odoo9-addon-product_manufacturer',
        'odoo9-addon-product_multi_category',
        'odoo9-addon-product_multi_image',
        'odoo9-addon-product_pricelist_direct_print',
        'odoo9-addon-product_pricelist_item_list_view',
        'odoo9-addon-product_pricelist_tax_included',
        'odoo9-addon-product_sequence',
        'odoo9-addon-product_supplierinfo_revision',
        'odoo9-addon-product_uom',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
