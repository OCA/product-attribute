- **Auto-populate stub rules for unknown HS codes + assignee
  activity.** When the matcher receives an HS code it can't
  resolve, optionally create a draft rule (empty
  ``category_id``, ``sequence=999``) and spawn a ``mail.activity``
  on a configurable responsible group / user — surfacing the
  gap in someone's "to-categorise" inbox instead of leaving it
  in the matcher's INFO log only.

  Off by default. Toggle via ``res.config.settings`` Boolean
  (system parameter
  ``product_category_hs_mapping.auto_create_unknown``) so the
  feature is opt-in per-database. Auto-creation is idempotent
  on (``hs_code_pattern``, ``company_id``, ``category_id IS NULL``):
  one stub per unknown code, no duplicates on subsequent
  imports.

  **Multi-company nuance**: in a multi-company environment
  different people / groups may be responsible for the
  category mapping per company (a product manager for the
  industrial entity, a procurement lead for the agri entity,
  etc). The activity-assignee target is therefore PER company,
  not a single global group. Concrete shape: a Many2one
  ``hs_mapping_responsible_user_id`` (or group) on
  ``res.company`` with a fallback chain — company-level
  setting → global system parameter
  ``product_category_hs_mapping.responsible_group_xmlid`` →
  log+skip if neither is set.

  When the responsible user fills ``category_id`` on the stub,
  the activity auto-marks Done (``mail.activity._action_done``
  hook). The chatter on the rule shows *which* product
  triggered the stub creation so the assignee can sanity-check
  the proposed category against a real example.

  Not implemented yet — pending real demand. The manual
  ``Apply HS Code → Category Mapping`` server action covers
  the buyer-driven re-categorise flow today.

- **Per-line / variant override**. ``product.product`` doesn't
  inherit ``hs_code`` separately, so the manual server action
  is currently bound to ``product.template``. If a customer
  ever ships variants with different tariff codes (rare in
  OEM-parts catalogues but conceivable for raw-material
  multipacks), surface the action on ``product.product`` too
  with a per-variant ``hs_code`` field.

- **Bulk re-categorisation cron / queued-job**. When the
  upstream HS mapping table changes (e.g. a new EU tariff
  line), a buyer may want to re-run the matcher across the
  entire product catalogue. Today they can multi-select in
  the product list and trigger the existing action — but for
  thousands of products that's a single heavy transaction.
  A cron-driven or ``queue_job``-backed variant with progress
  feedback would be more operator-friendly.
