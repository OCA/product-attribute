.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================
Product Profile
================

This module provides easier products configuration (in one click).
It allows to configure a product template with only one field.

.. image:: static/description/field.png

**Main use case**: a lot of modules are installed (mrp, purchase, sale, pos)
and products configuration becomes harder for end users: too many fields to take care of.

You are concerned that at any time a product might be not configured correctly: this module is your friend.

Thanks to this module, a lot of complexity becomes hidden (default behavior) to the end user and usability is optimal.

It eases as well the data migration by only specifying the profile field instead of all fields which depend on it.

Note: This module is meant to be used by skilled people in database fields creation within the ERP framework.

Additional feature: a default value can be attached to a profile (see § Configuration, part 3)



Configuration
=============

1. Create your own profile here: Sales > Configuration > Product Categories and Attributes > Product Profiles

.. image:: static/description/list.png


2. To have more fields available to attach to this profile you must define
   these fields in the model 'product.profile' in your own module
   If the field name (and its type) is the same than those in 'product.template'
   then values of these will be populated automatically
   in 'product.template'
   Example of fields declaration in your own module:

'''python

class ProductProfile(models.Model):
    """ Require dependency on sale, purchase and point_of_sale modules
    """

    _inherit = 'product.profile'

    def _get_types(self):
        return [('product', 'Stockable Product'),
                ('consu', 'Consumable'),
                ('service', 'Service')]

    sale_ok = fields.Boolean(
        string='Can be Sold',
        help="Specify if the product can be selected in a sales order line.")
    purchase_ok = fields.Boolean(
        string='Can be Purchased')
    available_in_pos = fields.Boolean()

'''

3. Second behavior: you might want to add a default behavior to these fields:
   in this case use prefix 'profile_default\_' for your field name
   in 'product.profile' model.

'''python

class ProductProfile(models.Model):
    ...
    profile_default_categ_id = fields.Many2one(
        'product.category',
        string='Default category')
    profile_default_route_ids = fields.Many2many(
        'stock.location.route',
        string=u'Default Routes',
        domain="[('product_selectable', '=', True)]",
        help="Depending on the modules installed, this will allow "
             "you to define the route of the product: "
             "whether it will be bought, manufactured, MTO/MTS,...")

'''

   In this case 'categ_id' field (from product.template) is populated
   with 'profile_default_categ_id' value but can be updated manually by the user.
   Careful: each time you change profile, the default value is also populated
   whatever the previous value. Custom value is only keep if don't change the profile.


4. Insert data (xml or csv) and define values for each field defined above
   for each configuration scenario


Usage
=====

Assign a value to the profile field in the product template form.
Then, all fields which depend on this profile will be set to the right value at once.

If you deselect the profile value, all these fields keep the same value and you can change them manually 
(back to standard behavior).

Install **Product Profile Example** module to see a use case in action.

Profiles are also defined as search filter and group.


Bug Tracker
===========

Bugs are tracked on 'GitHub Issues
<https://github.com/OCA/{project_repo}/issues>'_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* David BEAL <david.beal@akretion.com>
* Sébastien BEAU <sebastien.beau@akretion.com>
* Abdessamad HILALI <abdessamad.hilali@akretion.com>

Iconography
-----------

https://www.iconfinder.com/icondesigner


Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.

