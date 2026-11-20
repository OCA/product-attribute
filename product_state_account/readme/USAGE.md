To prevent products of a state from being invoiced:

1.  Open the product state. With `product_state_sale` installed, states are
    listed under *Sales \> Configuration \> Products \> Product States*.
2.  Untick *Can Be Invoiced*.
3.  Products in this state no longer appear in the product selection of
    customer invoices, credit notes and receipts, and cannot be set on
    invoice lines. This also applies to invoices generated from sales
    orders. Vendor bills are not restricted. Existing invoice lines are
    not modified.

![Product state form with the Can Be Invoiced toggle](readme/static/description/product_state_form.png)

The flag is enabled by default, so existing states keep their behaviour
until you change them. The list view shows the flag for all states:

![Product state list with the Can Be Invoiced column](readme/static/description/product_state_list.png)

Editing states requires the *Product State Manager* group.
