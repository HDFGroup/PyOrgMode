
import re

from PyOrgMode import OrgElement, OrgPlugin

'''
See https://orgmode.org/worg/dev/org-element-api.html

:key
    Keyword's name (string).
:value
    Keyword's value (string).
'''

class OrgKeyword(OrgPlugin):
    """A Plugin for keywords"""
    def __init__(self):
        OrgPlugin.__init__(self)
        # from org-element.el
        exp = "^[ \t]*#\+(HEADERS|NAME|TITLE|OPTIONS)" + \
	      "(?: +(\S-+))?" + \
	      "((?: +(?:-l \".*?\"|[-+][A-Za-z]))+)?" + \
	      "(.*)[ \t]*$"
        self.regexp = re.compile(exp)

    def _treat(self, current, line):
        keyword = self.regexp.search(line)

        if keyword:  # Creating a keyword
            s = keyword.group(0)
            a = s.split()
            keyword = a[0].strip()[2:-1]
            name = ""
            value = ""
            if keyword == "NAME":  # only NAME has a name
                name = a[1].strip()
            else:
                value = " ".join(a[1:])
            current = self._append(current,
                                   OrgKeyword.Element(keyword, name, value))
            # go home
            current = current.parent

        return current

    class Element(OrgElement):
        """A keyword, a pair of a keyword name and a keyword value"""
        TYPE = "KEYWORD"

        def __init__(self, keyword="KEYWORD", name="", value=""):
            OrgElement.__init__(self)
            self.keyword = keyword  # remember the kind of keyword
            self.name = name
            self.value = value
            
        def _output(self):
            output = ""
            if self.keyword == "NAME":
                output = "#+NAME: {}\n".format(self.name)
            else:
                output = "#+{}: {}\n".format(self.keyword, self.value)
            return output
