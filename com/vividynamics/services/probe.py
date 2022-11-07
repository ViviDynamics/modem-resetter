import socket
from http import client
from http.client import HTTPException
from multiprocessing import Pool
from com.vividynamics.util import logger


class Probe:
    DNS_PORT = 53

    def __init__(self, dns_addresses: list, websites: list, timeout: float):
        self._dns_addresses = dns_addresses
        self._websites = websites
        self._timeout = timeout

    # noinspection PyBroadException
    def is_connection_alive(self):
        try:
            with Pool() as P:
                return any(list(P.map(self._ping_address, self._dns_addresses))) and any(
                    list(P.map(self._can_send_and_receive_data, self._websites)))
        except Exception as e:
            logger.warn(f'Internet connection probe failed with the following exception: {str(e)}!')
            return False

    def _ping_address(self, address: str):
        try:
            conn = socket.create_connection((address, Probe.DNS_PORT), self._timeout)
            conn.close()
            logger.debug(f'Ping to {address} succeeded.')
            return True
        except OSError:
            logger.warn(f'Ping to {address} failed!')
        return False

    def _can_send_and_receive_data(self, url):
        try:
            connection = client.HTTPSConnection(url, timeout=self._timeout)
            connection.request('GET', '/')
            response = connection.getresponse()
            connection.close()
            logger.debug(f'GET request to {url} succeeded with status {response.status} - {response.reason}.')
            return True
        except HTTPException as e:
            logger.warn(f'GET request to {url} failed: {str(e)}!')
        except OSError as e:
            logger.warn(f'GET request to {url} failed: {str(e)}!')
        return False
