import asyncio
import time

from com.vividynamics.services.probe import Probe
from com.vividynamics.services.reset_orchestrator import ResetOrchestrator
from com.vividynamics.util import ASYNCIO_EVENT_LOOP, logger


class MonitoringService:
    def __init__(self, probe: Probe, reset_orchestrator: ResetOrchestrator, health_check_interval: float):
        self._probe = probe
        self._reset_orchestrator = reset_orchestrator
        self._health_check_interval = health_check_interval
        self._keep_monitoring = False
        self._reset_lock = False

    def monitor(self):
        self._keep_monitoring = True
        while self._keep_monitoring:
            self._check()
            time.sleep(self._health_check_interval)

    def stop_monitoring(self):
        stop_and_cleanup = ASYNCIO_EVENT_LOOP.create_task(self._cleanup())
        ASYNCIO_EVENT_LOOP.run_until_complete(asyncio.gather(stop_and_cleanup))

    def _check(self):
        if self._probe.is_connection_alive():
            logger.debug(f'Internet connection healthy.')
        else:
            self._reset_lock = True
            logger.warn('Internet connection outage detected!')
            self._reset_orchestrator.reset()
            self._reset_lock = False

    async def _cleanup(self):
        self._keep_monitoring = False
        while self._reset_lock:
            await asyncio.sleep(self._health_check_interval)
