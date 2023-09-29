from .models import (
    ProductionEvent,
    WeatherEvent,
    ChemicalEvent,
    GeneralEvent,
)

WEATHER_EVENT_TYPE = 0
PRODUCTION_EVENT_TYPE = 1
CHEMICAL_EVENT_TYPE = 2
GENERAL_EVENT_TYPE = 3

event_map = {
    0: WeatherEvent,
    1: ProductionEvent,
    2: ChemicalEvent,
    3: GeneralEvent,
}

ALLOWED_PERIODS = ["week", "month", "year"]
