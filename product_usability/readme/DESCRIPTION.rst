This module extends the Odoo CE product module to fill gaps present in the module.

New Menu items
~~~~~~~~~~~~~~
By default, when installing ``product`` module, a lot of menu items
are not created and are available only if other module are installed.
For exemple:

* Manage product categories requires to install ``stock`` module,
  that creates the menu entry
  _"Inventory / Configuration / Product / Product Categories"_.
* Manage product tags requires to install ``sale_management`` module,
  that creates the menu entry
  _"Sale / Configuration / Products / Tags"_.

This module so creates a new main menu item named 'Product' that provides
all menu entries to see and manage product, attributes, pricelists,
Units of Measure, etc. So that all the product configuration is available
in a unique place.

.. figure:: ../static/description/main_menu.png

New Access Rights
~~~~~~~~~~~~~~~~~

By default, to create product, attributes, pricelist, categories,
User should be member of a group that adds a lot of rights, like
'Inventory / Manager' or 'Sale / Manager'.

This module adds new Access rules to fine-tune access rights,
creating the following rules:

* _"Product Creation"_: Allow to create Products (``product.template``),
  Variants (``product.product``), Product Template Attribute Lines
  (``product.template.attribute.line``) and Product Template Attribute Values
  (``product.template.attribute.value``)

* _"Product Attribute Creation"_: Allow to create Attributes (``product.attribute``)
  and Values (``product.attribute.value``).

* _"Product Tag Creation"_: Allow to create Tags (``product.tag``)

* _"Product Category Creation"_: Allow to create Categories (``product.category``)

* _"Product Supplier Pricelist Creation"_: Allow to create Supplier Pricelists (``product.supplierinfo``)

* _"Unit of Measure Creation"_: Allow to create Unit of Measures
  (``uom.uom``) and Unit of Measures Categories (``uom.category``)
