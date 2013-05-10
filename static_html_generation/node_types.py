class NodeTypes():
    def __init__(self):
        """ This being a dict assumes that there are other
        node types that will need id alteration. if not,
        this can become less generic. """

        self.node_types_map = {'Interpretations': 'I'}
         
    def change_type_names(self, id_parts):
        """ Written originally to change the id representation
        of Interpretations on the front end vs. what is in the
        tree. The pattern may prove useful when we've fleshed
        out more node types. "1005-Interpretations" -> "I-1005"
        [ts] """

        node_elements = list(id_parts)
        for k, v in self.node_types_map.items():
            if node_elements.count(k): 
                node_elements.remove(k)
                node_elements.insert(0, v)
        return node_elements
