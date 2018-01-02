
# -*- encoding: utf-8 -*-
##############################################################################
#
#    PyOrgMode, a python module for treating with orgfiles
#    Copyright (C) 2010 Jonathan BISSON (bissonjonathan on the google thing).
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import re

from PyOrgMode import OrgElement, OrgPlugin


class OrgDrawer(OrgPlugin):
    """A Plugin for drawers"""
    def __init__(self):
        OrgPlugin.__init__(self)
        self.regexp = re.compile("^(?:\s*?)(?::)(\S.*?)(?::)\s*(.*?)$")

    def _treat(self, current, line):
        drawer = self.regexp.search(line)
        if isinstance(current, OrgDrawer.Element):  # We are in a drawer
            if drawer:
                if drawer.group(1).upper() == "END":  # Ending drawer
                    current = current.parent
                elif drawer.group(2):  # Adding a property
                    self._append(current,
                                 self.Property(drawer.group(1),
                                               drawer.group(2)))
            else:  # Adding text in drawer
                self._append(current,
                             line.rstrip("\n"))
        elif drawer:  # Creating a drawer
            current = self._append(current,
                                   OrgDrawer.Element(drawer.group(1)))
        else:
            self.treated = False
            return current
        # It is a drawer, change the current also (even if not modified)
        return current

    class Element(OrgElement):
        """A Drawer object, containing properties and text"""
        TYPE = "DRAWER_ELEMENT"

        def __init__(self, name=""):
            OrgElement.__init__(self)
            self.name = name

        def _output(self):
            output = ":" + self.name + ":\n"
            for element in self.content:
                output = output + str(element) + "\n"
            output = output + self.indent
            if self.name.upper() != "LOGBOOK":
                output += ":END:\n"
            return output

    class Property(OrgElement):
        """A Property object, used in drawers."""

        def __init__(self, name="", value=""):
            OrgElement.__init__(self)
            self.name = name
            self.value = value

        def _output(self):
            """Outputs the property in text format (e.g. :name: value)"""
            return ":" + self.name + ": " + self.value
