APPENDIX = u'appendix'
INTERP = u'interp'
REGTEXT = u'regtext'
SUBPART = u'subpart'
EMPTYPART = u'emptypart'


def is_appendix(id_parts):
    """ Inspect the id_parts to determine if this is an Appendix section. """
    if len(id_parts) > 1:
        return id_parts[1].isalpha()
    return False


def transform_part(p):
    """ Transform a part of the id of a node. """
    return p.replace('(', '').replace(')', '')


def to_markup_id(id_parts):
    """Given the id parts from the JSON tree, convert to an id that can
    be used in the front end"""
    new_id = list(id_parts)
    if 'Interpretations' in id_parts:
        new_id = ['I'] + new_id
        return [transform_part(part) for part in new_id
                if part != 'Interpretations']
    elif is_appendix(id_parts):
        return [transform_part(part) for part in new_id]
    return new_id

def label_to_text(label):
    """Convert a label:list[string] into a human-readable string"""
    if 'Interp' in label:
        # Interpretation
        prefix = list(takewhile(lambda l: l != 'Interp', label))
        suffix = label[label.index('Interp')+1:]
        if suffix:
            return 'Comment for %s-%s' % (label_to_text(prefix),
                                      '.'.join(suffix))
        else:
            return 'Comment for %s' % label_to_text(prefix)
    elif label[1].isalpha():
        # Appendix
        if len(label) == 2: # e.g. 225-B
            return 'Appendix ' + label[1]
        elif len(label) == 3: # e.g. 225-B-3
            return 'Appendix %s-%s' % label[1:]
        else: # e.g. 225-B-3-a-4-i
            return 'Appendix %s-%s(%s)' % (label[1], label[2],
                                           ')('.join(label[3:]))
    else:
        # Regulation Text
        if len(label) == 2: # e.g. 225-2
            return '.'.join(label)
        else: # e.g. 225-2-b-4-i-A
            return '%s.%s(%s)' % (label[0], label[1], ')('.join(label[2:]))
