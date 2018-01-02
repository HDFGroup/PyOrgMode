
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
from PyOrgMode import OrgPlugin, OrgElement


class OrgTable(OrgPlugin):
    """A plugin for table managment"""
    def __init__(self):
        OrgPlugin.__init__(self)
        self.regexp = re.compile("^\s*\|")

    def _treat(self, current, line):
        table = self.regexp.match(line)
        if table:
            if not isinstance(current, self.Element):
                current = current.append(self.Element())
            current.append(line.rstrip().strip("|").split("|"))
        else:
            if isinstance(current, self.Element):
                current = current.parent
            self.treated = False
        return current

    class Element(OrgElement):
        """
        A Table object
        """
        TYPE = "TABLE_ELEMENT"

        def __init__(self):
            OrgElement.__init__(self)

        def _output(self):
            output = ""
            for element in self.content:
                output = output + "|"
                for cell in element:
                    output = output + str(cell) + "|"
                output = output + "\n"
            return output
