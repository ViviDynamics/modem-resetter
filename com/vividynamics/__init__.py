import os

from com.vividynamics.devices.device import Device
from com.vividynamics.devices.plug import Plug
from com.vividynamics.devices.strip import Strip
from com.vividynamics.services.monitoring_service import MonitoringService
from com.vividynamics.services.probe import Probe
from com.vividynamics.services.reset_orchestrator import ResetOrchestrator


def _validate_float_env(value: str, missing_error_message, environment_variable_name) -> float:
    if not value:
        raise EnvironmentError(missing_error_message)
    try:
        return float(value)
    except ValueError:
        raise EnvironmentError(f'Incorrect value set for the {environment_variable_name} environment variable. The '
                               f'value data type must be an integer or a float.')


def ping_addresses() -> list[str]:
    idx = 0
    servers = list()
    while os.getenv(f'PING_ADDRESS_{idx}'):
        servers.append(os.getenv(f'PING_ADDRESS_{idx}'))
        idx += 1

    if not any(servers):
        raise EnvironmentError('At least 1 PING_ADDRESS_(X) must configured on the environment in order to validate '
                               'the internet connection is active. Example: PING_ADDRESS_0=1.0.0.1')
    return servers


def sample_websites() -> list[str]:
    idx = 0
    websites = list()
    while os.getenv(f'SAMPLE_WEBSITE_{idx}'):
        websites.append(os.getenv(f'SAMPLE_WEBSITE_{idx}'))
        idx += 1
    if not any(websites):
        raise EnvironmentError('At least 1 SAMPLE_WEBSITE_(X) must configured on the environment in order to validate '
                               'the internet connection is active. Example: SAMPLE_WEBSITE_0=www.google.com')
    return websites


def timeout() -> float:
    environment_variable_name = 'TIMEOUT'
    return _validate_float_env(
        os.getenv('TIMEOUT', 5.0),
        f'The {environment_variable_name} environment variable is missing. Please set as a float value for the number '
        f'of seconds to wait before failing any connections made by the probe.',
        environment_variable_name
    )


# Possible values: plug, strip
def device_type() -> str:
    possible_values = ['plug', 'strip']
    value = os.getenv('DEVICE_TYPE')
    if not value and not value in possible_values:
        raise EnvironmentError(f'The DEVICE_TYPE environment variable is missing or is set incorrectly. Possible '
                               f'values include the following: {", ".join(possible_values)}.')
    return value


def device_hostname() -> str:
    value = os.getenv('DEVICE_HOSTNAME')
    if not value:
        raise EnvironmentError('The DEVICE_HOSTNAME environment variable is missing.')
    return value


def strip_plug_alias() -> str:
    value = os.getenv('STRIP_PLUG_ALIAS')
    if device_type() == 'strip' and not value:
        raise EnvironmentError('The STRIP_PLUG_ALIAS environment variable is missing. It is required when the '
                               'DEVICE_TYPE environment variable is set to "strip".')
    return value


def device() -> Device:
    match device_type():
        case Device.PLUG:
            return Plug(device_hostname())
        case Device.STRIP:
            return Strip(device_hostname(), strip_plug_alias())
        case _:
            raise RuntimeError('Failed to create a Device. Please verify that the environment is correctly configured!')


def shutdown_duration() -> float:
    environment_variable_name = 'SHUTDOWN_DURATION'
    value = os.getenv(environment_variable_name, 30.0)
    return _validate_float_env(
        value,
        f'The {environment_variable_name} environment variable is missing. Please set as a float value for the number '
        f'of seconds to wait after turning off power to the plug.',
        environment_variable_name
    )


def boot_duration() -> float:
    environment_variable_name = 'BOOT_DURATION'
    value = os.getenv(environment_variable_name, 150.0)
    return _validate_float_env(
        value,
        f'The {environment_variable_name} environment variable is missing. Please set as a float value for the number '
        f'of seconds to wait after turning on power to the plug.',
        environment_variable_name
    )


def health_check_interval() -> float:
    environment_variable_name = 'HEALTH_CHECK_INTERVAL'
    value = os.getenv(environment_variable_name)
    return _validate_float_env(
        value,
        f'The {environment_variable_name} environment variable is missing. Please set as a float '
        f'value for the number of seconds to wait between internet connection polling.',
        environment_variable_name
    )


def main():
    probe = Probe(ping_addresses(), sample_websites(), timeout())
    orchestrator = ResetOrchestrator(device(), shutdown_duration(), boot_duration())
    monitor = MonitoringService(probe, orchestrator, health_check_interval())

    try:
        monitor.monitor()
    finally:
        monitor.stop_monitoring()
