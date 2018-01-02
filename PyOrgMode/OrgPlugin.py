
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

class OrgPlugin:
    """
    Generic class for all plugins
    """
    def __init__(self):
        """ Generic initialization """
        self.treated = True
        # By default, the plugin system stores the indentation before the
        # treatment
        self.keepindent = True
        self.keepindent_value = ""

    def treat(self, current, line):
        """This is a wrapper function for _treat. Asks the plugin if he can manage
        this kind of line. Returns True if it can"""
        self.treated = True
        if self.keepindent:
            # Keep a trace of the indentation
            self.keepindent_value = line[0:len(line)-len(line.lstrip(" \t"))]
            return self._treat(current, line.lstrip(" \t"))
        else:
            return self._treat(current, line)

    def _treat(self, current, line):
        """This is the function used by the plugin for the management of
        the line."""
        self.treated = False
        return current

    def _append(self, current, element):
        """ Internal function that adds to current. """
        if self.keepindent and hasattr(element, "set_indent"):
            element.set_indent(self.keepindent_value)
        return current.append(element)

    def close(self, current):
        """ A wrapper function for closing the module. """
        self.treated = False
        return self._close(current)

    def _close(self, current):
        """This is the function used by the plugin to close everything that have been
        opened."""
        self.treated = False
        return current
