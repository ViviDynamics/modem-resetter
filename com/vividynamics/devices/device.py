from kasa import SmartPlug


class Device(object):
    PLUG = 'plug'
    STRIP = 'strip'

    def __init__(self, host: str, smart_plug: SmartPlug):
        self._host = host
        self._smart_plug = smart_plug

    async def power_off(self):
        await self._smart_plug.turn_off()

    async def power_on(self):
        await self._smart_plug.turn_on()

    async def toggle_led(self):
        value = await self.get_led()
        await self._smart_plug.set_led(not value)

    async def led_on(self):
        await self._smart_plug.set_led(True)

    async def led_off(self):
        await self._smart_plug.set_led(False)

    async def get_led(self) -> bool:
        await self.update()
        return self._smart_plug.led

    async def update(self):
        await self._smart_plug.update()
