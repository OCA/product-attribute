import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_package_warning_ui_display", {
    steps: () => [
        {
            trigger: ".o_form_view",
            content: "Wait for picking form to load",
        },
        {
            // UC15: Package Type Validation Guidance
            // The warning should be displayed when product weight exceeds package max_weight
            // Look for alert-warning banner on the picking form
            trigger: ".o_form_view .alert-warning:contains('Weight')",
            content:
                "Check if package compatibility warning banner is displayed on picking form",
        },
    ],
});
