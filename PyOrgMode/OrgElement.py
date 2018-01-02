
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

class OrgElement:
    """
    Generic class for all Elements excepted text and unrecognized ones
    """
    def __init__(self):
        self.content = []
        self.parent = None
        self.level = 0
        self.indent = ""

    def append(self, element):
        # TODO Check validity
        self.content.append(element)
        # Check if the element got a parent attribute
        # If so, we can have childrens into this element
        if hasattr(element, "parent"):
            element.parent = self
        return element

    def set_indent(self, indent):
        """ Transfer the indentation from plugin to element. """
        self.indent = indent

    def output(self):
        """ Wrapper for the text output. """
        return self.indent+self._output()

    def _output(self):
        """ This is the function really used by the plugin. """
        return ""

    def __str__(self):
        """ Used to return a text when called. """
        return self.output()
