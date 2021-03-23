odoo.define('crm.lead.Activity', function (require) {
    "use strict";

const field_registry2 = require('web.field_registry');

require('mail.Activity');
const KanbanActivity = field_registry2.get('kanban_activity');

KanbanActivity.include({
    events: Object.assign({}, KanbanActivity.prototype.events, {
        'click .o_mark_as_done2': '_onMarkActivityDone2',
    }),
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    /**
     * @private
     * @param  {Event} event
     */
    _onMarkActivityDone2(event) {
            const activityID = $(event.currentTarget).data('data-activity-id');

            this._rpc({
                model: 'mail.activity',
                method: 'mark_as_done_2',
                args: [[activityID]],
            }).then(result => {
                this.trigger_up('reload', {keepChanges: true});
            });
            console.log(activityID);

        },
});

});
