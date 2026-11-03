Users in the *Product Manager* group can:

1. Open an attribute and press **Duplicates**. Values showing the same name in one of
   the languages of **Compare Names In** are grouped (case and spaces ignored). By
   default these are the languages of the internal users: translations nobody reviews
   can give two different values the same name. Tick **Ignore Accents and
   Punctuation** to also group names such as "2/3kg" and "2-3 kg", and **Search Again**.
2. Press **Merge** on a group, on the merge button of a value in the attribute form, or
   select values in a list of attribute values (core has no such list: a module such
   as `product_attribute_value_menu` adds it) and use *Action > Merge*.
3. In the wizard, check the usage of each value, choose the **Value to Keep** and review
   its name in each language. Rows in orange are languages where the values show
   different names.
4. Press **Merge**. The merge record opens with the moved records; its **Undo** button
   reverts the merge.

When a product has the kept value and a merged one on the same attribute line, the
merged value is not merged on that product and stays active: rename it so both can be
told apart, or remove one of them from the product. A merged value that the product
only keeps on archived variants is merged as usual.

Undo restores the merged values as they were: a value that was archived before the
merge stays archived.

The merges of an attribute are listed from the **Merges** button of its form.
