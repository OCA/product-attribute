This module allows users to efficiently merge multiple product templates into one.
This merge process ensures that attributes and variants from all selected products
are consolidated into the primary product template, without creating any new variants.
This approach is particularly important for maintaining data integrity and 
avoiding unnecessary database load.

By not creating new variants during the merge, the module helps to prevent 
heavy updates on existing tables, making it ideal for large-scale databases.
