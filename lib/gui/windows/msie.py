# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
GUI-specific interface functions for Internet Explorer on Microsoft Windows.
"""

__revision__ = '$Rev: 503 $'
__date__ = '$Date: 2006-06-17 08:14:59 +0200 (Sat, 17 Jun 2006) $'
__author__ = '$Author: johann $'

import os, time, sys
import win32api, win32gui, win32con, pywintypes
from win32com.shell import shellcon, shell
from shotfactory03.gui import windows

class Gui(windows.Gui):
    """
    Special functions for MSIE on Windows.
    """

    def find_window_by_classname(self, classname, verbose=False):
        """Wrapper for win32gui.FindWindow."""
        window = 0
        try:
            window = win32gui.FindWindow(classname, None)
        except pywintypes.error:
            pass
        if verbose:
            print "FindWindow('%s', None) => %d" % (classname, window)
        return window

    def find_child_window_by_classname(self, parent, classname, verbose=False):
        """Wrapper for win32gui.FindWindowEx."""
        window = 0
        try:
            window = win32gui.FindWindowEx(parent, 0, classname, None)
        except pywintypes.error:
            pass
        if verbose:
            print "FindWindowEx(%d, 0, '%s', None) => %d" % (
                parent, classname, window)
        return window

    def down(self, verbose=False):
        """Scroll down one line."""
        ieframe = self.find_window_by_classname('IEFrame', verbose)
        tabs = self.find_child_window_by_classname(
            ieframe, "TabWindowClass", verbose)
        if tabs:
            ieframe = tabs
        scrollable = self.find_child_window_by_classname(
            ieframe, "Shell DocObject View", verbose)
        self.send_keypress(scrollable, win32con.VK_DOWN)
        time.sleep(0.1)

    def start_browser(self, config, url, options):
        """Start browser and load website."""
        self.close()
        # self.remove_crash_dialog(config['browser'])
        if config['command'] == 'msie':
            command = r'c:\progra~1\intern~1\iexplore.exe'
        else:
            command = config['command']
        print 'running', command
        os.spawnl(os.P_DETACH, command, os.path.basename(command), url)
        print "Sleeping %d seconds while page is loading." % options.wait
        time.sleep(options.wait)


if __name__ == '__main__':
    gui = Gui(1024, 768, 24, 90)
    gui.down(verbose=True)
