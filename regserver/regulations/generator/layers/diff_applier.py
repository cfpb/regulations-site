import json
import types
from collections import deque

class DiffApplier(object):
    def __init__(self):
        self.diff = json.load(open('/vagrant/diff.json'))


    def apply_diff(self, original, label):
        if label in self.diff:
            text_diffs = self.diff[label]['text']
            oq = [deque([c]) for c in original]

            for d in text_diffs:
                if d[0] == u'insert':
                    _, pos, new_text = d
                    oq[pos].extend(['<ins>', new_text + ' ', '</ins>'])
                if d[0] == u'delete':
                    _, s, e = d
                    oq[s].appendleft('<del>')
                    oq[e].append('</del>')
                if isinstance(d[0], types.ListType):
                    if d[0][0] == u'delete':
                        _, s, e = d[0]
                        oq[s].appendleft('<del>')
                        oq[e].append('</del>')
                    if d[1][0] == u'insert':
                        _, pos, new_text = d[1]
                        oq[pos].extend(['<ins>', new_text + ' ', '</ins>'])
            modified_text = ''.join([''.join(d) for d in oq])
            return modified_text
        return original
