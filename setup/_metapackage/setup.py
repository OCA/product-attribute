import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-product_brand',
        'odoo11-addon-product_code_unique',
        'odoo11-addon-product_firmware_version',
        'odoo11-addon-product_manufacturer',
        'odoo11-addon-product_priority',
        'odoo11-addon-product_state',
        'odoo11-addon-stock_production_lot_firmware_version',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
