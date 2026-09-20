Create attribute values from another Odoo application ("a model").

This module allows to link product attributes to models and populate attribute values from the model records and vice versa. If a model is linked to an attribute :

- creating a record in the model will create a new corresponding attribute value,
- deleting a record in the model will archive or delete the corresponding attribute value depending of it's used or not,
- updating a record in the model will update the attribute value name,
- if the model is deleted (the app is uninstalled), all the linked attribute values remain in place.
