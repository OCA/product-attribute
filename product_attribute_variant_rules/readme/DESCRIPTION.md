This module lets you write rules on a product template to control which
variants are generated from its attributes.

Each rule is made of:

- **preconditions:** attribute values that must be matched for the rule to
  apply. An empty precondition means the rule always applies.
- **type:** "Only With" keeps the combinations matching the postconditions,
  "Never With" removes them.
- **postconditions:** values the combination must (or must not) contain.

In preconditions and postconditions, values of the same attribute are
**ORed** while values of different attributes are **ANDed**.
