
import re

from PyOrgMode import OrgElement, OrgPlugin


class OrgSrcBlock(OrgPlugin):
    """A Plugin for source blocks"""
    def __init__(self):
        OrgPlugin.__init__(self)
        begin_exp = "^[ \t]*#\+BEGIN_SRC" + \
	            "(?: +(\S-+))?" + \
	            "((?: +(?:-l \".*?\"|[-+][A-Za-z]))+)?" + \
	            "(.*)[ \t]*$"
        self.begin_regexp = re.compile(begin_exp)
        end_exp = "^[ \t]*#\+END_SRC"
        self.end_regexp = re.compile(end_exp)

    def _treat(self, current, line):
        srcblk = self.begin_regexp.search(line)

        if isinstance(current, OrgSrcBlock.Element):  # We are in a srcblk
            self._append(current,
                         line.rstrip("\n"))
            end_srcblk = self.end_regexp.search(line)
            if end_srcblk:  # Go home
                current = current.parent
        elif srcblk:  # Creating a srcblk
            current = self._append(current,
                                   OrgSrcBlock.Element(srcblk.group(0)))
        else:
            self.treated = False
            return current
        # It is a srcblk, change the current also (even if not modified)
        return current

    class Element(OrgElement):
        """A source block, containing parameters and source code"""
        TYPE = "SRC_BLOCK"

        def __init__(self, name=""):
            OrgElement.__init__(self)
            self.name = name

        def _output(self):
            output = ":" + self.name + ":\n"
            for element in self.content:
                output = output + str(element) + "\n"
            output = output + self.indent
            return output
