
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
        self.hosts = dict()
        self.inventory_yaml = dict()
        self.inventory_basedir = self.inventory_fname[:self.inventory_fname.rfind('/')]

    
    def load(self):        
        self.__read_inventory_file()
        self.__create_inventory_objects()
        self.__load_variables()
        self.__merge_group_vars()
        self.__merge_host_vars()

    def __read_inventory_file(self):
        try:
            with open(self.inventory_fname) as f:
                self.inventory_yaml.update(yaml.safe_load(f))
        except Exception as e:
            tb = traceback.format_exc()
            pretty_exception(self.__name__, self.__init__.__name__, tb, e)

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
                        h.ordered_groups[tier] = k
                        self.hosts[h.name] = h

                        for order,group_name in sorted(h.ordered_groups.items()):
                            self.groups[group_name].hosts.append(host)
                
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
            

    def __load_variables(self):
        hosts_files = {}
        for fname in os.listdir(f'{self.inventory_basedir}/hosts'):
            if '.' in fname:
                host = fname[:fname.rfind('.')]
            else:
                host = fname
            
            hosts_files[host] = fname

        for k,v in self.hosts.items():
            if k in hosts_files:
                with open(f'{self.inventory_basedir}/hosts/{hosts_files[k]}') as y:
                    yaml_vars = yaml.safe_load(y)

                    if 'extra_groups' in yaml_vars.keys():
                        extra_indices = [ i + len(self.hosts[k].ordered_groups.keys()) for i in range(0,len(yaml_vars['extra_groups']))]
                        print(v.ordered_groups)
                        print(yaml_vars['extra_groups'])
                        print(extra_indices)
                        for group_name in yaml_vars['extra_groups']:
                            g = InventoryGroup(group_name)
                            g.hosts.append(k)
                            self.groups[group_name] = g
                            self.hosts[k].ordered_groups.update({extra_indices.pop(0):group_name})
                
                v.variables.update(yaml_vars)
                v.merged_vars.update(yaml_vars)


        group_files = {}
        for fname in os.listdir(f'{self.inventory_basedir}/groups'):
            if '.' in fname:
                group = fname[:fname.rfind('.')]
            else:
                group = fname
            
            group_files[group] = fname
        
        for k,v in self.groups.items():
            if k in group_files:
                print(k, group_files[k])
                with open(f'{self.inventory_basedir}/groups/{group_files[k]}') as y:
                    yaml_vars = yaml.safe_load(y)
                    v.variables.update(yaml_vars)
                    v.merged_vars.update(yaml_vars)
    

    def __merge_variables(self, orig, update=dict()):
        variables = copy.deepcopy(orig)

        for u_k, u_v in update.items():
            if u_k not in orig.keys():
                variables.update({u_k:u_v})
            else:
                if type(u_v) == str:
                    variables[u_k] = u_v
                elif type(u_v) == list:
                    for item in u_v:
                        if item not in variables[u_k]:
                            variables[u_k].append(item)
                elif type(u_v) == dict:
                    self.__merge_variables(variables, u_v)

        return(variables)

    def __merge_group_vars(self):
        for k,v in self.groups.items():
            merged_vars = copy.deepcopy(v.merged_vars)

            if len(v.children) > 0:
                for c in v.children:
                    if c in self.groups.keys():
                        child_merged_vars = self.__merge_variables(merged_vars, copy.deepcopy(self.groups[c].merged_vars))
                        self.groups[c].merged_vars = child_merged_vars

            v.merged_vars = merged_vars

    def __merge_host_vars(self):
        for k,v in self.hosts.items():
            groups = v.groups()
            host_vars = dict()
            for g in groups:
                host_vars.update(self.__merge_variables(host_vars, copy.deepcopy(self.groups[g].merged_vars)))
                
            host_vars.update(self.__merge_variables(copy.deepcopy(v.merged_vars), copy.deepcopy(self.groups[g].merged_vars)))
            v.merged_vars = host_vars            


class InventoryGroup(object):
    def __init__(self, name):
        self.name = name
        self.hosts = list()
        self.children = list()
        self.variables = dict()
        self.merged_vars = dict()


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