Go to the "Inventory/Configuration/Products/Attributes" menu and select an existing or create a new attribute.

Following configuration fields are available:

- Linked Model. Model which records will be used for the attribute values. Cannot be a transient model. Warning: changing or removing existing value will not affect existing attribute values!

- Linked Field. Field of the selected model that will be used for the attribute value names. Can be any field except for related or computed non-stored ones. Digital field values will be converted to Char automatically. Warning: changing or removing existing value will not affect existing attribute values!

- Domain (optional). If configured only records matching the domain will be used for attribute value creation. Warning: updating domain will not affect existing attribute values!

- Add to Products on Create. If enabled when a new attribute value is created it will be automatically added to all existing products that use this attribute. Attention! You must completely understand possible consequences and use this option with care!

- Create from Attribute Values. If enabled when a new attribute value is added to the attribute a new record will be created in the linked model. Attention! The only value passed explicitly on creation will be the linked field containing the new attribute value name. You must ensure that this would be enough for new record creation. Otherwise an exception will be raised. If a digital field is used a conversion attempt will be done. If conversion fails an exception might be raised.

- Modify from Attribute Values. If enabled when an attribute value is renamed linked field value in the linked model will be updated accordingly. If a digital field is used a conversion attempt will be done. If conversion fails an exception might be raised. This option is available only if "Create from Attribute Values" option is enabled.

- Delete when Attribute Value is Deleted. When enabled if an attribute value is deleted linked record will be deleted too. Use with extreme care! This option is available only if "Create from Attribute Values" option is enabled.



Creating, modifying or deleting related records from attributes requires corresponding access rights to linked model. Otherwise access error will occur.

There is no "Attribute/Model" restriction so you can link several attributes to the same model. You can use same records and fields or apply custom domains to fine tune such mappings.

When adding a model mapping to an attribute with existing values you can map those manually in the attribute value list.