* Unable to save a product with an empty or blank internal reference.
* When creating more than one product variant from the template, a variant will be created
  with a default value for default_code field.
* A pre_init_hook process is initiated when there exist records without an internal reference(default_code).
  A default value is generated to populate empty field as a temporary value.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/12.0
