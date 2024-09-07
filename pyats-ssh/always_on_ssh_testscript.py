import logging
from pyats import aetest
from pyats.log.utils import banner
from tabulate import tabulate

# Get logger for script
log = logging.getLogger(__name__)

# AE Test Setup
class common_setup(aetest.CommonSetup):
    """Common Setup Section"""

# Connect to devices:
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        testbed.connect()

# Mark the loop for interface tests
# If you add more than 1 device to the testbed this will mark the test cases to be looped over each device
    @aetest.subsection
    def loop_mark(self, testbed):
        aetest.loop.mark(Test_IOS_XE_Interfaces, device_name=testbed.devices)

# AE test Cleanup
class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        testbed.disconnect()

# for running as its own executable
if __name__ == '__main__':
    aetest.main()

class Test_IOS_XE_Interfaces(aetest.Testcase):
    """Parse the pyATS Learn Interface Data"""

    @aetest.test
    def setup(self, testbed, device_name):
        """ Testcase Setup section """
        # connect to device
        self.device = testbed.devices[device_name]
        # Loop over devices in tested for testing

    @aetest.test
    def get_pre_test_interface_data(self):
        self.parsed_interfaces = self.device.learn("interface")

    @aetest.test
    def test_interface_input_errors(self):
        # Test for input discards 
        in_errors_threshold = 3
        self.failed_interfaces = {}
        table_data = []
        for intf, value in self.parsed_interfaces.info.items():
            counter = value['counters']['in_errors']
            table_row = []
            table_row.append(self.device.alias)
            table_row.append(intf)
            table_row.append(counter)
            if int(counter) > in_errors_threshold:
                table_row.append('Failed')
                self.failed_interfaces[intf] = int(counter)
                self.interface_name = intf
                self.error_counter = self.failed_interfaces[intf]
            else:
                table_row.append('Passed')
            table_data.append(table_row)

        # display the table
        log.info(tabulate(table_data,
                          headers=['Device',
                                    'Interface',
                                    'Input Error Counter',
                                    'Passed/Failed'],
                                    tablefmt='orgbl'))

        # should we pass or fail?
        if self.failed_interfaces:
            self.failed("Some interface have input errors")
        else:
            self.passed("No interface have input errors above the acceptable threshold")       