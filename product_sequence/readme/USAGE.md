To specify a different sequence for a product category proceed as
follows:

1.  Go to the a Product Category form view. (**note:** you will need to
    install Inventory app to be able to access to the form view,
    *Inventory \> Configuration \> Products \> Products Categories*; or
    create a menuitem manually).
2.  Fill the *Prefix for Product Internal Reference* as desired.
3.  Under the settings (Settings -\> General Settings -\> Product
    Sequences), you can specify whether the prefix of the parent
    category should be used if no prefix has been specified for the
    category.

Duplicating a product gives the copy its own new reference, drawn from the
sequence of its category, just like any other new product. Odoo already
appends *(copy)* to the name, which is what tells the two apart.

When the module is installed on a database with demo data, a few product
categories (*Lamps*, *Desk Lamps* and *Furniture*) and products are
created to illustrate the three cases: a category with its own prefix, a
category inheriting the prefix of its parent, and a product without
category falling back on the default product sequence.
