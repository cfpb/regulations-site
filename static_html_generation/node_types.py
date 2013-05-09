import sys
class NodeTypes():
    def __init__(self):
        self.node_types_map = {'Interpretations': 'I'}
         
    def change_type_names(self, id_parts):
        for k, v in self.node_types_map.items():
            if id_parts.count(k): 
                id_parts.remove(k)
                id_parts.insert(0, v)
        return "-".join(id_parts)

 
