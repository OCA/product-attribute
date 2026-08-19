Configuration
-------------

1. Enable *Sales → Configuration → Settings → Units of Measure & Packagings*.
2. Open a product and add the packagings it is sold in
   (*Sales* tab, *Packagings*).

Defining a rule per packaging
-----------------------------

1. Go to *Sales → Products → Pricelists* and open a pricelist.
2. Add a price rule applied on a single product.
3. Set the *Packaging* field to one of the product's packagings, and the
   *Min. Quantity* in that same packaging.

Leaving *Packaging* empty keeps the standard behaviour: the rule applies to any
unit of measure and its *Min. Quantity* is expressed in the product base unit.

You sell Sugar by the kg, so its UoM is kg and the product price is
1000€: you are selling it at 1000€/kg (a bit expensive as sugar goes,
but you can see why).

One customer is asking for 10g but the price you need for 10g is not 10€
(proportional with the price of 0,01kg) but it is 15€.

With this module, you can configure two price rules:

- Packaging *g*, minimum quantity 1 and a surcharge,  
  note that the surcharge is proportional to the original UoM (kg),  
  so in this example the surcharge must be 500€

- Packaging *kg*, minimum quantity 1 and original price

Report
------

Select the products, then *Print → Pricelist*. Products having a rule per
packaging are printed with one price row per packaging.
