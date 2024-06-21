# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from base64 import b64encode
from os import path

from freezegun import freeze_time

from odoo import Command, fields
from odoo.tests.common import TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class TestProductSupplierinfoImportByBarcodeCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.import_template_1 = cls.env["product.supplierinfo.import.template"].create(
            {
                "name": "Spanish Drinks S.A.",
                "barcode_header_name": "bar code",
                "template_line_ids": [
                    Command.create(
                        {
                            "header_name": "Product name",
                            "field_id": cls.env.ref(
                                "product.field_product_supplierinfo__product_name"
                            ).id,
                        }
                    ),
                    Command.create(
                        {
                            "header_name": "min qty",
                            "field_id": cls.env.ref(
                                "product.field_product_supplierinfo__min_qty"
                            ).id,
                        }
                    ),
                    Command.create(
                        {
                            "header_name": "price",
                            "field_id": cls.env.ref(
                                "product.field_product_supplierinfo__price"
                            ).id,
                        }
                    ),
                    Command.create(
                        {
                            "header_name": "from",
                        }
                    ),
                ],
            }
        )
        cls.import_template_2 = cls.env["product.supplierinfo.import.template"].create(
            {
                "name": "Olé Drinks S.A.",
                "barcode_header_name": "EAN",
                "header_offset": 1,
                "template_line_ids": [
                    Command.create(
                        {
                            "header_name": "Description",
                            "field_id": cls.env.ref(
                                "product.field_product_supplierinfo__product_name"
                            ).id,
                        }
                    ),
                    Command.create({"header_name": "Ref"}),
                    Command.create({"header_name": "Price"}),
                    Command.create({"header_name": "Disc\n%"}),
                    Command.create({"header_name": "Prom\n%"}),
                    Command.create(
                        {
                            "header_name": "Final",
                            "field_id": cls.env.ref(
                                "product.field_product_supplierinfo__price"
                            ).id,
                        }
                    ),
                ],
            }
        )
        cls.supplier_1 = cls.env["res.partner"].create(
            {
                "name": "Spanish Drinks S.A.",
                "supplier_rank": 1,
            }
        )
        cls.supplier_2 = cls.env["res.partner"].create(
            {
                "name": "Olé Drinks S.A.",
                "supplier_rank": 1,
            }
        )
        cls.prod_horchata = cls.env["product.product"].create(
            {
                "name": "Horchata",
                "barcode": "000001",
            }
        )
        cls.product_salmorejo = cls.env["product.product"].create(
            {
                "name": "Salmorejo",
                "barcode": "000003",
                "seller_ids": [
                    Command.create(
                        {
                            "partner_id": cls.supplier_1.id,
                            "date_start": "2024-01-01",
                            "min_qty": 1,
                            "price": 1.33,
                        }
                    )
                ],
            }
        )
        cls.salorejo_initial_supplierinfo = cls.product_salmorejo.seller_ids

    def _data_file(self, filename, encoding=None):
        """Helper: load the excel file binary"""
        mode = "rt" if encoding else "rb"
        with open(path.join(path.dirname(__file__), filename), mode) as file:
            data = file.read()
            if encoding:
                data = data.encode(encoding)
            return b64encode(data)

    def _import_supplierinfo_file(
        self, file_path, supplier, date_start, delay=0, create_new_products=True
    ):
        """ "Helper: import an excel file for testing"""
        data = self._data_file(file_path)
        wiz = self.env["product.supplierinfo.import"].create(
            {
                "supplierinfo_filename": file_path,
                "supplierinfo_file": data,
                "supplier_id": supplier.id,
                "date_start": date_start,
                "delay": delay,
                "create_new_products": create_new_products,
            }
        )
        return wiz

    def _check_supplierinfo_values(self, supplierinfo_dict):
        for supplierinfo, values in supplierinfo_dict.items():
            for field, value in values.items():
                if isinstance(value, float):
                    self.assertAlmostEqual(supplierinfo[field], value)
                else:
                    self.assertEqual(supplierinfo[field], value)


class TestProductSupplierinfoImportByBarcode(
    TestProductSupplierinfoImportByBarcodeCommon
):
    @freeze_time("2024-07-01")
    def test_simple_import(self):
        # 1. Import the test case file
        self._import_supplierinfo_file(
            "test_supplier_spanish_drinks.xlsx",
            self.supplier_1,
            fields.Date.today(),
        ).action_import_file()
        # 2. Check that the vendor pricelists are correctly imported
        # 2.1 Horchata had two entries for a different min_qty each
        self._check_supplierinfo_values(
            {
                self.prod_horchata.seller_ids.filtered(lambda x: x.min_qty == 1): {
                    "product_name": "Horchata Fufi",
                    "price": 0.7,
                    "date_start": fields.Date.from_string("2024-07-01"),
                },
                self.prod_horchata.seller_ids.filtered(lambda x: x.min_qty == 20): {
                    "product_name": "Horchata Fufi",
                    "price": 0.5,
                    "date_start": fields.Date.from_string("2024-07-01"),
                },
            }
        )
        # 2.2 Gazpacho didn't exist and is marked for review
        product_gazpacho = self.env["product.product"].search(
            [("barcode", "=", "000002")]
        )
        self.assertTrue(product_gazpacho.created_from_supplierinfo_import)
        self.assertEqual(product_gazpacho.name, "Gazpacho Almonte")
        self._check_supplierinfo_values(
            {
                product_gazpacho.seller_ids: {
                    "product_name": "Gazpacho Almonte",
                    "price": 1.52,
                    "date_start": fields.Date.from_string("2024-07-01"),
                }
            }
        )
        # 2.3 Salmorejo already had a vendor list, which we'll override
        new_salmorejo_supplierinfo = (
            self.product_salmorejo.seller_ids - self.salorejo_initial_supplierinfo
        )
        self._check_supplierinfo_values(
            {
                self.salorejo_initial_supplierinfo: {
                    "price": 1.33,
                    "date_end": fields.Date.from_string("2024-06-30"),
                },
                new_salmorejo_supplierinfo: {
                    "product_name": "Salmorejo Almonte",
                    "price": 1.37,
                    "date_start": fields.Date.from_string("2024-07-01"),
                },
            }
        )

    @freeze_time("2024-07-01")
    def test_complex_file_import(self):
        """This file has some traps, like header offsets, category rows, repeating
        headers..."""
        # 1. Import the test case file
        self._import_supplierinfo_file(
            "test_supplier_drinks_complex_sheet.xlsx",
            self.supplier_2,
            fields.Date.today(),
        ).action_import_file()
        # 2.1 Check that the vendor pricelists are correctly imported
        self._check_supplierinfo_values(
            {
                self.prod_horchata.seller_ids: {
                    "product_name": "Horch. Fufi",
                    "price": 11.09,
                    "date_start": fields.Date.from_string("2024-07-01"),
                },
            }
        )
        # 2.2 Gazpacho didn't exist and is marked for review
        product_gazpacho = self.env["product.product"].search(
            [("barcode", "=", "000002")]
        )
        self.assertTrue(product_gazpacho.created_from_supplierinfo_import)
        self.assertEqual(product_gazpacho.name, "Gazp. Alm.")
        self._check_supplierinfo_values(
            {
                product_gazpacho.seller_ids: {
                    "product_name": "Gazp. Alm.",
                    "price": 15.29,
                    "date_start": fields.Date.from_string("2024-07-01"),
                }
            }
        )
        # 2.3 Salmorejo already had a vendor list but is from another supplier
        new_salmorejo_supplierinfo = (
            self.product_salmorejo.seller_ids - self.salorejo_initial_supplierinfo
        )
        self._check_supplierinfo_values(
            {
                self.salorejo_initial_supplierinfo: {
                    "price": 1.33,
                    "date_end": False,
                },
                new_salmorejo_supplierinfo: {
                    "product_name": "Salm. Alm.",
                    "price": 6.03,
                    "date_start": fields.Date.from_string("2024-07-01"),
                },
            }
        )
