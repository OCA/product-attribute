odoo.define(
    "ooops_dimensions_core.01400_ooops_dimensions_core_tour_test_doc_1_4",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");
        var ajax = require("web.ajax");
        var session = require("web.session");
        var domReady = new Promise(function (resolve) {
            $(resolve);
        });
        var ready = Promise.all([domReady, session.is_bound, ajax.loadXML()]);
        var constants = require("ooops_dimensions_core.constants");

        const FIRST_STEPS = [
            {
                trigger: '.full[data-toggle="dropdown"]',
            },
            {
                trigger: '.o_app[data-menu-xmlid="sale.sale_menu_root"]',
            },
            {
                trigger: ".o_list_button_add",
                extra_trigger: ".o_sale_order",
                position: "bottom",
            },
            {
                trigger: " .o_field_many2one[name='partner_id']",
                extra_trigger: ".o_sale_order",
                run: function (actions) {
                    const TEXT = "Azure Interior";
                    actions.text(TEXT, this.$anchor.find("input"));
                },
                timeout: constants.STANDART_TIMEOUT,
            },
            {
                trigger: " .ui-state-active",
                timeout: constants.STANDART_TIMEOUT,
            },
        ];

        const listOfAllTests = [
            FIRST_STEPS,
            require("ooops_dimensions_core.01401_ooops_dimensions_core_tour_test_doc_1_4_1"),
            require("ooops_dimensions_core.01402_ooops_dimensions_core_tour_test_doc_1_4_2"),
            require("ooops_dimensions_core.01403_ooops_dimensions_core_tour_test_doc_1_4_3"),
            require("ooops_dimensions_core.01404_ooops_dimensions_core_tour_test_doc_1_4_4"),
            require("ooops_dimensions_core.01405_ooops_dimensions_core_tour_test_doc_1_4_5"),
            require("ooops_dimensions_core.01406_ooops_dimensions_core_tour_test_doc_1_4_6"),
            require("ooops_dimensions_core.01407_ooops_dimensions_core_tour_test_doc_1_4_7"),
        ];

        const TEST_DOC_1_4 = [];
        for (let i = 0; i < listOfAllTests.length; i++) {
            var test_object = listOfAllTests[i];
            if (!Array.isArray(test_object)) {
                var test_array = constants.setWaitingTimeout(test_object.test_array);
                TEST_DOC_1_4.push(...test_array);
            } else if (Array.isArray(test_object)) {
                test_object = constants.setWaitingTimeout(test_object);
                TEST_DOC_1_4.push(...test_object);
            }
        }

        function download(filename, text) {
            var element = document.createElement("a");
            element.setAttribute(
                "href",
                "data:text/plain;charset=utf-8," + encodeURIComponent(text)
            );
            element.setAttribute("download", filename);

            element.style.display = "none";
            document.body.appendChild(element);

            element.click();

            document.body.removeChild(element);
        }
        var report_text = "";
        TEST_DOC_1_4.push({
            trigger: ".o_menu_apps a",
            run: function () {
                for (let k = 0; k < listOfAllTests.length; k++) {
                    var test_data = listOfAllTests[k];

                    if (!Array.isArray(test_data)) {
                        report_text += `========${test_data.test_name}=========\n`;
                        for (var key in test_data) {
                            if (key !== "test_array") {
                                report_text += `${key} - ${test_data[key]}\n`;
                                console.log(key, test_data[key]);
                            }
                        }
                    }
                }
                download("report.txt", report_text);
            },
        });
        tour.register(
            "01401_ooops_dimensions_core_tour_test_doc_1_4",
            {
                url: "/web",
                wait_for: ready,
                rainbowManMessage: "Congrats, best of luck catching such big fish! :)",
            },
            TEST_DOC_1_4
        );

        return TEST_DOC_1_4;
    }
);
