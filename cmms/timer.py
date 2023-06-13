from __future__ import annotations

import datetime as dt
import threading
from contextlib import suppress

from cmms import models
from cmms.utils import dispatch, utcnow


class TimerInterrupted(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Timer is interrupted")


class Timer(threading.Thread):
    """Modified version of Z3R0's Timer extension

    Modified to work in sync environment, probably doesn't work exactly the
    same, but close enough.

    REF: https://github.com/ZiRO-Bot/Z3R0/blob/c511135/src/main/exts/timer/timer.py#L76-L141
    """

    def __init__(self) -> None:
        self.have_data = threading.Event()
        self._current_timer = None
        self._stop_event = threading.Event()
        super().__init__(daemon=True)

    def wait(self, timeout: float | None = None):
        self._stop_event.wait(timeout)

    def stop(self) -> None:
        self.have_data.set()
        self._stop_event.set()

    def get_active_timer(self) -> models.Timer | None:
        return models.Timer.objects.all().order_by("expires_at").first()

    def wait_for_active_timer(self) -> models.Timer:
        timer = self.get_active_timer()
        if timer:
            self.have_data.set()
            return timer

        self.have_data.clear()
        self._current_timer = None
        self.have_data.wait()
        if self._stop_event.is_set():
            raise TimerInterrupted()

        # As long as have_data.set() is executed (not by Timer.stop()), this will always return models.Timer
        return self.get_active_timer()  # type: ignore

    def handle_timer(self, timer: models.Timer):
        dispatch(timer.name, timer)

        if timer.repeat == 0:
            timer.delete()
        elif timer.repeat >= 1:
            timer.repeat -= 1
            timer.save()

    def run(self):
        while True:
            # Timer interruption just means we need to restart.
            # This should only happened when new timer with much earlier expiry
            # time is added while the logic is trying to get active timer or
            # when the logic is waiting for active timer to expired
            with suppress(TimerInterrupted):
                timer = self._current_timer = self.wait_for_active_timer()
                now = utcnow()

                if timer.expires_at >= now:
                    self.wait((timer.expires_at - now).total_seconds())

                if self._stop_event.is_set():
                    raise TimerInterrupted()

                self.handle_timer(timer)
