from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from dateutil.relativedelta import relativedelta

from cmms.enums import WorkOrderType


if TYPE_CHECKING:
    from cmms import models


class Events:
    def on_timer_complete(self, *, timer: models.Timer):
        print("test")

    def on_scheduled_pm(self, equipment_id, *, timer: models.Timer):
        """Should be triggered by cmms.Timer"""
        e = models.Equipment.objects.get(pk=equipment_id)
        if not e:
            timer.delete()
            return

        expires_at: dt.datetime = timer.expires_at  # type: ignore

        date = expires_at + dt.timedelta(weeks=1)  # automated PM is triggered 7 days before the actual scheduled PM
        end_date = date + relativedelta(months=1)

        models.WorkOrder.objects.create(WorkOrderType.PM, e.name, date, end_date, e)
