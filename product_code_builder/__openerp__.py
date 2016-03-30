# coding: utf-8
#    @author Abdessamad HILALI <abdessamad.hilali@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Product Code Builder",
    'author': "Akretion,Odoo Community Association (OCA)",
    'summary': "Create product references according to attributes",
    'website': "http://www.Akretion.com",
    'license': 'AGPL-3',
    'category': 'Product',
    'version': '8.0.0.0.1',
    'depends': ['sale'],
    'data': [
        'views/product_view.xml',
        'views/product_attribute_view.xml'
    ],
    'demo': [
        'demo/product.attribute.csv',
        'demo/product.attribute.value.csv',
        'demo/product_demo.xml',
        ],
    'installable': True,
}
