"""View package."""
from .base_view import BaseView
from .main_view import MainView
from .sample_view import SampleView
from .order_view import OrderView
from .monitor_view import MonitorView
from .production_view import ProductionView
from .shipment_view import ShipmentView

__all__ = [
    "BaseView",
    "MainView",
    "SampleView",
    "OrderView",
    "MonitorView",
    "ProductionView",
    "ShipmentView",
]
