This module lets you configure a **stock reservation lead time (in days) per
product category**, so that each type of product can be reserved with the
anticipation it actually needs instead of a single global value.

Key features:

* A reservation lead time rule per **product category** and **company**.
* Rules are resolved **up the category hierarchy**: a category without its own
  rule inherits the one of its closest ancestor.
* A configurable **global default** (15 days) per company, used when neither the
  category nor any of its ancestors has a rule.
* A lead time of **0 days** is valid (reserve only on the delivery date); the
  existence of the rule is the discriminator, so 0 is never confused with
  "not configured".

This module only provides the configuration surface. The engine that reserves
and releases stock based on these lead times is provided by a separate module.
