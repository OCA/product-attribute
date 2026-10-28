# Copyright 2004 Tiny SPRL
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def pre_init_hook(env):
    """
    Updates existing codes matching the default '/' or
    empty. Primarily this ensures installation does not
    fail for demo data.
    :param cr: database cursor
    :return: void
    """
    env.cr.execute(
        "UPDATE product_product "
        "SET default_code = '!!mig!!' || id "
        "WHERE default_code IS NULL OR default_code = '/';"
    )
