To configure this module, go to **Settings** and locate the **Units of Measure**
section.

## Secondary Unit Price Display

Configure how unit prices and quantities are shown in reports when secondary units are
used.

- **Sales**: Select the display policy for sales order and customer invoice reports and
  portal views.
- **Purchase**: Select the display policy for purchase order and vendor bill reports and
  portal views.

Available options:

- **Primary Unit Price Only**: Show only the primary unit price.
- **Prioritize Secondary Unit Price**: Show the secondary unit price when available,
  otherwise fall back to the primary unit price.
- **Both Primary and Secondary Unit Prices**: Show both primary and secondary unit
  prices.

## Hide Secondary Qty Column

Hide the separate **Second Qty** column in reports.

- When enabled, the **Second Qty** column is hidden in reports. The
  secondary quantity can still be shown in the main **Qty** column
  depending on the selected price display policy above.
- Apply the setting per document type:
  - **Sales**
  - **Purchase**

These settings are intended to be used by dependency modules (for example,
`purchase_order_secondary_unit` and `account_move_secondary_unit`).