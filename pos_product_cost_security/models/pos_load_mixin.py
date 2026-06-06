from odoo import api, models


class PosLoadMixin(models.AbstractModel):
    _inherit = "pos.load.mixin"

    @api.model
    def with_user(self, user):
        ctx = dict(self.env.context)
        ctx["pos_override_cost_security"] = True
        return super().with_user(user).with_context(**ctx)

    def with_env(self, env):
        ctx = dict(env.context)
        ctx["pos_override_cost_security"] = True
        return super().with_env(env(context=ctx))
