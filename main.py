
import sys
import FANHelper

# This code is used to get the FAN APP ID and FAN ACCESS TOKEN from the command line arguments
if len(sys.argv) == 3:

    fan_app_id = sys.argv[1]
    fan_access_token = sys.argv[2]

    FANHelper.get_and_plot_fan_data(fan_app_id, fan_access_token)
else:
    print("Invalid Command Line Arguments.\nThe arguments should be : <FAN_APP_ID> <FAN_ACCESS_TOKEN>")


