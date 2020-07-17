1. Create your own profile here:
   Sales > Configuration > Product > Product Profiles

   .. figure:: static/img/list.png
     :alt: profile list
     :width: 600 px

2. Extend "product.profile" model to add fields from product.template, either in normal mode or default mode (see note section below). These fields should be identical to their original fields **(especially "required" field attribute)**.

   .. code-block:: python

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

3. Insert data (xml or csv) and define values for each field defined above
   for each configuration scenario

Note :
You might want to declare profile fields as defaults. To do this, just prefix the field with "profile_default".

   .. code-block:: python

    class ProductProfile(models.Model):
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

Default fields only influence the records the first time they are set.
- if the profile is modified, changes are not propagated to all the records that have this profile
- if the record previously had another profile, changing profile will not influence default values
