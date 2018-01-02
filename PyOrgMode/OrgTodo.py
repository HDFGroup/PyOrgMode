
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

class OrgTodo():
    """Describes an individual TODO item for use in agendas and TODO lists"""
    def __init__(self, heading, todo_state,
                 scheduled=None, deadline=None,
                 tags=None, priority=None,
                 path=[0], node=None
                 ):
        self.heading = heading
        self.todo_state = todo_state
        self.scheduled = scheduled
        self.deadline = deadline
        self.tags = tags
        self.priority = priority
        self.node = node

    def __str__(self):
        string = self.todo_state + " " + self.heading
        return string
