import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-product-attribute",
    description="Meta package for oca-product-attribute Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-product_bom_revision',
        'odoo14-addon-product_code_unique',
        'odoo14-addon-product_cost_security',
        'odoo14-addon-product_dimension',
        'odoo14-addon-product_multi_category',
        'odoo14-addon-product_secondary_unit',
        'odoo14-addon-product_sequence',
        'odoo14-addon-product_template_tags',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
