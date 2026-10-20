In order to better test and illustrate this module, example CSV files are
provided in the `example` folder to import some variants (you will need the demo
data).

The demo data provides 2 attributes, each with 3 possible values:

- Cut: Short sleeves, Long sleeves, Tanktop
- Embroidery: Cheap, High quality, Average

At the beginning, the product template "T-shirt" declares only one attribute
with two values:

```text
Cut: Short sleeves, Long sleeves
```

![](static/description/step_1.png)

Its variants are:

1. Cut: Short sleeves
2. Cut: Long sleeves

**First import**

Go to the product variants page and import the first CSV file of the `example`
folder. It creates a new "T-shirt" variant: `Cut: Tanktop, Embroidery: Cheap`.

The template "T-shirt" now declares a new attribute and two new values:

```text
Cut: Short sleeves, Long sleeves, Tanktop
Embroidery: Cheap
```

![](static/description/step_2_tmpl.png)

> **Note**: the new "Embroidery" attribute has a single value, so Odoo
> automatically adds "Embroidery: Cheap" to all the existing variants (the two
> original ones included). Indeed, a variant always carries one value per
> attribute line of its template.

The variants are now:

1. Cut: Short sleeves, Embroidery: Cheap
2. Cut: Long sleeves, Embroidery: Cheap
3. Cut: Tanktop, Embroidery: Cheap

**Second import**

Go to the product variants page and import the second CSV file of the `example`
folder. It creates 2 new "T-shirt" variants: `Cut: Short sleeves, Embroidery:
Average`, and `Cut: Long sleeves, Embroidery: High quality`.

The template "T-shirt" now declares 2 attributes, each with 3 possible values:

```text
Cut: Short sleeves, Long sleeves, Tanktop
Embroidery: Cheap, High quality, Average
```

![](static/description/step_3_tmpl.png)

The resulting variants of the template are then:

1. Cut: Short sleeves, Embroidery: Cheap
2. Cut: Long sleeves, Embroidery: Cheap
3. Cut: Tanktop, Embroidery: Cheap
4. Cut: Short sleeves, Embroidery: Average
5. Cut: Long sleeves, Embroidery: High quality

![](static/description/step_3_variant.png)

> **Note**: even if both attributes are configured with
> `Variant Creation: Instantly`, importing variants only creates the imported
> combinations. For example, no `Cut: Tanktop, Embroidery: Average` variant is
> created.
