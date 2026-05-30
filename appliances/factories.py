from appliances.models import Appliance


# Factory Pattern — creates Appliance objects with correct default power ratings
class ApplianceFactory:

    # Default power ratings for each type
    DEFAULTS = {
        Appliance.AC:              {'power_rating_kw': 1.5},
        Appliance.FRIDGE:          {'power_rating_kw': 0.1},
        Appliance.LIGHT:           {'power_rating_kw': 0.06},
        Appliance.WASHING_MACHINE: {'power_rating_kw': 0.5},
        Appliance.WATER_HEATER:    {'power_rating_kw': 3.0},
        Appliance.TV:              {'power_rating_kw': 0.1},
    }

    @staticmethod
    def create(appliance_type, **kwargs):
        if appliance_type not in ApplianceFactory.DEFAULTS:
            valid_types = list(ApplianceFactory.DEFAULTS.keys())
            raise ValueError(
                f"Unknown appliance type '{appliance_type}'. "
                f"Valid types are: {valid_types}"
            )

        appliance_config = dict(ApplianceFactory.DEFAULTS[appliance_type])
        appliance_config['appliance_type'] = appliance_type
        appliance_config.update(kwargs)  # caller's values override the defaults

        return Appliance(**appliance_config)  # unsaved — only saved when .save() is called.
