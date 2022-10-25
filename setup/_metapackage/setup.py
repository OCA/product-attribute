import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-product_assortment>=16.0dev,<16.1dev',
        'odoo-addon-product_code_unique>=16.0dev,<16.1dev',
        'odoo-addon-product_logistics_uom>=16.0dev,<16.1dev',
        'odoo-addon-product_multi_category>=16.0dev,<16.1dev',
        'odoo-addon-product_packaging_dimension>=16.0dev,<16.1dev',
        'odoo-addon-product_sequence>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
