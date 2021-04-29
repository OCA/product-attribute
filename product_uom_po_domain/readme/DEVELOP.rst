Technically, this module add two new related fields on ``product.template`` model,

* ``uom_category_id``, related to ``uom_id.category_id``
* ``uom_measure_type`` related to ``uom_id.category_id.measure_type``. This second field
  is a technical field that can be used for other modules.
