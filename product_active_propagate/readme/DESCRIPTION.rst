This module extends the functionnaly of Odoo Product module.

By default, in Odoo,
- when a user disable a template, it will disable the related variants.
- when a user enable a template, it will enable the related variants.

But if a user disables all the variants of a template, the related template
will still remain active, what doesn't make sense in many case,
and which will force the user to disable the template as well,
to avoid seeing the obsolete template.

This module avoids having inconsistent states between the active field of the varinats
and the active field of the template.

Once installed:

- if a user disables a variant, it will disable the template, if all the variants
  are disabled.

- if a user enables a variant, it will enable the template.
