In order to better test and illustrate this module, and example CSV file is provided in the exmaple folder (you will need the demo data).

First, the setup:

* We have a product attribute named "Cut" which has 3 possible values: "Short sleeved", "Long sleeved", "Tanktop"

* We have a product attribute named "Embroidery" which has 3 possible values: "Cheap", "High quality", "Average"

Next, for our example:

* Install this module and the purchase or sale module so that you have product menus

* Observe on product template "T-shirt" the attribute lines and possible values. We have:

    Cut: Short-sleeved, Long-sleeved

.. figure:: static/description/step_1.png
   :width: 600 px

* Go to product variants page, import the provided CSV file in the "examples" folder

  This will create a new T-shirt variant with the attributes:
    Cut: Tanktop; Embroidery: Cheap

.. figure:: static/description/step_2_variant.png
   :width: 600 px

* Observe on product template "T-shirt" the attribute lines and possible values.
  Because imported the variant with new attributes, we now have:

  Cut: Short-sleeved, Long-sleeved, Tanktop

  Embroidery: Cheap

.. figure:: static/description/step_2_tmpl.png
   :width: 600 px

Thus we have synced product variant attributes -> product template attributes.

Let's continue:

* Go to product variants page, import the 2nd provided CSV file in the "examples" folder

  This will create 2 new T-shirt variants as follows:

    Cut: Short-sleeved; Embroidery: Average

    Cut: Long-sleeved; Embroidery: High quality

.. figure:: static/description/step_3_variant.png
   :width: 600 px

* Observe on product template "T-shirt" the attribute lines and possible values.
  Because we imported the new attributes, we now have:

    Cut: Short-sleeved, Long-sleeved, Tanktop

    Embroidery: Cheap, Average, High Quality

.. figure:: static/description/step_3_tmpl.png
   :width: 600 px

* Because this module prevents creating all the possible variants to prevent exponential growth of variants, we only have the following variants that we imported according to the following matrix:

| (Attribute combination) | Cheap | High quality | Average |
| ----------------------- | ----- | ------------ | ------- |
| Short sleeve | No | No | Yes |
| Long sleeve | No | Yes | No |
| Tanktop | Yes | No | No |
