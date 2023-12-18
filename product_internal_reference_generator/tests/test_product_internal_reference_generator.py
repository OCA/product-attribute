# Copyright 2023 Ooops - Ilyas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import exceptions
from odoo.tests import Form, SavepointCase


class TestProductInternalReferenceGenerator(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductInternalReferenceGenerator, cls).setUpClass()
        attr_model = cls.env["product.attribute"]
        val_model = cls.env["product.attribute.value"]
        pt_model = cls.env["product.template"]
        cls.group_int_ref = cls.env.ref(
            "product_internal_reference_generator.group_int_ref_template_always_visible"
        )
        cls.pt_seq = cls.env.ref("product_internal_reference_generator.demo_pcs_1")
        cls.attr1 = attr_model.create({"name": "Wheels", "create_variant": "always"})
        cls.attr2 = attr_model.create({"name": "Frame"})
        cls.val1 = val_model.create({"name": "Big", "attribute_id": cls.attr1.id})
        cls.val2 = val_model.create({"name": "Very Big", "attribute_id": cls.attr1.id})
        cls.val3 = val_model.create({"name": "Carbon", "attribute_id": cls.attr2.id})
        cls.val4 = val_model.create({"name": "Magnesium", "attribute_id": cls.attr2.id})
        cls.pt_bicycle = pt_model.create({"name": "Bicycle"})
        cls.pt_car = pt_model.create({"name": "Car"})
        cls.pt_plane = pt_model.create({"name": "Plane"})

    def test_all(self):
        with Form(self.pt_bicycle) as pt:
            pt.int_ref_template_id = self.pt_seq
            pt.save()
            # trigger onchange_int_ref_template_id
            self.assertFalse(pt.variants_prefix, msg="Prefix must be empty.")
            self.pt_bicycle.btn_generate_sequence()
            # default_code must be generated for variant
            self._check_default_code("000", 0, self.pt_bicycle)

        with Form(self.pt_car) as pt_car:
            pt_car.int_ref_template_id = self.pt_seq
            pt_car.save()
            with pt_car.attribute_line_ids.new() as line:
                line.attribute_id = self.attr1
                line.value_ids.add(self.val1)
                line.value_ids.add(self.val2)
            pt_car.save()
            self.pt_car.btn_generate_sequence()
            # default_code must be generated for multiple variants
            self._check_default_code("001", 0, self.pt_car)
            self._check_default_code("002", 1, self.pt_car)

            with pt_car.attribute_line_ids.new() as line:
                line.attribute_id = self.attr2
                line.value_ids.add(self.val3)
                line.value_ids.add(self.val4)
            pt_car.save()
            # default_code must be generated after more attributes was added
            self._check_default_code("003", 0, self.pt_car)
            self._check_default_code("004", 1, self.pt_car)
            self._check_default_code("005", 2, self.pt_car)
            self._check_default_code("006", 3, self.pt_car)
            # no code if no sequence template
            self.assertFalse(self.pt_plane.get_variant_next_default_code())

    def test_unlink(self):
        self.pt_bicycle.write({"int_ref_template_id": self.pt_seq.id})
        with self.assertRaises(exception=exceptions.ValidationError):
            self.pt_seq.unlink()
        products = self.env["product.template"].search(
            [("int_ref_template_id", "=", self.pt_seq.id)]
        )
        products.write({"int_ref_template_id": False})
        self.pt_seq.unlink()

    def _check_default_code(self, sequence_str, ind, pt):
        self.assertIn(
            str(self.pt_seq.sequence_id.number_next_actual - 1) + sequence_str,
            pt.product_variant_ids[ind].default_code,
            msg="Internal reference mismatch.",
        )
