The approval rules can be configured to suit particular use cases.
A default validation rule is provided out of the box,
that can be used as a starting point fot this configuration.

This configuration is done at
*Settings > Technical > Tier Validations > Tier Definition*.

Note that, since Product start as archived records,
the *Definition Domain* must include ``"|",["active","=",True],["active","=",False]``.
Otherwise the validation rule won't apply correctly in new records.

Setting new Products inactive can be disabled,
by removing the "draft" code from the initial Product State.
