import asyncio
from typing import cast
from kasa import SmartStrip, SmartPlug

from com.vividynamics.util import ASYNCIO_EVENT_LOOP
from com.vividynamics.devices.device import Device


class Strip(Device):

    def __init__(self, host: str, plug_alias: str = None):
        self._strip: SmartStrip = SmartStrip(host)
        update_task = ASYNCIO_EVENT_LOOP.create_task(self._strip.update())
        ASYNCIO_EVENT_LOOP.run_until_complete(asyncio.gather(update_task))
        plugs: list[SmartPlug] = cast(list[SmartPlug], self._strip.children)
        plug: SmartPlug = next(filter(lambda c: c.alias == plug_alias, plugs), None)
        if not plug:
            raise RuntimeError(f'Plug could not be found matching alias: {plug_alias}')
        super().__init__(host, plug)

    async def toggle_led(self):
        value = await self.get_led()
        await self._strip.set_led(not value)

    async def led_on(self):
        await self._strip.set_led(True)

    async def led_off(self):
        await self._strip.set_led(False)

    async def get_led(self) -> bool:
        await self._strip.update()
        return self._strip.led
