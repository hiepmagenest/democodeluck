odoo.define('web.call.effect', function (require) {
"use strict";

/**
 * Sh@dowWalker
 */

var Widget = require('web.Widget');
var core = require('web.core');

var _t = core._t;

var CallEffect = Widget.extend({
    template: 'show.call.effect',
    xmlDependencies: ['/sim_advanced_call_center/static/src/xml/call_effect.xml'],
    /**
     * @override
     * @constructor
     */
    init: function (options) {
        this._super.apply(this, arguments);
        var rainbowDelay = {slow: 4500, medium: 3500, fast:2000, no: false };
        this.options = _.defaults(options || {}, {
            fadeout: 'medium',
            img_url: '/sim_advanced_call_center/static/images/phone-ringing-gif-9.gif',
            message: _t('UnKnown!'),
        });
        this.delay = rainbowDelay[this.options.fadeout];
    },
    /**
     * @override
     */
    start: function () {
        var self = this;
        core.bus.on('click', this, function (ev) {
            if (ev.originalEvent && ev.target.className.indexOf('o_reward') === -1) {
                this.destroy();
            }
        });
        if (this.delay) {
            setTimeout(function () {
                self.$el.addClass('o_reward_fading');
                setTimeout(function () {
                    self.destroy();
                }, 600); // destroy only after fadeout animation is completed
            }, this.delay);
        }
        this.$('.content').append(this.options.message);
        return this._super.apply(this, arguments);
    }
});

return CallEffect;

});
