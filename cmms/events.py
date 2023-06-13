from cmms.timer import Timer


class Events:
    def on_timer_complete(self, *, timer: Timer):
        print("test")

    def on_pm_create_request(self, equipment_id, *, timer: Timer):
        """Should be triggered by cmms.Timer"""

        # TODO: Do PM creation
