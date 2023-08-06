import asyncio
import time
from types import SimpleNamespace
from typing import List, Dict

from sanic import Sanic, Request
from sanic.response import BaseHTTPResponse

from web_foundation import settings
from web_foundation.environment.events.metrics import NewMetricEvent
from web_foundation.environment.metrics.basemetric import CounterBaseMetric, HistogramBaseMetric, \
    SummaryBaseMetric
from web_foundation.environment.metrics.exporter import BaseMetric
from web_foundation.kernel import IChannel

try:
    from prometheus_client.metrics import Gauge, Histogram, Counter, MetricWrapperBase
except ImportError:
    settings.PROMETHEUS_METRICS_ENABLE = False


class MetricsMixin:
    _metrics: List[BaseMetric]
    _channel: IChannel

    def _reg_metrics(self):
        pass

    async def give_metric(self, metric: BaseMetric):
        asyncio.create_task(self._channel.produce(NewMetricEvent(metric)))


class ApiMetricsMixin(MetricsMixin):
    _name: str
    app_name: str
    sanic_app: Sanic
    stored_metric: Dict[str, BaseMetric]

    def _reg_metrics(self):
        self.sanic_app.ctx.metrics = SimpleNamespace()

        async def metrics_before(request: Request):
            if not settings.METRICS_ENABLE:
                return
            request.app.ctx.metrics.exec_time = time.time()

        async def metrics_after(request: Request, response: BaseHTTPResponse):
            if not settings.METRICS_ENABLE:
                return
            else:
                metr = HistogramBaseMetric(f"exec_request_time")
                metr.observe(time.time() - request.app.ctx.metrics.exec_time)
                metr.add_label(request=request.path,
                               method=request.method,
                               status=str(response.status))
                await self.give_metric(metr)
                metr = CounterBaseMetric(f"request_path_count", value=1)
                metr.add_label(request=request.path,
                               method=request.method,
                               status=str(response.status))
                await self.give_metric(metr)
                metr = SummaryBaseMetric(f"request_path_latency")
                metr.add_label(request=request.path,
                               method=request.method,
                               status=str(response.status))
                metr.observe(time.time() - request.app.ctx.metrics.exec_time)
                await self.give_metric(metr)

        self.sanic_app.register_middleware(metrics_before)
        self.sanic_app.register_middleware(metrics_after, "response")
