import abc


# Strategy Pattern — all three pricing algorithms share this interface
class PricingStrategy(abc.ABC):

    @abc.abstractmethod
    def calculate(self, usage_kwh, timestamp):
        # Returns cost in pence, raise NotImplementedError if subclass skips this
        raise NotImplementedError


# Same price per kWh at any hour of the day
class FlatRateStrategy(PricingStrategy):

    def __init__(self, base_rate):
        self.base_rate = base_rate

    def calculate(self, usage_kwh, timestamp):
        return usage_kwh * self.base_rate  # timestamp ignored for flat rate


# Higher rate during peak hours, cheaper off-peak
class TimeOfUseStrategy(PricingStrategy):

    def __init__(self, base_rate, peak_rate, peak_start_hour, peak_end_hour):
        self.base_rate = base_rate
        self.peak_rate = peak_rate
        self.peak_start_hour = peak_start_hour
        self.peak_end_hour = peak_end_hour

    def calculate(self, usage_kwh, timestamp):
        current_hour = timestamp.hour
        is_peak_hour = self.peak_start_hour <= current_hour < self.peak_end_hour
        if is_peak_hour:
            return usage_kwh * self.peak_rate
        return usage_kwh * self.base_rate


# Flat rate with a percentage discount for renewable energy
class GreenEnergyStrategy(PricingStrategy):

    def __init__(self, base_rate, discount_percent):
        self.base_rate = base_rate
        self.discount_percent = discount_percent

    def calculate(self, usage_kwh, timestamp):
        full_cost = usage_kwh * self.base_rate
        discount_amount = full_cost * (self.discount_percent / 100)
        return full_cost - discount_amount
