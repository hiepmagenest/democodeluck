odoo.define('sim_crm_activity/static/src/models/activity/activity.js', function (require) {
'use strict';

const {
    registerFieldPatchModel,
    registerClassPatchModel,
} = require('mail/static/src/model/model_core.js');
// const { one2one } = require('mail/static/src/model/model_field.js');
const { attr, many2many, many2one } = require('mail/static/src/model/model_field.js');
registerFieldPatchModel('mail.activity', 'sim_crm_activity/static/src/models/activity/activity.js', {
    result_vals: attr(),
});

registerClassPatchModel('mail.activity', 'sim_crm_activity/static/src/models/activity/activity.js', {
    //----------------------------------------------------------------------
    // Public
    //----------------------------------------------------------------------
    /**
     * @override
     */
    convertData(data) {
        const data2 = this._super(data);
        if ('result_vals' in data)  {
                data2.result_vals =
                    JSON.parse(data['result_vals'])
                ;
            }

        return data2;
    },

     // MarkDone2() {
     //        const activityID = $(event.currentTarget).data('data-activity-id');
     //        console.log(55);
     //
     //        this._rpc({
     //            model: 'mail.activity',
     //            method: 'mark_as_done_2',
     //            args: [[activityID]],
     //        })
     //
     //    },
});


});
