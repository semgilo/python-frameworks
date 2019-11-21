# -*- coding: utf-8 -*-
from utils.log import Log
import getopt

class Operation(object):
    """docstring for Operation"""
    def __init__(self):
        super(Operation, self).__init__()

    def handle_commands(self, args):
        # Log.w("Operation handle_commands should be override")
        options, args = self.parse_args(args)

        for option,value in options:
            if option in ['-h', "--help"]:
                self.show_help_info()
                return (None, None)
            elif option in ["-v", "--version"]:
                self.show_version_info()
                return (None, None)

        return (options, args)

    def show_help_info(self):
        Log.i("print something introduce operation.")

    def show_version_info(self):
        Log.i("print something introduce operation.")

    def get_option_info_list(self):
        options = [
            ('h', 'help', 'show_help_info'),
            ('v', 'version', 'show_version_info')
        ]
        return options

    def parse_args(self, args):
        option_info_list = self.get_option_info_list()
        option_abbrs = ""
        option_full_describes = []
        for option_info in option_info_list:
            option_abbrs += option_info[0]
            option_full_describes.append(option_info[1])

        options, args = getopt.getopt(args, option_abbrs, option_full_describes)
        return (options, args)
