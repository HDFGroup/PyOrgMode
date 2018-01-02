
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

from PyOrgMode import OrgElement, OrgPlugin, OrgDate


class OrgSchedule(OrgPlugin):
    """Plugin for Schedule elements"""
    # TODO: Need to find a better way to do this
    def __init__(self):
        OrgPlugin.__init__(self)

        self.regexp_scheduled = re.compile(
            "SCHEDULED: ((<|\[).*?(>|\])(--(<|\[).*?(>|\]))?)")
        self.regexp_deadline = re.compile(
            "DEADLINE: ((<|\[).*?(>|\])(--(<|\[).*?(>|\]))?)")
        self.regexp_closed = re.compile(
            "CLOSED: ((<|\[).*?(>|\])(--(<|\[).*?(>|\]))?)")

    def _treat(self, current, line):
        scheduled = self.regexp_scheduled.findall(line)
        deadline = self.regexp_deadline.findall(line)
        closed = self.regexp_closed.findall(line)

        if scheduled != []:
            scheduled = scheduled[0][0]
        if closed != []:
            closed = closed[0][0]
        if deadline != []:
            deadline = deadline[0][0]

        if scheduled or deadline or closed:
            self._append(current,
                         self.Element(scheduled, deadline, closed))
        else:
            self.treated = False
        return current

    class Element(OrgElement):
        """Schedule is an element taking into account DEADLINE, SCHEDULED and CLOSED
        parameters of elements"""
        DEADLINE = 1
        SCHEDULED = 2
        CLOSED = 4
        TYPE = "SCHEDULE_ELEMENT"

        def __init__(self, scheduled=[], deadline=[], closed=[]):
            OrgElement.__init__(self)
            self.type = 0

            if scheduled != []:
                self.type = self.type | self.SCHEDULED
                self.scheduled = OrgDate(scheduled)
            if deadline != []:
                self.type = self.type | self.DEADLINE
                self.deadline = OrgDate(deadline)
            if closed != []:
                self.type = self.type | self.CLOSED
                self.closed = OrgDate(closed)

        def _output(self):
            """Outputs the Schedule element in text format (e.g SCHEDULED:
            <2010-10-10 10:10>)"""
            output = ""
            if self.type & self.SCHEDULED:
                output = output + "SCHEDULED: "+self.scheduled.get_value()+" "
            if self.type & self.DEADLINE:
                output = output + "DEADLINE: "+self.deadline.get_value()+" "
            if self.type & self.CLOSED:
                output = output + "CLOSED: "+self.closed.get_value()+" "
            if output != "":
                output = output.rstrip() + "\n"
            return output
