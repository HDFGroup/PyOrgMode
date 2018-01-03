
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


class OrgNode(OrgPlugin):
    def __init__(self):
        OrgPlugin.__init__(self)
        self.todo_list = ['TODO']
        self.done_list = ['DONE']
        # If the line starts by an indent, it is not a node
        self.keepindent = False

    def _treat(self, current, line):
        # Build regexp
        regexp_string = "^(\*+)\s*"
        if self.todo_list:
            separator = ""
            re_todos = "("
            for todo_keyword in self.todo_list + self.done_list:
                re_todos += separator
                separator = "|"
                re_todos += todo_keyword
            re_todos += ")?\s*"
            regexp_string += re_todos
        regexp_string += "(\[.*?\])?\s+(.*)$"
        self.regexp = re.compile(regexp_string)
        heading = self.regexp.findall(line)
        if heading:  # We have a heading

            if current.parent:
                current.parent.append(current)

                # Is that a new level ?
            if (len(heading[0][0]) > current.level):  # Yes
                # Parent is now the current node
                parent = current
            else:
                # If not, the parent of the current node is the parent
                parent = current.parent
                # If we are going back one or more levels, walk through parents
                while len(heading[0][0]) < current.level:
                    current = current.parent
                    parent = current.parent
            # Creating a new node and assigning parameters
            current = OrgNode.Element()
            current.level = len(heading[0][0])

            current.heading = re.sub(":([:\w]+)*:",
                                     "",
                                     heading[0][3])  # Remove tags

            current.priority = heading[0][2].strip('[#]')
            current.parent = parent
            if heading[0][1]:
                current.todo = heading[0][1]

            # Looking for tags
            heading_without_links = re.sub(" \[(.+)\]", "", heading[0][3])
            heading_without_title = re.sub(r"^(?:.+)\s+(?=:)", "",
                                           heading_without_links)
            matches = re.finditer(r'(?=:([\w]+):)', heading_without_links)
            # if no change, there is no residual string that

            # follows the tag grammar
            if heading_without_links != heading_without_title:
                matches = re.finditer(r'(?=:([\w]+):)',
                                      heading_without_title)
                [current.tags.append(match.group(1)) for match in matches]
        else:
            self.treated = False
        return current

    def _close(self, current):
        # Add the last node
        if (current.level > 0) and current.parent:
            current.parent.append(current)

    class Element(OrgElement):
        # Defines an OrgMode Node in a structure
        # The ID is auto-generated using uuid.
        # The level 0 is the document itself
        TYPE = "NODE_ELEMENT"

        def __init__(self):
            OrgElement.__init__(self)
            self.content = []
            self.level = 0
            self.heading = ""
            self.priority = ""
            self.tags = []
            # TODO  Scheduling structure

        def _output(self):
            output = ""

            if hasattr(self, "level"):
                output = output + "*"*self.level

            if hasattr(self, "todo"):
                output = output + " " + self.todo

            if self.parent is not None:
                output = output + " "
                if self.priority:
                    output = output + "[#" + self.priority + "] "
                output = output + self.heading

                if self.tags:
                    output += ':' + ':'.join(self.tags) + ':'

                output = output + "\n"

            for element in self.content:
                output = output + element.__str__()

            return output

        def append_clean(self, element):
            if isinstance(element, list):
                self.content.extend(element)
            else:
                self.content.append(element)
            self.reparent_cleanlevels(self)

        def reparent_cleanlevels(self, element=None, level=None):
            """
            Reparent the childs elements of 'element' and make levels simpler.
            Useful after moving one tree to another place or another file.
            """
            if element is None:
                element = self.root
            if hasattr(element, "level"):
                if level is None:
                    level = element.level
                else:
                    element.level = level

            if hasattr(element, "content"):
                for child in element.content:
                    if hasattr(child, "parent"):
                        child.parent = element
                        self.reparent_cleanlevels(child,
                                                  level+1)
