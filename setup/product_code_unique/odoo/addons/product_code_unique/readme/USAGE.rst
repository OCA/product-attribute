* Unable to save a product when a new internal reference or default_code value is
  the same with an existing record.
* A pre_init_hook process is initiated when there exist records without an internal reference(default_code).
  A default value is generated to populate empty field as a temporary value.
