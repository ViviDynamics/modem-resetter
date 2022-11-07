from kasa import SmartPlug

from com.vividynamics.devices.device import Device


class Plug(Device):

    def __init__(self, host):
        super().__init__(host, SmartPlug(host))
