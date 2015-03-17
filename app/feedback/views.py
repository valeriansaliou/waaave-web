from django.shortcuts import render

from _commons.decorators.security import auth_required
from _commons.helpers.rank import RankHelper

from rank.helpers import RankProcessHelper

from models import *
from forms import *
from emails import *


@auth_required
def root(request):
    """
    Feedback > Root
    """
    user = request.user
    report_sent, report_already_sent = False, False

    try:
        instance = Report.objects.get(user=user)
        report_already_sent = True
    except Report.DoesNotExist:
        instance = Report(user=user)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()

            if not report_already_sent:
                report_email(
                    request,
                    user,
                    form
                )

            report_sent = True

            # User rank gains 2 points
            if not report_already_sent:
                RankProcessHelper.create(
                    instance.user.profile,
                    None,
                    [instance.user_id, 'feedback'],
                    RankHelper.get_action_by_name('feedback_report'),
                )
    
    if request.method != 'POST' or report_sent:
        form = ReportForm(instance=instance)

    return render(request, 'feedback/feedback_root.jade', {
        'form': form,
        'report_sent': report_sent,
        'report_already_sent': report_already_sent
    })
