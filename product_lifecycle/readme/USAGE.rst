**Lifecycle Status**

The status of the ``Product Variant`` is managed in the header of the product 
form view as a clickable status bar widget, and with the default value ``Normal``.

The possible lifecycle states are:

- ``Normal``: An active product that can be sell or purchase.
- ``End of Lifecycle``: This means that the product is a discontinued product but there is still in stock.
- ``Obsolete``: This means that the product is a discontinued product and has no stock.

Search filters were added to search and group-by products by its lifecycle status.


**Replacement Products**

A new field section named ``Replacement Info`` was added to the ``Product Variant`` 
form view to hold the information about replacements products. This applies when 
the product is a ``obsolete`` product. There are new fields:

- ``Replaced By``: Apply when the current product is an obsolete product, 
  this field is the new product that will be replaced by the current product.
- ``Replace To``: This field holds an obsolete product and indicates that 
  the current product is the new replacement of the obsolete product.

**Sale Order and Obsolete Products**

This module adds a widget to inform the product lifecycle status and avoid 
selling an obsolete product.

Also, when you sell a ``End of Life`` product and there is no existence of 
the product (stock inventory 0.0) the product state will be affected. 
The product will change automatically from ``End of Life`` to ``Obsolete`` state.  
This is an automatic action and it can be configured to be run in the system.
