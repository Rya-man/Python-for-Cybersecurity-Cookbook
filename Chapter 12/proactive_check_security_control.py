# proactive_check_security_control.py

"""
Description:
    A security control for proactively checking the configurations in /etc/login.defs and print the security weakness 
    in the configuration. This can then be called periodically by adding a line in /etc/crontab.

Author:
    Nishant Krishna

Created:
    12 February, 2023
"""


import platform
import subprocess


class ProactiveCheckSecurityControl:
    PASS_MAX_DAYS_POLICY = 60

    def check_config(self):
        if platform.system() == 'Linux':
            output = subprocess.check_output('grep \'^PASS\' /etc/login.defs', shell=True)
            output_list = output.decode('utf-8').split('\n')

            # Print all the login.defs config
            print('Password configuration from login.def:')
            print(output_list, '\n')

            # Find out if the configurations are as per the policy
            num_failed_check = 0
            for config_item_line in output_list:
                config_item = config_item_line.split('\t')

                if (config_item[0] == 'PASS_MAX_DAYS') and int(config_item[1]) > int(self.PASS_MAX_DAYS_POLICY):
                    print('Config Item: ', config_item[0], '\tExpected Value: ',
                          self.PASS_MAX_DAYS_POLICY, '\tFound Value: ', config_item[1])
                    num_failed_check += 1

            if (num_failed_check > 0):
                print('\nNo. of failed checks: ', num_failed_check)

        else:
            print('This program can only be run on Linux')


if __name__ == "__main__":
    security_control = ProactiveCheckSecurityControl()
    security_control.check_config()