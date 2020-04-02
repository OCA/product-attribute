from odoo.tests.common import TransactionCase


class TestProductToScaleBizerba(TransactionCase):

    def test_create_scale_system_001(self):
        vals_system = {
            'name': 'Bizerba Test System',
            'csv_relative_path': '/bizerba_test1/IMPORT/',
            'product_image_relative_path': '/bizerba_test1/IMAGE_IMPORT/',
            'external_text_file_pattern': 'TEXT_MAG_TEST_0000_%Y%m%d_%H%M%S.CSV',
            'product_text_file_pattern': 'ARTI_MAG_TEST_0000_%Y%m%d_%H%M%S.CSV',
        }
        scale_system_id = self.env['product.scale.system'].create(vals_system)
        vals_sys_line = {
            'scale_system_id': scale_system_id.id,
            'code': 'TESTABNR',
            'name': 'Bizerba Shelf Test ID',
            'sequence': 1,
            'type': 'many2one',
            'field_id': self.env.ref(
                'product_to_scale_bizerba.field_product_product__scale_group_id'
            ).id,
            'related_field_id': self.env.ref(
                'product_to_scale_bizerba.field_product_scale_group__external_identity'
            ).id,
            'delimiter': '#',
        }
        self.env['product.scale.system.product.line'].create(vals_sys_line)
        vals_group = {
            'name': 'Test Group',
            'scale_system_id': scale_system_id.id,
            'external_identity': 1,
        }
        group_id = self.env['product.scale.group'].create(vals_group)
        vals_product = {
            'name': 'Apple Test (Gala, small)',
            'list_price': 2.05,
            'barcode': 2341321000001,
            'uom_id':  self.env.ref('uom.product_uom_kgm').id,
            'uom_po_id': self.env.ref('uom.product_uom_kgm').id,
            'scale_group_id': group_id.id,
            'scale_tare_weight': 0.015,
            'scale_sequence': 1,
        }
        product_id = self.env['product.product'].create(vals_product)
        scale_log_count = self.env['product.scale.log'].search_count(
            [
                ('product_id', '=', product_id.id),
                ('scale_system_id', '=', scale_system_id.id)
            ]
        )
        self.assertEquals(scale_log_count, 1, 'Scale Log should create')
