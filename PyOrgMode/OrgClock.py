
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


class OrgClock(OrgPlugin):
    """Plugin for Clock elements"""
    def __init__(self):
        OrgPlugin.__init__(self)
        self.regexp = re.compile(
            "(?:\s*)CLOCK:(?:\s*)((?:<|\[).*(?:>||\]))--\
            ((?:<|\[).*(?:>||\])).+=>\s*(.*)")

    def _treat(self, current, line):
        clocked = self.regexp.findall(line)
        if clocked:
            self._append(current,
                         self.Element(clocked[0][0],
                                      clocked[0][1],
                                      clocked[0][2]))
        else:
            self.treated = False
        return current

    class Element(OrgElement):
        """Clock is an element taking into account CLOCK elements"""
        TYPE = "CLOCK_ELEMENT"

        def __init__(self, start="", stop="", duration=""):
            OrgElement.__init__(self)
            self.start = OrgDate(start)
            self.stop = OrgDate(stop)
            self.duration = OrgDate(duration)

        def _output(self):
            """Outputs the Clock element in text format
            (e.g CLOCK: [2010-11-20 Sun 19:42]--[2010-11-20 Sun 20:14] => 0:32)
            """
            return "CLOCK: " + self.start.get_value() + "--" + \
                self.stop.get_value() + " =>  "+self.duration.get_value()+"\n"
