1. Open the product template and go to the *Attributes & Variants* tab.
2. Tick **Use Attribute Rules**.
3. Add your rules (preconditions are optional) and choose their type.
4. Save the product: the variants are generated again according to the rules.

A rule like:

> "All products with blue or green color in XL size will appear only with
> a V neck collar and a short sleeve."

is written as:

```text
Preconditions: (color: blue), (color: green), (size: XL)
Type: Only With
Postconditions: (collar: V neck), (sleeve: short)
```

When the preconditions are empty the rule always applies. To only keep the
variants with a short sleeve:

```text
Preconditions: (none)
Type: Only With
Postconditions: (sleeve: short)
```

To remove all the variants with a sailor collar:

```text
Preconditions: (none)
Type: Never With
Postconditions: (collar: sailor)
```

When several rules are defined, they are ANDed together.
