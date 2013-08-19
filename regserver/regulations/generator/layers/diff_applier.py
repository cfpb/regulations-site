import json
import types
from collections import deque

class DiffApplier(object):

    INSERT = u'insert'
    DELETE = u'delete'

    def __init__(self):
        self.diff = json.load(open('/vagrant/diff.json'))


    def apply_diff(self, original, label):
        if label in self.diff:
            if 'text' in self.diff[label]:
                text_diffs = self.diff[label]['text']
                oq = [deque([c]) for c in original]

                for d in text_diffs:
                    if d[0] == self.INSERT:
                        _, pos, new_text = d
                        if pos == len(oq):
                            oq[pos-1].extend(['<ins>', new_text + ' ', '</ins>'])
                        else:
                            oq[pos].extend(['<ins>', new_text + ' ', '</ins>'])
                    if d[0] == self.DELETE:
                        _, s, e = d
                        oq[s].appendleft('<del>')
                        oq[e-1].append('</del>')
                    if isinstance(d[0], types.ListType):
                        if d[0][0] == self.DELETE and d[1][0] == self.INSERT:
                            # Text replace scenario. 
                            _, s, e = d[0]
                            oq[s].appendleft('<del>')
                            oq[e-1].append('</del>')

                            _, _, new_text = d[1]
                            # Place the new text at the end of the delete for readability.
                            oq[e-1].extend(['<ins>', new_text + '', '</ins>'])
                modified_text = ''.join([''.join(d) for d in oq])
                return modified_text
        return original
