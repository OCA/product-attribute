This module permits to quickly see the different prices of a product : price with taxes and price without taxes.

The four use cases
------------------

In Customer taxes, there's a boolean called "Tax included in Price".

.. image:: ../static/description/taxes_creation.png
   :alt: Choice of customer taxes
   :width: 40%

**According to the customer taxes** of the product (choosen in accouting part), there are 4 possibilities :

- The sale price **AND** the sale price without taxes are displayed.

.. image:: ../static/description/product_tax_included.png
   :alt: A product with sale price and sale price without taxes
   :width: 75%

- **Or** the sale price **AND** the sale price with taxes.

.. image:: ../static/description/product_tax_excluded.png
   :alt: A product with sale price and sale price with taxes
   :width: 75%

- **Or** if you choose two customer taxes, one included in price, and the other
  one not included in price, this module displays the sale price and the two
  calculated prices.

.. image:: ../static/description/product_tax_included_and_not.png
   :alt: A product with sale price without taxes, sale price, sale price with taxes
   :width: 75%

- **And lastly** if there's no taxe choosen, only the normal price is displayed.

.. image:: ../static/description/product_no_tax.png
   :alt: A product with a unique sale price
   :width: 75%
