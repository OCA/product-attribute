# Product State Control: Sale & Purchase

## Configuration
To configure this module:

1. Go to **Sales > Configuration > Products > Product States**.
2. Create or edit a product state.
3. You will find two new checkboxes:
   - **Authorized to be sold**: Allow products in this state to be validated in Sales Orders.
   - **Authorized to be bought**: Allow products in this state to be validated in Purchase Orders.

### Default settings
- **R & D / Draft**: Both unchecked
- **Normal**: Both checked
- **Obsolete**: Authorized to be bought checked, Authorized to be sold unchecked
- **Archived**: Both unchecked

## Usage

### Sales Order Validation
- When confirming a Sales Order, the system checks all products.
- If any product has **Authorized to be sold** unchecked, confirmation is blocked.
- Error message:
  - EN: "The status of one of the products prevents order validation. Please change the product status or request a user with the necessary permissions."
  - FR: "L'état d'un des produits ne permet pas de procéder à la validation de la commande. Veuillez changer l'état du produit ou demander à un utilisateur ayant les droits de le faire."

### Purchase Order Validation
- When confirming a Purchase Order, the system checks all products.
- If any product has **Authorized to be bought** unchecked, confirmation is blocked.
- Error message:
  - EN: "The status of one of the products prevents order validation. Please change the product status or request a user with the necessary permissions."
  - FR: "L'état d'un des produits ne permet pas de procéder à la validation de la commande. Veuillez changer l'état du produit ou demander à un utilisateur ayant les droits de le faire."

## Changelog
**18.0.1.0.0** – First official version, extending `product_state`.

## Bug Tracker
Tracked on [GitHub Issues](https://github.com/OCA/product-attribute/issues).

## Maintainers
This module is maintained by the Odoo Community Association (OCA).  
Contributions are welcome: [OCA Contribute](https://odoo-community.org/page/contribute)