# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestCommon(common.SingleTransactionCase):
    # pylint: disable=too-many-instance-attributes
    post_install = True

    def setUp(self):
        """Create common objects for tab tests."""
        # pylint: disable=invalid-name
        super(TestCommon, self).setUp()
        self.tab_model = self.env['product.tab']
        self.type_model = self.env['product.relation.type']
        self.product_model = self.env['product.template']
        self.relation_model = self.env['product.relation']
        # Categories.
        self.category_machine = self.env.ref(
            'product_multi_relation_tabs.category_machine')
        self.category_installation_service = self.env.ref(
            'product_multi_relation_tabs.category_installation_service')
        self.category_spare = self.env.ref(
            'product_multi_relation_tabs.category_spare')
        # Tabs.
        self.tab_supporting_services = self.env.ref(
            'product_multi_relation_tabs.tab_supporting_services')
        self.tab_installation_services = self.env.ref(
            'product_multi_relation_tabs.tab_installation_services')
        self.tab_supported_machines = self.env.ref(
            'product_multi_relation_tabs.tab_supported_machines')
        self.tab_spares = self.env.ref(
            'product_multi_relation_tabs.tab_spares')
        # Types.
        self.type_chairperson = self.env.ref(
            'product_multi_relation_tabs'
            '.relation_type_machine_supported_by_service')
        self.type_machine_is_installed_using = self.env.ref(
            'product_multi_relation_tabs'
            '.relation_type_machine_is_installed_using_service')
        # Products.
        self.product_machine = self.env.ref(
            'product_multi_relation_tabs.product_machine')
        self.product_basic_is = self.env.ref(
            'product_multi_relation_tabs.product_basic_is')
        self.product_premius_ss = self.env.ref(
            'product_multi_relation_tabs.product_premius_ss')
        # Relations.
        self.relation_m1_bis = self.env.ref(
            'product_multi_relation_tabs.relation_m1_bis')
