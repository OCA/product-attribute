odoo.define(
    "ooops_dimensions_core.01200_ooops_dimensions_core_tour_test_doc_1_2",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");
        var ajax = require("web.ajax");
        var session = require("web.session");
        var domReady = new Promise(function (resolve) {
            $(resolve);
        });
        var ready = Promise.all([domReady, session.is_bound, ajax.loadXML()]);
        var STANDART_TIMEOUT = require("ooops_dimensions_core.constants")
            .STANDART_TIMEOUT;
        var TEST_DOC_1_2_1 = require("ooops_dimensions_core.01201_ooops_dimensions_core_tour_test_doc_1_2_1");
        var TEST_DOC_1_2_2 = require("ooops_dimensions_core.01202_ooops_dimensions_core_tour_test_doc_1_2_2");
        var TEST_DOC_1_2_3 = require("ooops_dimensions_core.01203_ooops_dimensions_core_tour_test_doc_1_2_3");
        var TEST_DOC_1_2_4 = require("ooops_dimensions_core.01204_ooops_dimensions_core_tour_test_doc_1_2_4");
        var TEST_DOC_1_2_5 = require("ooops_dimensions_core.01205_ooops_dimensions_core_tour_test_doc_1_2_5");
        var TEST_DOC_1_2_6 = require("ooops_dimensions_core.01206_ooops_dimensions_core_tour_test_doc_1_2_6");
        var TEST_DOC_1_2_7 = require("ooops_dimensions_core.01207_ooops_dimensions_core_tour_test_doc_1_2_7");
        var TEST_DOC_1_2_8 = require("ooops_dimensions_core.01208_ooops_dimensions_core_tour_test_doc_1_2_8");
        var TEST_DOC_1_2_9 = require("ooops_dimensions_core.01209_ooops_dimensions_core_tour_test_doc_1_2_9");
        var TEST_DOC_1_2_10 = require("ooops_dimensions_core.01210_ooops_dimensions_core_tour_test_doc_1_2_10");
        var TEST_DOC_1_2_11 = require("ooops_dimensions_core.01211_ooops_dimensions_core_tour_test_doc_1_2_11");
        var TEST_DOC_1_2_12 = require("ooops_dimensions_core.01212_ooops_dimensions_core_tour_test_doc_1_2_12");
        var TEST_DOC_1_2_13 = require("ooops_dimensions_core.01213_ooops_dimensions_core_tour_test_doc_1_2_13");
        const FIRST_STEPS = [
            // Tour.STEPS.SHOW_APPS_MENU_ITEM,
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
                timeout: STANDART_TIMEOUT,
            },
            {
                trigger: " .ui-state-active",
                timeout: STANDART_TIMEOUT,
            },
        ];

        const listOfAllTests = [
            FIRST_STEPS,
            TEST_DOC_1_2_1,
            TEST_DOC_1_2_2,
            TEST_DOC_1_2_3,
            TEST_DOC_1_2_4,
            TEST_DOC_1_2_5,
            TEST_DOC_1_2_6,
            TEST_DOC_1_2_7,
            TEST_DOC_1_2_8,
            TEST_DOC_1_2_9,
            TEST_DOC_1_2_10,
            TEST_DOC_1_2_11,
            TEST_DOC_1_2_12,
            TEST_DOC_1_2_13,
        ];
        const TEST_DOC_1_2 = [];
        for (let i = 0; i < listOfAllTests.length; i++) {
            var test_object = listOfAllTests[i];
            if (!Array.isArray(test_object)) {
                TEST_DOC_1_2.push(...test_object.test_array);
            } else if (Array.isArray(test_object)) {
                TEST_DOC_1_2.push(...test_object);
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
        TEST_DOC_1_2.push({
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
            "0010_ooops_dimensions_core_tour_test_doc_1_2",
            {
                url: "/web",
                wait_for: ready,
                rainbowManMessage: "Congrats, best of luck catching such big fish! :)",
            },
            TEST_DOC_1_2
        );

        return TEST_DOC_1_2;
    }
);
