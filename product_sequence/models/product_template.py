from odoo import models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_apply_new_code(self):
      categ_id = self.categ_id
      sequence = self.env["ir.sequence"].get_category_sequence_id(categ_id)
      is_seq_curr_categ = self.default_code.startswith(sequence.prefix)
      if not is_seq_curr_categ:
          ref = sequence.next_by_id()
          self.default_code = ref
          