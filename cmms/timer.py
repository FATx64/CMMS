from __future__ import annotations

import datetime as dt
import threading
from contextlib import suppress

from dateutil.relativedelta import relativedelta

from cmms import models
from cmms.abstract import singleton
from cmms.enums import Periodicity
from cmms.events import Events
from cmms.utils import utcnow


class TimerInterrupted(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Timer is interrupted")


class Timer(threading.Thread, metaclass=singleton.Singleton):
    """Modified version of Z3R0's Timer extension

    Modified to work in sync environment, probably doesn't work exactly the
    same, but close enough.

    REF: https://github.com/ZiRO-Bot/Z3R0/blob/c511135/src/main/exts/timer/timer.py#L76-L141
    """

    def __init__(self) -> None:
        self.have_data = threading.Event()
        self._current_timer = None
        self._restart_event = threading.Event()
        self.events = Events()
        super().__init__(daemon=True)

    def wait(self, timeout: float | None = None):
        self._restart_event.wait(timeout)

    def restart(self) -> None:
        self.have_data.set()
        self._restart_event.set()

    def get_active_timer(self, days=40) -> models.Timer | None:
        return models.Timer.objects.filter(expires_at__lt=utcnow() + dt.timedelta(days=days)).order_by("expires_at").first()

    def wait_for_active_timer(self) -> models.Timer:
        future = 40  # how far ahead the timer can see

        timer = self.get_active_timer(days=future)
        if timer:
            self.have_data.set()
            return timer

        self.have_data.clear()
        self._current_timer = None
        self.have_data.wait(future * 86400)
        if self._restart_event.is_set():
            print("Restarting...")
            raise TimerInterrupted()

        # As long as have_data.set() is executed (not by Timer.stop()), this will always return models.Timer
        return self.get_active_timer(days=future)  # type: ignore

    def handle_timer(self, timer: models.Timer):
        args = timer.extra.get("args", [])
        kwargs = {"timer": timer}
        kwargs.update(timer.extra.get("kwargs", {}))

        print(f"Dispatching '{timer.name}'...")
        self.events.dispatch(timer.name, *args, **kwargs)

        if timer.repeat == 0:
            return timer.delete()
        elif timer.repeat >= 1:
            timer.repeat -= 1

        dt_kwargs = Periodicity.to_dt_kwargs(timer.repeat_frequency, 1)
        if dt_kwargs:
            timer.expires_at = timer.expires_at + relativedelta(**dt_kwargs)  # type: ignore
            timer.save()
        else:
            timer.delete()

    def run(self):
        print("Starting timer thread...")
        while True:
            # Timer interruption just means we need to restart.
            # This should only happened when new timer with much earlier expiry
            # time is added while the logic is trying to get active timer or
            # when the logic is waiting for active timer to expired
            with suppress(TimerInterrupted):
                self._restart_event.clear()
                timer = self._current_timer = self.wait_for_active_timer()
                now = utcnow()

                if timer.expires_at >= now:
                    self.wait((timer.expires_at - now).total_seconds())

                if self._restart_event.is_set():
                    print("Restarting...")
                    raise TimerInterrupted()

                self.handle_timer(timer)
