REGTEXT = 'regtext'
APPENDIX = 'appendix'
INTERP = 'interp'

def is_appendix(id_parts):
    """ Inspect the id_parts to determine if this is an Appendix section. """
    if len(id_parts) > 2:
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
        return [transform_part(part) for part in new_id if part != 'Interpretations']
    elif is_appendix(id_parts):
        return [transform_part(part) for part in new_id]
    return new_id
