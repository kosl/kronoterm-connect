import logging

from ha_services.mqtt4homeassistant.components.sensor import Sensor
from ha_services.mqtt4homeassistant.device import MainMqttDevice, MqttDevice
from ha_services.mqtt4homeassistant.mqtt import get_connected_client

import kronoterm2mqtt
from kronoterm2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


class KronotermMqttHandler:
    def __init__(self, user_settings: UserSettings, verbosity: int):
        self.user_settings = user_settings
        self.device_name = user_settings.device_name

        self.mqtt_client = get_connected_client(settings=user_settings.mqtt, verbosity=verbosity)
        self.mqtt_client.loop_start()

        self.main_device = None

    def init_device(self):
        self.main_device = MainMqttDevice(
            name='KRONOTERM 2 MQTT',
            uid=self.device_name,
            manufacturer='kronoterm2mqtt',
            sw_version=kronoterm2mqtt.__version__,
            config_throttle_sec=self.user_settings.mqtt.publish_config_throttle_seconds,
        )
        self.mqtt_device = MqttDevice(
            main_device=self.main_device,
            name="Kronoterm subdevice",
            uid="kronoterm_sub",
            manufacturer='Kronoterm',
            sw_version=kronoterm2mqtt.__version__,
            config_throttle_sec=self.user_settings.mqtt.publish_config_throttle_seconds,
        )

        #################################################################################


        self.temperature = Sensor(
            device=self.mqtt_device,
            name='Temperature',
            uid='temperature',
            state_class='measurement',
            unit_of_measurement='°C',
            suggested_display_precision=1,
        )

        
    def publish(self, user_settings: UserSettings, verbosity: int):

        logger.info(f'Publishing for {self.device_name}')
        
        if self.main_device is None:
            self.init_device()

        self.main_device.poll_and_publish(self.mqtt_client)

        #################################################################################

        self.temperature.set_state(12.34)
        self.temperature.publish(self.mqtt_client)


    def __call__(self, user_settings: UserSettings, verbosity: int):
        logger.info(f'Publishing for {self.device_name}')

        if self.main_device is None:
            self.init_device()

        self.main_device.poll_and_publish(self.mqtt_client)

        #################################################################################

        self.temperature.set_state(parsed_data.temperature)
        self.temperature.publish(self.mqtt_client)

