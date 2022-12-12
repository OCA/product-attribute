import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-product_category_code>=15.0dev,<15.1dev',
        'odoo-addon-product_category_code_unique>=15.0dev,<15.1dev',
        'odoo-addon-product_category_product_link>=15.0dev,<15.1dev',
        'odoo-addon-product_code_mandatory>=15.0dev,<15.1dev',
        'odoo-addon-product_code_unique>=15.0dev,<15.1dev',
        'odoo-addon-product_cost_security>=15.0dev,<15.1dev',
        'odoo-addon-product_dimension>=15.0dev,<15.1dev',
        'odoo-addon-product_manufacturer>=15.0dev,<15.1dev',
        'odoo-addon-product_net_weight>=15.0dev,<15.1dev',
        'odoo-addon-product_packaging_type>=15.0dev,<15.1dev',
        'odoo-addon-product_secondary_unit>=15.0dev,<15.1dev',
        'odoo-addon-product_state>=15.0dev,<15.1dev',
        'odoo-addon-product_supplierinfo_for_customer>=15.0dev,<15.1dev',
        'odoo-addon-product_template_tags>=15.0dev,<15.1dev',
        'odoo-addon-sale_product_template_tags>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
