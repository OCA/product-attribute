This module allows to link product attributes to models and populate attribute values from the model records and vice versa.

When a record is created in a model that is linked to an attribute new attribute value will be created automatically.

When a record that is linked to an attribute value is deleted linked attribute value will be deleted if it is not used or archived otherwise.

If a related record field value linked to an attribute value is updated the attribute value name is updated accordingly.

If a module that implements a model linked to attribute(s) is uninstalled all the linked attribute values remain in place.