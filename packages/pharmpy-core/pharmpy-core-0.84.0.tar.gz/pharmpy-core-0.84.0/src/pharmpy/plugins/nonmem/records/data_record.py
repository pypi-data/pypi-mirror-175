"""
NONMEM data record class.
"""

from pharmpy.internals.parse import AttrToken, AttrTree
from pharmpy.model import ModelSyntaxError

from .option_record import OptionRecord


class DataRecord(OptionRecord):
    @property
    def filename(self):
        """The (raw, unresolved) path of the dataset."""
        filename = self.root.filename
        if filename.find('TEXT'):
            return str(filename)
        else:  # 'QUOTE'
            return str(filename)[1:-1]

    @filename.setter
    def filename(self, value):
        if not value:
            # erase and replace by * (for previous subproblem)
            new = [AttrToken('ASTERISK', '*')]
            nodes = []
            for child in self.root.children:
                if new and child.rule == 'ws':
                    nodes += [child, new.pop()]
                elif child.rule in {'ws', 'comment'}:
                    nodes += [child]
            self.root = AttrTree.create('root', nodes)
        else:
            # replace only 'filename' rule and quote appropriately if, but only if, needed
            filename = str(value)
            quoted = [
                ',',
                ';',
                '(',
                ')',
                '=',
                ' ',
                'IGNORE',
                'NULL',
                'ACCEPT',
                'NOWIDE',
                'WIDE',
                'CHECKOUT',
                'RECORDS',
                'RECORDS',
                'LRECL',
                'NOREWIND',
                'REWIND',
                'NOOPEN',
                'LAST20',
                'TRANSLATE',
                'BLANKOK',
                'MISDAT',
            ]
            if not any(x in filename for x in quoted):
                node = AttrTree.create('filename', {'TEXT': filename})
            else:
                if "'" in filename:
                    node = AttrTree.create('filename', {'QUOTE': '"%s"' % filename})
                else:
                    node = AttrTree.create('filename', {'QUOTE': "'%s'" % filename})
            (pre, old, post) = self.root.partition('filename')
            self.root.children = pre + [node] + post

    @property
    def ignore_character(self):
        """The comment character from ex IGNORE=C or None if not available."""
        if hasattr(self.root, 'ignchar') and self.root.ignchar.find('char'):
            chars = set()
            for option in self.root.all('ignchar'):
                char = str(option.char)
                if len(char) == 3:  # It must be quoted
                    char = char[1:-1]
                chars.add(char)
            if len(chars) > 1:
                raise ModelSyntaxError("Redefinition of ignore character in $DATA")
            else:
                return chars.pop()
        else:
            return None

    @ignore_character.setter
    def ignore_character(self, c):
        if c != self.ignore_character:
            self.root.remove('ignchar')
            char_node = AttrTree.create('char', [{'CHAR': c}])
            node = AttrTree.create('ignchar', [{'IGNORE': 'IGNORE'}, {'EQUALS': '='}, char_node])
            self.append_option_node(node)

    def ignore_character_from_header(self, label):
        """Set ignore character from a header label
        If s[0] is a-zA-Z set @
        else set s[0]
        """
        c = label[0]
        if c.isalpha():
            self.ignore_character = '@'
        else:
            self.ignore_character = c

    @property
    def null_value(self):
        """The value to replace for NULL (i.e. . etc) in the dataset
        note that only +,-,0 (meaning 0) and 1-9 are allowed
        """
        if hasattr(self.root, 'null') and self.root.null.find('char'):
            char = str(self.root.null.char)
            if char == '+' or char == '-':
                return 0
            else:
                return float(char)
        else:
            return 0

    @property
    def ignore(self):
        filters = []
        for option in self.root.all('ignore'):
            for filt in option.all('filter'):
                filters.append(filt)
        return filters

    @ignore.deleter
    def ignore(self):
        self.root.remove('ignore')

    @property
    def accept(self):
        filters = []
        for option in self.root.all('accept'):
            for filt in option.all('filter'):
                filters.append(filt)
        return filters

    @accept.deleter
    def accept(self):
        self.root.remove('accept')
