This module allows changing the standard expiry dates managing.
Currently, the odoo product_expiry modules compute the use_date, removal_date, life_date, and alert_date applying the use_time, removal_time, life_date, and alert_date to the creation date of the lot. For example, if alert_time is set to 2 days and the lot is created the 16/02/2022, the alert_date is set to 18/02/2022.
With this module, this behavior can be changed. It computes the use_date, removal_date, and alert_date depending on the life_date. For example, if the alert_time is set to 2 days, and the lot life_date is 20/04/2022, the alert_date is set to 18/04/22.
In addition, the times and type of computing (from current_date or life_date) can be configured on the product_category and on the product_template. If a field is provided on the product, the provided on the category is set.
Filters of "Alert Date Reached", "Use Date Reached", "Life Date Reached" and "Removal Date Reached" have been added.
Finally, crons that generate activities have been created to warn for each date. By default, they are desastivated.
