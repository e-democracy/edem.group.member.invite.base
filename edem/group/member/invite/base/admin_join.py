# coding=utf-8
from zope.formlib import form
from gs.group.member.invite.base.invite import InviteEditProfileForm
from edem.profile.signup.base.utils import fn_to_nickname

import logging
log = logging.getLogger('edem.group.member.invite.base.admin_join')


class EDemAdminJoinEditProfileForm(InviteEditProfileForm):
    @form.action(label=u'Invite', failure='handle_add_action_failure')
    def handle_add(self, action, data):
        userInfo = self.actual_handle_add(action, data)
        if userInfo and (userInfo.nickname == userInfo.id):
            m = 'Adding nickname to %s (%s)' % (userInfo.name, userInfo.id)
            log.info(m.encode('ascii', 'ignore'))
            nickname = fn_to_nickname(self.context, userInfo.name)
            userInfo.user.add_nickname(nickname)

    def handle_add_action_failure(self, action, data, errors):
        log.error(errors)
        if len(errors) == 1:
            self.status = u'<p>There is an error: %s</p>' % errors[0]
        else:
            self.status = u'<p>There are multiple errors:</p><ul>'
            for error in errors:
                self.status = self.status + u'<li>%s</li>' % error

            self.status = self.status + u'</ul>'

        assert type(self.status) == unicode
