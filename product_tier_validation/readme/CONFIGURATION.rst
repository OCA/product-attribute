The approval rules can be configured to suit particular use cases.
A default validation rule is provided out of the box,
that can be used as a starting point fot this configuration.

This configuration is done at
*Settings > Technical > Tier Validations > Tier Definition*.

Note: This module is incompatible with product_status.
Since tier validations use the state field and the product_status module needs
specific states/stages, tier validations will not trigger if that module is installed.
