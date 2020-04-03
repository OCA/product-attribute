Relation Type Tabs
~~~~~~~~~~~~~~~~~~

Before being able to show certain types of relations on a tab in the product
form, you will have to define the tab.

Do that in Products / Relations / Relation Tabs.

.. image:: ../static/description/product_multi_relation_tabs-tab-configuration.png

If you specify nothing, the tab will be shown on all product forms that have
tabs (page elements). Normally you will select to show the tab only on
products that are consumable, or only for services. You can also
select a category to further limit for which products the tab wil be shown.

The possibility exists to show a tab only on specific products. For instance
on your own company product.

Relation Types
~~~~~~~~~~~~~~

In configuring the relation types, you can select which type of relation will
be shown on which tab. It is possible to show multiple types on one tab.

Do that in Products / Relations / Relation Types.

For example on a 'related products' tab, you might want to show accessories,
but also spare parts.

You might specify a tab for both the 'left side' of a relation, as for the
'right side' of inverse relation.

For each side of a relation, the product product type and the product category
must be consistent with those specified for the tab.

.. image:: ../static/description/product_multi_relation_tabs-relation-type-configuration.png

Product Form
~~~~~~~~~~~~

The product form will contain extra tab pages, for each tab that is
appropiate for that product. So a company product does not show the tabs that
are meant for persons and vice versa. Also tabs meant for products with
a certain category/label will only show if products have that label.

When adding relations on a tab, only relation types appropiate for that tab
can be selected.

Example of adding a relation:

.. image:: ../static/description/product_multi_relation_tabs-product-edit.png

Example of a filled out board tab:

.. image:: ../static/description/product_multi_relation_tabs-product-display.png

Deleting tabs
~~~~~~~~~~~~~

When a tab is deleted, this will in no way effect the existing relations.

However the references on the relation types to the deleted tabs will also be
cleared.

Searching Relations by Tab
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can search relations with the tab on which they are shown. For instance
to find all board members.

Do that in Products / Relations / Relations.

.. image:: ../static/description/product_multi_relation_tabs-relation-search.png
