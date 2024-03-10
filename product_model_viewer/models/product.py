from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    gltf_3d_model = fields.Binary(
        "3D model", attachment=True, help="Load a model in GLTF 2.0 format"
    )


class Product(models.Model):
    _inherit = "product.product"
    gltf_3d_model_variant = fields.Binary(
        "Variant 3D model",
        attachment=True,
        help="This field holds the 3D model used for the product variant.",
    )
    gltf_3d_model = fields.Binary(
        "3D model",
        compute="_compute_gltf_3d_model",
        inverse="_inverse_set_gltf_3d_model",
        help="3D model of the product variant.",
    )

    @api.depends("gltf_3d_model_variant", "product_tmpl_id.gltf_3d_model")
    def _compute_gltf_3d_model(self):
        for p in self:
            p.gltf_3d_model = p.gltf_3d_model_variant
            if not p.gltf_3d_model:
                self.gltf_3d_model = self.product_tmpl_id.gltf_3d_model

    def _inverse_set_gltf_3d_model(self):
        for p in self:
            if p.product_tmpl_id.gltf_3d_model and p.product_variant_count > 1:
                p.gltf_3d_model_variant = p.gltf_3d_model
            else:
                p.product_tmpl_id.gltf_3d_model = p.gltf_3d_model
                p.gltf_3d_model_variant = False
