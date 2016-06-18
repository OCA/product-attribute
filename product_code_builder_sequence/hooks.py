# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# © 2015 Domatix (http://domatix.com)
# Angel Moua <angel.moya@domatix.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def pre_init_hook(cr):
    """
    Updates existing codes matching the default '/' or
    empty. Primarily this ensures installation does not
    fail for demo data.
    :param cr: database cursor
    :return: void
    """
    cr.execute("UPDATE product_template "
               "SET prefix_code = '!!mig!!' || id "
               "WHERE prefix_code IS NULL OR prefix_code = '/'")
