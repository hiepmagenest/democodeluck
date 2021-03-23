odoo.define('bus.call.trigger', function (require) {
    "use strict";
    var core = require('web.core');
    var WebClient = require('web.WebClient');
    var session = require('web.session');
    var Widget = require('web.Widget');
    // var CallEffect = require('web.call.effect');
    var super_self = this;
    var _t = core._t;
    // Update Real Time On Same Session Tree View
    WebClient.include({
        init: function (parent, client_options) {
            this._super.apply(this, arguments);
            this.bus_channels = {};
        },
        start: function () {
            var self = this;
            self._reload = _.throttle(self._reload, 1000);
            return $.when(this._super.apply(this, arguments));
        },
        bus_declare_channel: function (channel, method) {
            if (!(channel in this.bus_channels)) {
                this.bus_channels[channel] = method;
                this.call('bus_service', 'addChannel', channel);
            }
        },
        bus_delete_channel: function (channel) {
            this.call('bus_service', 'deleteChannel', channel);
            this.bus_channels = _.omit(this.bus_channels, channel);
        },
        bus_notification: function (notifications) {
            _.each(notifications, function (notification, index) {
                var channel = notification[0];
                var message = notification[1];
                if (channel in this.bus_channels) {
                    this.bus_channels[channel](message);
                }
            }, this);
        },
        destroy: function () {
            _.each(this.bus_channels, function (method, channel) {
                this.bus_delete_channel(channel);
            }, this);
            this.call('bus_service', 'stopPolling');
            this._super.apply(this, arguments);
        },
        show_application: function () {
            this.call('bus_service', 'onNotification', this, this.bus_notification);
            this.call('bus_service', 'startPolling');
            this.bus_declare_channel('show_call_effect_' + (session.uid).toString(), this.show_call_effect.bind(this));
            this.bus_declare_channel('world_sms_trigger_' + (session.uid).toString(), this.world_sms_trigger.bind(this));
            return this._super.apply(this, arguments);
        },
        show_call_effect: function (message) {
            // window.focus();
            var self = this;
            if (session.uid == message.uid) {
                this._trigger(message);
            }
        },
        _trigger: function (message) {
            if (message) {
                // new CallEffect(message).appendTo(this.$el);
                if (session.user_context.lang == 'vi_VN') {
                    var name = "Cuộc gọi";
                    var default_name = "Cuộc gọi từ:";
                } else {
                    var name = 'On Calling';
                    var default_name = 'Calling From:';
                }
                var action = {
                    name: name,
                    type: 'ir.actions.act_window',
                    res_model: 'call.effect',
                    context: {
                        default_name: default_name,
                        default_phone: message.phone,
                        default_customer: message.name,
                        default_description: message.description,
                        default_has_customer: message.customer
                    },
                    views: [[false, 'form']],
                    target: 'new'
                };
                this.do_action(action)
                // window.open();
                // window.focus();
                // $(window).focus();
            }
        },
        // World SMS
        world_sms_trigger: function (message) {
            if (session.user_context.lang == 'vi_VN') {
                var success = "Gửi tin nhắn thành công";
                var fail = "Gửi tin nhắn thất bại,";
            } else {
                var success = 'Send Message Successful';
                var fail = 'Send Message Fail,';
            }
            var self = this;
            if (!message[0] && message[1]) {
                this.do_notify(success)
            }
            if (!message[0] && !message[1]) {
                this.do_warn(fail + message[2])
            }
            if (message && message[0] != false) {
                this._rpc({
                    model: 'world.sms.trigger',
                    method: 'send_sms',
                    args: [message, true],
                }).then(function (result) {
                    if (result == true) {
                        self.do_notify(success)
                    } else {
                        self.do_warn(fail + result)
                    }
                });
                try {
                    var controller = this.action_manager.getCurrentController();
                    if (message[4] && session.uid == message[5] && controller && controller.widget) {
                        controller.widget.reload();
                    }
                } catch (e) {
                    console.log(e)
                }

            }
        },
    });
});