odoo.define("ooops_dimensions_core.constants", function () {
    "use strict";
    var constants = {};
    constants.STANDART_TIMEOUT = 10000;
    constants.WAITING_ELEMENT_TIMEOUT = 1000;
    constants.KEY = "krZQySYrem";
    constants.setWaitingTimeout = function (instructions_list) {
        var final_test_array = [];
        for (let i = 0; i < instructions_list.length; i++) {
            var test_object = instructions_list[i];
            if ("setWaitingTimeout" in test_object) {
                const WAITING_ELEMENT_TIMEOUT = test_object.setWaitingTimeout;
                const selector = test_object.selector ? test_object.selector : "body";
                final_test_array.push(
                    ...[
                        {
                            trigger: selector,
                            is_modal: false,
                            run: function () {
                                console.log("selector", selector);
                                setTimeout(function () {
                                    $(selector).append(`<p>${constants.KEY}</p>`);
                                }, WAITING_ELEMENT_TIMEOUT);
                            },
                            timeout: constants.STANDART_TIMEOUT,
                        },
                        {
                            trigger: `p:contains(${constants.KEY})`,
                            is_modal: false,
                            run: function () {
                                this.$anchor.remove();
                            },
                            timeout: constants.STANDART_TIMEOUT,
                        },
                    ]
                );
            } else {
                final_test_array.push(test_object);
            }
        }
        return final_test_array;
    };
    return constants;
});
