#vim: set encoding=utf-8
from itertools import takewhile

APPENDIX = u'appendix'
INTERP = u'interp'
REGTEXT = u'regtext'
SUBPART = u'subpart'
EMPTYPART = u'emptypart'


def transform_part(p):
    """ Transform a part of the id of a node. """
    return p.replace('(', '').replace(')', '')


def to_markup_id(id_parts):
    """Given the id parts from the JSON tree, convert to an id that can
    be used in the front end"""
    new_id = list(id_parts)
    if type_from_label(id_parts) in (APPENDIX, INTERP):
        return [transform_part(part) for part in new_id]
    return new_id


def type_from_label(label):
    """Given a list of label parts, determine the associated node's type"""
    if 'Interp' in label:
        return INTERP
    if label[-1] == 'Subpart':
        return EMPTYPART
    if 'Subpart' in label:  # but not the final segment
        return SUBPART
    if len(label) > 1 and label[1][:1].isalpha():
        return APPENDIX
    return REGTEXT


def label_to_text(label, include_section=True, include_marker=False):
    """Convert a label:list[string] into a human-readable string"""
    if len(label) == 1:
        return 'Regulation %s' % label[0]

    # Use short circuiting to grab the *first* type of label that matches
    return (_l2t_subterp(label) or _l2t_interp(label) or _l2t_appendix(label)
            or _l2t_section(label, include_section, include_marker))


def _l2t_subterp(label):
    """Helper function converting subterp labels to text. Assumes label has
    more then one segment"""
    if label[1:] == ['Subpart', 'Interp']:
        return 'Interpretations for Regulation Text of Part ' + label[0]
    elif label[1:] == ['Appendices', 'Interp']:
        return 'Interpretations for Appendices of Part ' + label[0]
    elif len(label) == 4 and label[1] == 'Subpart' and label[3] == 'Interp':
        interpretations_for = 'Interpretations for Subpart '
        return interpretations_for + label[2] + ' of Part ' + label[0]


def _l2t_interp(label):
    """Helper function converting interpretation labels to text. Assumes
    _l2t_subterp failed"""
    if 'Interp' in label:
        # Interpretation
        prefix = list(takewhile(lambda l: l != 'Interp', label))
        suffix = label[label.index('Interp')+1:]
        if len(prefix) == 1:
            return 'Supplement I to Part %s' % prefix[0]
        elif suffix:
            return 'Comment for %s-%s' % (label_to_text(prefix),
                                          '.'.join(suffix))
        else:
            return 'Comment for %s' % label_to_text(prefix)


def _l2t_appendix(label):
    """Helper function converting appendix labels to text. Assumes
    _l2t_subterp and _l2t_interp failed"""
    if type_from_label(label) == APPENDIX:
        # Appendix
        if len(label) == 2:  # e.g. 225-B
            return 'Appendix ' + label[1] + ' to Part ' + label[0]
        elif len(label) == 3:  # e.g. 225-B-3
            return 'Appendix %s-%s' % tuple(label[1:])
        else:  # e.g. 225-B-3-a-4-i
            return 'Appendix %s-%s(%s)' % (label[1], label[2],
                                           ')('.join(label[3:]))


def _l2t_section(label, include_section, include_marker):
    """Helper function converting section labels to text. Assumes
    _l2t_subterp, _l2t_interp, and _l2t_appendix failed"""
    if include_marker:
        marker = u'§ '
    else:
        marker = ''

    if include_section:
        # Regulation Text with section number
        if len(label) == 2:  # e.g. 225-2
            return marker + '.'.join(label)
        else:  # e.g. 225-2-b-4-i-A
            return marker + '%s.%s(%s)' % (label[0], label[1],
                                           ')('.join(label[2:]))
    else:
        # Regulation Text without section number
        if len(label) == 2:  # e.g. 225-2
            return marker + label[1]
        else:  # e.g. 225-2-b-4-i-A
            return marker + '%s(%s)' % (label[1], ')('.join(label[2:]))
