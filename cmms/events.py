import datetime as dt

from dateutil.relativedelta import relativedelta

from cmms import models
from cmms.enums import Periodicity, WorkOrderType


class Events:
    def on_timer_complete(self, *, timer: models.Timer):
        print("test")

    def on_scheduled_pm(self, equipment_id, *, timer: models.Timer):
        """Should be triggered by cmms.Timer"""

        e = models.Equipment.objects.get(pk=equipment_id)
        last = models.WorkOrder.objects.all().order_by("code").last
        date = timer.expires_at
        end_date = timer.expires_at  # TODO: When exactly?
        cost = 0  # TODO
        # TODO: Why do we need these?
        wp = e.work_place
        loc = e.location

        models.WorkOrder(WorkOrderType.PM, last.code + 1 if last else 0, "TODO: DESC", date, end_date, cost, wp, loc, e)
