import os
from genie.testbed import load

def main(runtime):

    #Load the testbed
    if not runtime.testbed:
        # If no testbed is provided, load the default testbed
        # Load the default location of the testbed
        testbedfile = os.path.join('testbed_ssh.yaml')
        testbed = load(testbedfile)
    else:
        # Use the one provided
        testbed = runtime.testbed

    # Find the location of the script in the relation to the job file
    testscript = os.path.join(os.path.dirname(__file__), 'always_on_ssh_testscript.py')

    # Run the script
    runtime.tasks.run(testscript=testscript, testbed=testbed)

