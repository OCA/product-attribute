- Go to Sales -\> Products -\> Pricelists.
- Create a new pricelist and add at least one rule.
- Specify the product template or category for the rule.
- Set the computation mode and save

**Note**: Ensure the minimum quantity is not great than 1 for the rule
to apply effectively.

- Go to Sales -\> Configuration -\> Settings.
- In the Pricing section, select the Pricelist to compute sale price
  created in the previous step.
- Optionally and only with a multi-company environment enabled, set the
  Main company for compute sale price to restrict the computation to a
  specific company.
- Save the configuration

The module creates a cron job to update the product list price every
day. The cron job is disabled by default. To enable it, go to Settings
-\> Technical -\> Automation -\> Scheduled Actions and search for
Product sale price: Update price from pricelist.
