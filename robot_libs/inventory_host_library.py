
   
    
class InventoryHost(object):
    def __init__(self, name):
        self.name = name
        self.ordered_groups = dict()
        self.variables = dict()
        self.merged_vars = dict()

    def groups(self):
        groups = list()
        for k,v in sorted(self.ordered_groups.items()):
            groups.append(v)
        return(groups)  