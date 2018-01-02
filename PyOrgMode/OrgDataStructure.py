
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

from PyOrgMode import OrgElement
from PyOrgMode import OrgTable, OrgDrawer, OrgNode, OrgSchedule, OrgClock

class OrgDataStructure(OrgElement):
    """
    Data structure containing all the nodes
    The root property contains a reference to the level 0 node
    """
    root = None
    TYPE = "DATASTRUCTURE_ELEMENT"

    def __init__(self):
        OrgElement.__init__(self)
        self.plugins = []
        self.load_plugins(OrgTable(),
                          OrgDrawer(),
                          OrgNode(),
                          OrgSchedule(),
                          OrgClock())

        # Add a root element
        #
        # The root node is a special node (no parent) used as a container for
        # the file

        self.root = OrgNode.Element()
        self.root.parent = None
        self.level = 0

    def load_plugins(self, *arguments, **kw):
        """
        Used to load plugins inside this DataStructure
        """
        for plugin in arguments:
            self.plugins.append(plugin)

    def set_todo_states(self, new_states):
        """
        Used to override the default list of todo states for any
        OrgNode plugins in this object's plugins list. Expects
        a list[] of strings as its argument. The list can be split
        by '|' entries into TODO items and DONE items. Anything after
        a second '|' will not be processed and be returned.
        Setting to an empty list will disable TODO checking.
        """
        new_todo_states = []
        new_done_states = []
        num_lists = 1
        # Process the first part of the list (delimited by '|')
        for new_state in new_states:
            if new_state == '|':
                num_lists += 1
                break
            new_todo_states.append(new_state)
        # Clean up the lists so far
        if num_lists > 1:
            new_states.remove('|')
        for todo_state in new_todo_states:
            new_states.remove(todo_state)
        # Process the second part of the list (delimited by '|')
        for new_state in new_states:
            if new_state == '|':
                num_lists += 1
                break
            new_done_states.append(new_state)
        # Clean up the second list
        if num_lists > 2:
            new_states.remove('|')
        for todo_state in new_done_states:
            new_states.remove(todo_state)
        # Write the relevant attributes
        for plugin in self.plugins:
            if plugin.__class__ == OrgNode:
                plugin.todo_list = new_todo_states
                plugin.done_list = new_done_states
        if new_states:
            return new_states  # Return any leftovers

    def get_todo_states(self, list_type="todo"):
        """
        Returns a list of todo states. An empty list means that
        instance of OrgNode has TODO checking disabled. The first argument
        determines the list that is pulled ("todo"*, "done" or "all").
        """
        all_states = []
        for plugin in self.plugins:
            if plugin.__class__ == OrgNode:
                if plugin.todo_list and (list_type == "todo" or list_type ==
                                         "all"):
                    all_states += plugin.todo_list
                if plugin.done_list and (list_type == "done" or list_type ==
                                         "all"):
                    all_states += plugin.done_list
        return list(set(all_states))

    def add_todo_state(self, new_state):
        """Appends a todo state to the list of todo states of any OrgNode plugins in
        this objects plugins list. Expects a string as its argument.

        """
        for plugin in self.plugins:
            if plugin.__class__ == OrgNode:
                plugin.todo_list.append(new_state)

    def add_done_state(self, new_state):
        """Appends a todo state to the list of todo states of any OrgNode plugins in
        this objects plugins list. Expects a string as its argument.

        """
        for plugin in self.plugins:
            if plugin.__class__ == OrgNode:
                plugin.done_list.append(new_state)

    def remove_todo_state(self, old_state):
        """
        Remove a given todo state from both the todo list and the done list.
        Returns True if the plugin was actually found.
        """
        found = False
        for plugin in self.plugins:
            if plugin.__class__ == OrgNode:
                while old_state in plugin.todo_list:
                    found = True
                    plugin.todo_list.remove(old_state)
                while old_state in plugin.done_list:
                    found = True
                    plugin.done_list.remove(old_state)
        return found

    def extract_todo_list(self, todo_list=None):
        """Extract a list of headings with TODO states specified by the first
        argument.
        """

        if todo_list is None:  # Set default
            # Kludge to get around lack of self in function declarations
            todo_list = self.get_todo_states()
        else:
            # Check to make sure all todo_list items are registered
            # with the OrgNode plugin
            for possible_state in todo_list:
                if possible_state not in self.get_todo_states("all"):
                    raise ValueError(
                        "State " + possible_state
                        + " not registered. See \
                        PyOrgMode.OrgDataStructure.add_todo_state.")
        results_list = []
        # Recursive function that steps through each node in current level,
        # looking for TODO items and then calls itself to look for
        # TODO items one level down.

        def extract_from_level(content):
            for node in content:
                # Check if it's a TODO item and add to results
                try:
                    current_todo = node.todo
                except AttributeError:
                    pass
                else:  # Handle it
                    if current_todo in todo_list:
                        new_todo = OrgTodo(node.heading,
                                           node.todo,
                                           tags=node.tags,
                                           priority=node.priority,
                                           node=node)
                        results_list.append(new_todo)
                # Now check if it has sub-headings
                try:
                    next_content = node.content
                except AttributeError:
                    pass
                else:  # Handle it
                    extract_from_level(next_content)
        extract_from_level(self.root.content)
        return results_list

    def load_from_file(self, name, form="file"):
        """
        Used to load an org-file inside this DataStructure
        """
        current = self.root
        # Determine content type and put in appropriate form
        if form == "file":
            content = open(name, 'r')
        elif form == "string":
            content = [tmp+"\n" for tmp in name.split("\n")]
        else:
            raise ValueError("Form \""+form+"\" not recognized")

        for line in content:
            for plugin in self.plugins:
                current = plugin.treat(current, line)
                if plugin.treated:  # Plugin found something
                    treated = True
                    break
                else:
                    treated = False
            if not treated and line is not None:
                # Nothing special, just content
                current.append(line)

        for plugin in self.plugins:
            current = plugin.close(current)

        if form == "file":
            content.close()

    def load_from_string(self, string):
        """A wrapper calling load_from_file but with a string instead of reading from
        a file.
        """
        self.load_from_file(string, "string")

    def save_to_file(self, name, node=None):
        """
        Used to save an org-file corresponding to this DataStructure
        """

        with open(name, 'w') as output:
            if node is None:
                node = self.root
            output.write(str(node))

    @staticmethod
    def parse_heading(heading):
        heading = heading.strip()
        r = re.compile('(.*)(?:\s+\[(\d+)/(\d+)\])(?:\s+)?')
        m = r.match(heading)
        if m:
            return {'heading': m.group(1),
                    'todo_done': m.group(2),
                    'todo_total': m.group(3)}
        else:
            return {'heading': heading}

    @staticmethod
    def get_nodes_by_priority(node, priority, found_nodes=[]):

        # print "start of get_nodes_by_priority"
        # print " node instance type: %s" % node.__class__.__name__

        if isinstance(node, OrgElement):
            # print " node.heading: %s" % node.heading
            try:
                if node.todo and node.priority == priority:
                    found_nodes.append(node)
            except AttributeError:
                # TODO: This could be a Property.  Handle it!
                pass

            for node in node.content:
                OrgDataStructure.get_nodes_by_priority(node,
                                                       priority,
                                                       found_nodes)
            return found_nodes
        else:
            return found_nodes

    @staticmethod
    def get_node_by_heading(node, heading, found_nodes=[]):

        if isinstance(node, OrgElement):
            try:
                heading_dict = OrgDataStructure.parse_heading(node.heading)
                if heading_dict['heading'] == heading.strip():
                    found_nodes.append(node)
            except AttributeError:
                # TODO: This could be a Property.  Handle it!
                pass

            for node in node.content:
                OrgDataStructure.get_node_by_heading(node,
                                                     heading,
                                                     found_nodes)
            return found_nodes
        else:
            return found_nodes
