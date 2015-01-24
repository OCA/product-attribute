{
'name': 'Product Brand Manager',
'version': '0.1',
'category': 'Product',
'summary': ' brand',
'description': """
Product Brand Manager

=====================
This module allows your user to easily manage product brands. You can
define brands, attach a logo and a description to them. It also allows to
attach a partner to a brand. Once installed, check the menu
Product/configuration/brand
To do / To come:
- A view to seeing products by brand.
""",
'author': 'Prisnet Telecommunications SA ',
'website': 'http://www.prisnet.ch ',
'depends': ['product'],
'data': [
'product_brand_view.xml',
'security/ir.model.access.csv'
],
'installable': True,
}
