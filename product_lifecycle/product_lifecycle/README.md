Product Lifecycle
=================

This module apply a part of the product lifecycle management concept by
extending the logic of the fields status in odoo and by adding a list of
repaclement products that will be used when a product is discontinued.

Lifecycle Status
----------------

The Status of the product now is manage in the header of the product form view
as a clickable statusbar widget and with default value `In Development`.

Also some search filters were added to search and group by products lifecycle
status.

Replacement Products
--------------------

A new field named `Replacement Products` were added to hold a list of products
that can be use as a replacement when the current product is discontinued.

A wizard was created to be popup everytime you are going to use a discontinued
product so you can view and select a replacement product.


Product Edit Restriction
------------------------

A new access rules over the `Products` and `Product Variants` records were
added. A product only can be edited by his product manager.