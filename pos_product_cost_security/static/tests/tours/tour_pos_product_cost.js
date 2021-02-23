odoo.define("pos_product_cost_security.tour.pos_product_cost", function (require) {
    "use strict";

    var Tour = require("web_tour.tour");

    // We just want to load the data to test that there aren't errors due to rpc calls
    var steps = [
        {
            content: "waiting for loading to finish",
            trigger: "body:not(:has(.loader))",
        },
    ];

    Tour.register("pos_product_cost", {test: true, url: "/pos/ui"}, steps);
});
