from core.patterns import Subject


# Singleton + Observer Subject — one shared EMS instance controls the whole application
class EnergyManagementSystem(Subject):

    _instance = None  # class level slot that holds the single shared object

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._observers = []
            cls._instance.observers_attached = False  # prevents double attaching on re-run
        return cls._instance

    def __init__(self):
        pass  # intentional no-op, calling super().__init__() would reset _observers every time

    def register_appliance(self, appliance):
        print(f'[EMS] Appliance registered: {appliance}')

    def check_thresholds(self, appliance, daily_total_kwh, daily_threshold_kwh):
        # Only notify if the homeowner's daily usage has exceeded their limit
        if daily_total_kwh > daily_threshold_kwh:
            event_data = {
                'appliance': appliance,
                'homeowner': appliance.owner,
                'daily_total': daily_total_kwh,
                'daily_threshold': daily_threshold_kwh,
            }
            self.notify(event_data)  # fires all attached observers
