import os
import rospy
import QtGui
from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QWidget
#from controller.msg import Permission
from std_srvs.srv import Empty
from PyQt4.QtCore import QObject, pyqtSignal
#from mavros.msg import OverrideRCIn
#from mavros.msg import BatteryStatus

#import analysis
#import utils
import subprocess

#import trajectory_generator
#from trajectory import Trajectory
#from trajectory_generato import TrajectoryGenerator
#from trajectory_node import TrajectoryNode
#from mocap.msg import QuadPositionDerived
#from controller.msg import Permission
#from straight_line_class import StraightLineGen
#from pointInput import pointInputPlugin
#from RCDisplay import RCDisplayPlugin
from saver import saverPlugin

from saver_mavros import saver_mavrosPlugin

from positionPlot import positionPlotPlugin

from TrajectorySelection import TrajectorySelectionPlugin

from ChooseController import ChooseControllerPlugin

from ChooseSimulator import ChooseSimulatorPlugin



import argparse


class tabbedGUIPlugin(Plugin):

    

    
    def __init__(self, context,namespace = None):

        # it is either "" or the input given at creation of plugin
        self.namespace = self._parse_args(context.argv())
        # warn message for letting user know namespace for the gui
        rospy.logwarn("Gui within namespace: " + self.namespace)


        super(tabbedGUIPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('tabbedGUIPlugin')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns
        
        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which is a sibling of this file
        # in this example the .ui and .py file are in the same folder
        ui_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tabbedGUI.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('tabbedGUIUi')
        # Show _widget.windowTitle on left-top of each plugin (when 
        # it's set in _widget). This is useful when you open multiple 
        # plugins at once. Also if you open multiple instances of your 
        # plugin at once, these lines add number to make it easy to 
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)
        
        # # Adding all the tabs


        self.saver_mavros        = saver_mavrosPlugin(context,self.namespace)
        # self.saver               = saverPlugin(context,self.namespace)
        self.positionPlot        = positionPlotPlugin(context,self.namespace)
        self.TrajectorySelection = TrajectorySelectionPlugin(context,self.namespace)
        self.ChooseController    = ChooseControllerPlugin(context,self.namespace)
        self.ChooseSimulator     = ChooseSimulatorPlugin(context,self.namespace)


        self._widget.tabWidget.addTab(self.saver_mavros._widget,'Data recorder')
        # self._widget.tabWidget.addTab(self.saver._widget,'Data recorder')
        self._widget.tabWidget.addTab(self.positionPlot._widget,'Check Data')
        self._widget.tabWidget.addTab(self.TrajectorySelection._widget,'Select Trajectory')
        self._widget.tabWidget.addTab(self.ChooseController._widget,'Select Controller')
        self._widget.tabWidget.addTab(self.ChooseSimulator._widget,'Select Simulator')

        self._widget.tabWidget.show()

    def _parse_args(self, argv):

        parser = argparse.ArgumentParser(prog='saver', add_help=False)

        # args = parser.parse_args(argv)

        if argv:
            namespace = argv[0]
            return namespace            
        else:
            # is argv is empty return empty string
            return ""

        
    # def execute(self,cmd):
    #     #subprocess.Popen(["bash","-c","cd "+self.pwd+"/src/kampala/gui/scripts; echo "+cmd+" > pipefile" + self.name]) 


    # def shutdown_plugin(self):
    #     # TODO unregister all publishers here
    #     pass

    # def save_settings(self, plugin_settings, instance_settings):
    #     # TODO save intrinsic configuration, usually using:
    #     # instance_settings.set_value(k, v)
    #     instance_settings.set_value("irisindex", self._widget.IrisInputBox.currentIndex())

    # def restore_settings(self, plugin_settings, instance_settings):
    #     # TODO restore intrinsic configuration, usually using:
    #     # v = instance_settings.value(k)
    #     index = instance_settings.value("irisindex",0)
    #     self._widget.IrisInputBox.setCurrentIndex(int(index))
        
    #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog

    
