from pyats import aetest
from genie.testbed import load
import logging
from unicon.core.errors import ConnectionError


logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self, testbed):
        """
        establishes connection to all your testbed devices
        """
        # make sure testbed is provided
        assert testbed, "Testbed is  not provided!"

        if len(testbed.devices) == 0:
            self.failed('{testbed} is empty'.format(testbed=str(testbed)))
        else:
            # connect to all testbed devices
            # By default ANY error in the CommonSetup will fail the entire test run
            # Here we catch common exceptions if a device is unavailable to allow test to continue
            try:
                for device in testbed:
                    device.connect(via='ssh', verify=False)
            except (TimeoutError, ConnectionError):
                logger.error("Unable to connect to all devices")


class verify_connected(aetest.Testcase):
    """verify_connected
    Ensure successful connnection to all devices in testbed.
    """
    @aetest.test
    def test(self, testbed, steps):
        # Loop over every device in the testbed
        for device_name, device in testbed.devices.items():
            with steps.start(
                f"Test Connection Status of {device_name}", continue_=True
            ) as step:
                # Test "connnected" status
                if device.connected:
                    logger.info(f"{device_name} connected status: {device.connected}")
                else:
                    logger.error(f"{device_name} connected status: {device.connected}")
                    step.failed()
                    error_occured = True


class verify_ospf_process_id(aetest.Testcase):
    """verify_ospf_process_id
    """
    @aetest.test
    def test(self, testbed, steps):
        command = 'show ip ospf neighbors'
        # Loop over every device in the testbed
        for device_name, device in testbed.devices.items():
            with steps.start(
                f"Verify OSPF Process ID is UNDERLAY on {device_name}", continue_=True
            ) as step:
                output = device.api.nxapi_method_nxapi_cli('send', command, message_format='json', command_type='cli_show', alias='rest').json()
                ospf_process_id = output['ins_api']['outputs']['output']['body']['TABLE_ctx']['ROW_ctx']['ptag']
                if ospf_process_id == 'UNDERLAY':
                    logger.info(f"{device_name} OSPF Process ID: {ospf_process_id}")
                else:
                    logger.error(f"{device_name} OSPF Process ID: {ospf_process_id}")
                    step.failed()


























































class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        for device in testbed:
            # Only disconnect if we are connected to the device
            if device.is_connected() == True:
                device.disconnect()


if __name__ == '__main__':
    # set logger level
    logger.setLevel(logging.INFO)

    aetest.main()