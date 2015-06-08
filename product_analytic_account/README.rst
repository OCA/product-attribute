Product Analytic Account
========================

This module allows you to configure an **income analytic account** and an **expense analytic account** on products and on product categories. When you select the product in an invoice line, it will check if this product has an income analytic account (for customer invoice/refunds) or an expense analytic account (for supplier invoice/refunds) ; if it doesn't find any, it checks if the category of the product has an income or expense analytic account ; if an analytic account is found, it will be set by default on the invoice line.

This module is an alternative to the official module *account_analytic_default*. The advantages of this module are:
- it only depends on the *account* module, whereas the *account_analytic_default* module depends on *sale_stock* ;
- the analytic account is configured on the product form or the product category form, and not on a separate object.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
