def to_markup_id(id_parts):
    """Given the id parts from the JSON tree, convert to an id that can
    be used in the front end"""
    new_id = list(id_parts)
    if 'Interpretations' in id_parts:
        new_id = ['I'] + new_id
        return [part.replace('(', '').replace(')', '') 
            for part in new_id if part != 'Interpretations']
    return new_id
