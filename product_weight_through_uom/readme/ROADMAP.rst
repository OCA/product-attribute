* There's an incompatibility with the module `delivery` because of the way this
  one computes the `stock.quant.package` and `stock.picking` weight based on
  unit conversion multiplied by product weight.

  E. g.: A product with a UoM of Tons will have a weight of 1000 Kg. `delivery`
  computes it this way for every quant package or picking line:

  - Converts the product Uom (Tons) to the line Uom (e.g.: Kg.) = 1000
  - Multiplies it by the line quantity (e.g.: 5) = 5000
  - Then multiplies it by the product weight = 50000

  This would be a correct compute if the UoM wouldn't be a weight measure
  itself.
