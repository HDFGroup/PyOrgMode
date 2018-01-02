from PyOrgMode import OrgDataStructure, OrgDrawer, OrgNode, OrgSchedule

base = OrgDataStructure()

new_todo = OrgNode.Element()
new_todo.heading = "I am a new todo item"
new_todo.tags=["things", "important"]
new_todo.level = 1
new_todo.todo = "TODO"

_sched = OrgSchedule()
_sched._append(new_todo,
               _sched.Element(scheduled="<2015-08-01 Sat 12:00-13:00>"))
_sched._append(new_todo,
               _sched.Element(deadline="<2015-08-01 Sat 12:00-13:00>"))

_props = OrgDrawer.Element("LOGBOOK")
# Add a properties drawer
_props.append(
    OrgDrawer.Element(
        "- State \"SOMEDAY\"    from \"TODO\"     [2015-07-01 Wed 09:45]"))
# Append the properties to the new todo item
new_todo.append_clean(_props)

_props = OrgDrawer.Element("PROPERTIES")
# Add a properties drawer
_props.append(OrgDrawer.Property("FRUITS", "pineapples"))
_props.append(OrgDrawer.Property("NAMES", "bob, sally"))
# Append the properties to the new todo item
new_todo.append_clean(_props)

base.root.append_clean(new_todo)

base.save_to_file("example1.org")
