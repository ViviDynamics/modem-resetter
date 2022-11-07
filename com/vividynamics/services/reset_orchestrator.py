import asyncio

from com.vividynamics.util import ASYNCIO_EVENT_LOOP, logger
from com.vividynamics.devices.device import Device

FLASH_DELAY = 0.5


class ResetOrchestrator:
    def __init__(self, device: Device, shutdown_duration: float = 30, boot_duration: float = 150):
        self._shutdown_duration = shutdown_duration
        self._boot_duration = boot_duration
        self._total_duration = self._shutdown_duration + self._boot_duration
        self._device = device
        self._flasher = False

    def reset(self):
        logger.info('Begin reset process...')
        flash_lights = ASYNCIO_EVENT_LOOP.create_task(self._flash_lights())
        cycle_power = ASYNCIO_EVENT_LOOP.create_task(self._cycle_power())
        ASYNCIO_EVENT_LOOP.run_until_complete(asyncio.gather(flash_lights, cycle_power))
        logger.info('Reset complete.')

    async def _cycle_power(self):
        logger.debug('Power cycle start...')
        await self._device.power_off()
        await asyncio.sleep(self._shutdown_duration)
        await self._device.power_on()
        await asyncio.sleep(self._boot_duration)
        logger.debug('Power cycle finished.')
        self._flasher = False

    async def _flash_lights(self):
        logger.debug('Flash lights start...')
        self._flasher = True
        while self._flasher:
            await self._device.toggle_led()
            await asyncio.sleep(FLASH_DELAY)
        await self._device.led_off()
        logger.debug('Flash lights complete.')
