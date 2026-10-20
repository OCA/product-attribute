Add 'Type' field on Product Categories to distinguish between parent and final categories.

figure:: ../static/description/product_category_tree.png

* Categories (type view) can contain only categories.

* Categories (type normal) can contain only products.

It is so impossible to select a category (type view) in the product
template form view.

figure:: ../static/description/product_template_form.png

When installing the module, the categories that contain child categories
and that don't have any product related will be set as 'view'. Otherwise,
categories will be set as 'normal'.
If your database already contains products and categories data,
maybe you should fix some misconfigurations.

Note
----

This module restores a feature that was present in Odoo Community
Edition until the V10 revision.

Ref: https://github.com/odoo/odoo/blob/10.0/addons/product/models/product.py#L24
