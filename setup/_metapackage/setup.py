import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-product_brand',
        'odoo12-addon-product_manufacturer',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
