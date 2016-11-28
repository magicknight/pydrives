#!/usr/bin/env python3
import sys
from pydrives.drives_api.google_drive import GDrive
from pydrives.drives_api.drop_box import DropBox
from pydrives.drives_api.the_box import Box
from pydrives.config import config


class Drive:
    def __init__(self):
        self.google_drive = GDrive()
        self.drop_box = DropBox()
        self.the_box = Box()
        self.modules = config['modules']
        self.current_module = None
        self.actions = config['actions']
        self.current_action = None
        self.parameter_1 = None
        self.parameter_2 = None
        self.is_list = False

    def parse(self, arguments):
        """
        parse the arguments, setup program
        :param arguments:
        :return:
        """
        if len(arguments) < 4:
            print('Usage: main.py', self.modules, self.actions, '<source> <destination>')
            return False
        if not arguments[1] in self.modules:
            print('Wrong module, modules are:', self.modules)
            return False
        self.current_module = getattr(self, arguments[1])
        if not arguments[2] in self.actions:
            print('Wrong action, actions are:', self.actions)
            return False
        self.current_action = getattr(self.current_module, arguments[2])
        if arguments[3] == 'root':
            self.parameter_1 = config[arguments[1]]['root_directory']
        else:
            self.parameter_1 = arguments[3]
        if arguments[2] == 'list':
            self.is_list = True
            return True
        else:
            if len(arguments) < 5:
                print('Usage: main.py', self.modules, self.actions, '<source> <destination>')
                return False
            self.parameter_2 = arguments[4]
            return True

    def run(self):
        """
        run the program
        :return:
        """
        self.current_module.authorization()
        if self.is_list:
            self.current_action(self.parameter_1)
        else:
            self.current_action(self.parameter_1, self.parameter_2)

if __name__ == '__main__':
    drive = Drive()
    if drive.parse(sys.argv):
        drive.run()





