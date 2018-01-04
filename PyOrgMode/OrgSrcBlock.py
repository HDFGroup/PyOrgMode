
import re

from PyOrgMode import OrgElement, OrgPlugin

'''
See https://orgmode.org/worg/dev/org-element-api.html

:label-fmt
    Format string used to write labels in current block, if different from
    org-coderef-label-format (string or nil).
:language
    Language of the code in the block, if specified (string or nil).
:number-lines
    Non-nil if code lines should be numbered. A new value starts numbering
    from 1 wheareas continued resume numbering from previous numbered block
    (symbol: new, continued or nil).
:parameters
    Optional header arguments (string or nil).
:preserve-indent
    Non-nil when indentation within the block mustn't be modified upon export
    (boolean).
:retain-labels
    Non-nil if labels should be kept visible upon export (boolean).
:switches
    Optional switches for code block export (string or nil).
:use-labels
    Non-nil if links to labels contained in the block should display the label
    instead of the line number (boolean).
:value
    Source code (string).
'''

class OrgSrcBlock(OrgPlugin):
    """A Plugin for source blocks"""
    def __init__(self):
        OrgPlugin.__init__(self)
        # from org-element.el
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
            if end_srcblk:
                # extract the souce code (last element is the end tag)
                current.value = "\n".join(current.content[:-1])
                # clear the content
                current.content.clear()
                # go home
                current = current.parent
        elif srcblk:  # Creating a srcblk
            s = srcblk.group(0)
            a = s.split()
            # language follows the #+BEGIN_SRC tag
            language = a[1].strip()
            # parameters are next
            parameters = []
            if len(a) > 2:
                parameters = " ".join(a[2:])
            current = self._append(current,
                                   OrgSrcBlock.Element(language,
                                                       parameters))
        else:
            self.treated = False
            return current
        # It is a srcblk, change the current also (even if not modified)
        return current

    class Element(OrgElement):
        """A source block, containing parameters and source code in a certain
           language"""
        TYPE = "SRC_BLOCK"

        def __init__(self,
                     language="klingon",
                     parameters = [],
                     value = "\"Hello, World!\""):
            OrgElement.__init__(self)
            self.language = language
            self.parameters = parameters
            self.value = value
            
        def _output(self):
            output = "#+BEGIN_SRC {} {}\n{}\n#+END_SRC".format(self.language,
                                                               self.parameters,
                                                               self.value)
            return output
