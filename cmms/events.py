from __future__ import annotations

import datetime as dt
from contextlib import suppress

from dateutil.relativedelta import relativedelta

from cmms.core import models
from cmms.core.enums import Periodicity, WorkOrderType


class Events:
    def on_timer_complete(self, *, timer: models.Timer):
        print("test")

    def on_scheduled_pm(self, equipment_id, *, timer: models.Timer):
        """Should be triggered by cmms.Timer"""
        e: models.Equipment | None = None
        try:
            e = models.Equipment.objects.get(pk=equipment_id)
        except models.Equipment.DoesNotExist:
            timer.delete()
            return

        if not e:
            raise RuntimeError("How did we get here?")

        expires_at: dt.datetime = timer.expires_at  # type: ignore

        date = expires_at
        if timer.repeat_frequency == Periodicity.MONTHLY:
            date += dt.timedelta(weeks=1)  # automated PM is triggered 7 days before the actual scheduled PM
        end_date = date + relativedelta(months=1)

        models.WorkOrder.objects.create(WorkOrderType.PM, e.name, date, end_date, e)

    def dispatch(self, event_name: str, *args, **kwargs):
        with suppress(AttributeError):
            probably_event = getattr(self, f"on_{event_name}", self.on_timer_complete)
            if callable(probably_event):
                probably_event(*args, **kwargs)
