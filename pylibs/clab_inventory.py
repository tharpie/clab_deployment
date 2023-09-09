
import os
import sys
import yaml
import traceback
import copy

def pretty_execption(class_name, func_name, tb, e):
    print(f'Exception caught:  in class={class_name} func={func_name}')
    print()
    print(' Traceback ')
    print(tb)
    print()
    print('Exception')
    print(e)
    print()
    sys.exit(1)


class Inventory(object):
    def __init__(self, inventory_fname):
        self.inventory_fname = inventory_fname
        self.groups = dict()
        self.devices = dict()
        self.inventory_yaml = dict()

        try:
            with open(self.inventory_fname) as f:
                self.inventory_yaml.update(yaml.safe_load(f))
        except Exception as e:
            tb = traceback.format_exc()
            pretty_exception(self.__name__, self.__init__.__name__, tb, e)
        
        self.__create_inventory_objects()
        self.__build_variables()


    def __create_inventory_objects(self, structure=None, groups={}, tier=0):
        if structure == None:
            structure = self.inventory_yaml

        for k,v in structure.items():
            if type(v) == dict:
                g = InventoryGroup(k)
                self.groups[k] = g

                if 'hostnames' in v.keys():
                    parent_group = groups[tier-1]
                    self.groups[parent_group].children.append(k)
                    
                    for host in v['hostnames']:
                        h = InventoryHost(host)
                        h.ordered_groups.update(groups)
                        h.ordered_groups[tier+1] = k
                        self.devices[h.name] = h

                else:
                    if tier > 0:
                        parent_group = groups[tier-1]
                        self.groups[parent_group].children.append(k)

                    _groups = copy.deepcopy(groups)
                    _tier = copy.deepcopy(tier)
                    _groups.update({tier:k})
                    _tier += 1
                    self.__create_inventory_objects(v, _groups, _tier)

            try:
                g
            except Exception as e:
                tb = traceback.format_exc()
                pretty_exception(self.__name__, self.__create_inventory_objects.__name__, tb, e)


    def __build_devices(self):
        pass

    def __build_variables(self):
        pass

'''
global:
  namerica:
    il:
      chicago:
        hostnames:
        - chi-sw1
    tx:
      houston:
        hostnames:
        - hou-sw1
''' 



class InventoryGroup(object):
    def __init__(self, name):
        self.name = name
        self.hosts = list()
        self.children = list()
        self.variables = dict()

#    def _set_child(self, g):
#        i = len(self.ordered_children.keys())
#        self.ordered_children[i] = g

#    def children(self):
#        return([self.ordered_children[k] for k in sorted(self.ordered_children.keys())])


class InventoryHost(object):
    def __init__(self, name):
        self.name = name
        self.ordered_groups = dict()
        self.variables = dict()

    def groups(self):
        groups = list()
        for k,v in sorted(self.ordered_groups.items()):
            groups.append(v)
        return(groups)    

'''
{
{
    "group001": {
        "hosts": ["host001", "host002"],
        "vars": {
            "var1": true
        },
        "children": ["group002"]
    },
    "group002": {
        "hosts": ["host003","host004"],
        "vars": {
            "var2": 500
        },
        "children":[]
    }

}

    # results of inventory script as above go here
    # ...

    "_meta": {
        "hostvars": {
            "host001": {
                "var001" : "value"
            },
            "host002": {
                "var002": "value"
            }
        }
    }
}
'''


#def iterate_and_squash(x=dict()):
#    final = dict()
#    for k,v in x.items():
#        if type(v) == str:
#            o = Inventory({k:v})
#            final[k] = v
#        elif type(v) == list:
#            final


#if __name__ == '__main__':
#    try:
#        inv_fname = os.environ.get('CLAB_INVENTORY_FNAME')
#
#    except Exception as e:
#        print('CLAB_INVENTORY_FNAME environment variable is not set')
#        sys.exit(1)


#>>> print(vars(x.details))
#{'a': '1', 'b': '2', 'c': '3'}