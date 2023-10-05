
import os
import sys
import yaml
import traceback
import copy
import keyword
import json


def pretty_exception(class_name, func_name, tb, e):
    print(f'Exception caught:  in class={class_name} func={func_name}')
    print()
    print(' Traceback ')
    print(tb)
    print()
    print('Exception')
    print(e)
    print()
    sys.exit(1)


def is_name_valid(name):
    valid = True
    if type(name) != str:
        valid = False
    elif name in keyword.kwlist:
        valid = False            
    elif '.' in name:
        valid = False
    elif ' ' in name:
        valid = False
    elif '-' in name:
        valid = False
    elif name.isnumeric():
        valid = False
    elif name[0].isnumeric():
        valid = False
    
    return(valid)

def merge_variables(orig, update=dict()):
    if type(orig) != dict or type(update) != dict:
        raise Exception(f'input for merge_variables needs two dicts orig={type(orig)} update={type(update)}')

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
            elif type(u_v) == dict or isinstance(u_v, DotDict):
                variables[u_k] = merge_variables(variables[u_k], u_v)
    
    return(variables)

def load_from_dict(d):
    _vars = dict()
    if type(d) != dict:
        raise Exception(f'input for load_from_dict type={type(d)}, please provide dict')
    _vars.update(d)
    return(_vars)

def load_from_file(fname):
    _vars = dict()
    if not os.path.exists(fname):
        raise Exception(f'fname={fname} is not a valid path')
    try:
        with open(fname) as f:
            _vars.update(yaml.safe_load(f))
    except Exception as e:
        tb = traceback.format_exc()
        raise Exception(f'error in load_from_file reading={fname}', tb)
    return(_vars)

def load_from_file_list(flist):
    _vars = dict()
    if type(flist) != list:
        raise Exception(f'input for load_from_file_list type={type(flist)}, please provide list')
    for fname in flist:
        _vars.update({label_from_fname(fname): load_from_file(fname)})
    return(_vars)

def load_from_url(uri):
    _vars = dict()
    return(_vars)

def load_from_dir(d):
    flist = list()
    if not os.path.exists(d):
        raise Exception(f'dir={d} is not a valid path')
    for fname in os.listdir(d):
        flist.append(f'{d}/{fname}')    
    return(load_from_file_list(flist))

def load_from_dir_list(dlist):
    _vars = dict()
    if type(dlist) != list:
        raise Exception(f'input for load_from_dir_list type={type(dlist)}, please provide list')
    for dirname in dlist:
        _vars.update(load_from_dir(dirname))
    return(_vars)

def label_from_fname(fname):
    slash_index = 0 if fname.rfind('/') == -1 else fname.rfind('/')
    dot_index = fname.rfind('.')
    if dot_index == -1:
        label = fname[slash_index+1:]
    else:
        label = fname[slash_index+1:dot_index]
    return(label)


LOAD_FUNCTIONS = {
    'dict': load_from_dict,
    'file_name': load_from_file,
    'file_list': load_from_file_list,
    'dir': load_from_dir,
    'dir_list': load_from_dir_list,
    'url': load_from_url
}

class InventoryGroup(object):
    def __init__(self, name):
        self.name = name.lower()
        if not self._is_valid():
            raise Exception(f'{name} has invalid InventoryGroup name')

        self.set_children = set()
        self.set_hosts = set()
        self.parent = None
        self.hosts = self._hosts
        self.children = self._children
        self.variables = dict()
        self._vars = dict()

    def _is_valid(self):
        return(is_name_valid(self.name))

    def _add_child(self, child):
        self.set_children.add(child)

    def _add_children(self, children):
        for c in list(children):
            self._add_child(c)        

    def _add_host(self, host):
        self.set_hosts.add(host)

    def _add_hosts(self, hosts):
        for h in list(hosts):
            self._add_host(h)

    def _set_parent(self, parent):
        self.parent = parent

    def _hosts(self):
        return(list(sorted(self.set_hosts)))

    def _children(self):
        return(list(sorted(self.set_children)))

    def _parent(self):
        return(list(sorted(self.set_parent)))

    def _load_variables(self, input, input_type):
        if input_type not in LOAD_FUNCTIONS.keys():
            raise Exception(f'{input_type} is not supported. Specify one of the following {str(LOAD_FUNCTIONS.keys())}')
        else:
            self._vars = LOAD_FUNCTIONS[input_type](input)
            self.variables = copy.deepcopy(self._vars)

    def _merge_vars(self, update=dict()):
        self.variables = merge_variables(self.variables, update)


class InventoryHost(object):
    def __init__(self, name):
        self.name = name.lower()
        self.groups = self._groups
        self.ordered_groups = dict()
        self.variables = dict()
        self._vars = dict()

    def _add_group(self, group_name):
        index = len(self.ordered_groups)
        self.ordered_groups[index] = group_name

    def _add_groups(self, groups):
        for g in list(groups):
            self._add_group(g)

    def _groups(self):
        groups = list()
        for k,v in sorted(self.ordered_groups.items()):
            groups.append(v)
        return(groups)  

    def _load_variables(self, input, input_type):
        if input_type not in LOAD_FUNCTIONS.keys():
            raise Exception(f'{input_type} is not supported. Specify one of the following {str(LOAD_FUNCTIONS.keys())}')
        else:
            self._vars = LOAD_FUNCTIONS[input_type](input)
            self.variables = copy.deepcopy(self._vars)

    def _merge_vars(self, update=dict()):
        self.variables = merge_variables(self.variables, update)


class Inventory(object):
    def __init__(self, label, inventory_input, input_type):
        self.label = label
        self.inventory_input = inventory_input
        self.input_type = input_type
        self._vars = dict()

        try:
            self._vars = LOAD_FUNCTIONS[input_type](inventory_input)
        except Exception as e:
            tb = traceback.format_exc()
            pretty_exception('Inventory (class)', __name__, tb, e)

        self._groups = dict()
        self._hosts = dict()
        self._groups_index = dict()
    
    def groups(self):
        groups = list()
        for k,v in sorted(self._groups_index.items(), key=lambda x: x[1]):
            groups.append(k)
        return(groups)

    def group(self, name):
        return(self._groups[name])

    def group_index(self, name):
        return(self._groups_index[name])

    def hosts(self):
        hosts = list()
        for k,v in sorted(self._hosts.items()):
            hosts.append(k)
        return(hosts)
    
    def host(self, name):
        return(self._hosts[name])

    def load(self, vars_input, input_type):
        self._create_inventory_objects()
        self._load_variables(vars_input, input_type)
        #self._merge_group_vars()
        #self._merge_host_vars()

    def _create_group_object(self, name, parent=None):
        g = InventoryGroup(name)
        index = len(self._groups)
        self._groups[name] = g
        self._groups_index[name] = index

    def _create_host_object(self, name):
        h = InventoryHost(name)
        self._hosts[name] = h

    def _get_group_parent_tree(self, group_name, groups=[]):
        if group_name in self._groups.keys():
            parent = self._groups[group_name].parent
            if parent == None:
                groups.append(group_name)
            else:
                self._get_group_parent_tree(parent, groups)        
        return(sorted(groups, reverse=True))

    def _create_inventory_objects(self, nested=None, parent=None):
        if nested == None:
            nested = self._vars

        for k,v in nested.items():
            label = k.lower()
            if type(v) == dict:
                self._create_group_object(label)
                if self._groups_index[label] > 0:
                    self._groups[label]._set_parent(parent)
                    self._groups[parent]._add_child(label)

                if 'hostnames' in v.keys():
                    for host in v['hostnames']:
                        hostname = host.lower()
                        self._create_host_object(hostname)
                        groups = self._get_group_parent_tree(label)
                        self._hosts[hostname]._add_groups(groups)
                        for group in groups:
                            self._groups[group]._add_host(hostname)
                else:
                    self._create_inventory_objects(v, label)
        
    def _load_variables(self, vars_input, vars_type):
        object_vars = LOAD_FUNCTIONS[vars_type](vars_input)

        for h in self.hosts():
            if h in self.object_vars.keys():
                _vars = self.object_vars[h]
                host_obj = self.host(h)
                if 'extra_groups' in _vars.keys():
                    for group_name in _vars['extra_groups']:
                        self._create_group_object(group_name)
                        host_obj._add_group(group_name)
                host_obj._load_variables(_vars, 'dict')
        
        for g in self.groups():
            if g in self.object_vars.keys():
                _vars = self.object_vars[g]
                group_obj = self.group(g)
                group_obj._load_variables(_vars, 'dict')
    
    def _merge_group_vars(self):
        for group, index in sorted(self._groups_index.items(), key=lambda x: x[1]):
        #for group_name in self.ordered_groups:
            g = self._groups[group]
            if g.parent != None:
                g._merge_vars(self._groups[g.parent].variables)

            #if len(g.children) > 0:
            #    for c in g.children:
            #        self._groups[c]._merge_vars()
            #        g._merge_vars(self._groups[c].variables)
            #        self.groups[c].merged_vars = child_merged_vars
            #g.merged_vars = merged_vars

    def _merge_host_vars(self):
        for name, host in self._hosts.items():
        #for k,v in self.hosts.items():
            groups = host.groups()
            #host_vars = dict()
            for g in groups:
                host._merge_vars(self._groups[g].variables)

                #host_vars.update(self.__merge_variables(host_vars, copy.deepcopy(self.groups[g].merged_vars)))
                
            #host_vars.update(self.__merge_variables(copy.deepcopy(v.merged_vars), copy.deepcopy(self.groups[g].merged_vars)))
            #v.merged_vars = host_vars

    def ansible_inventory(self):
        ansible_vars = dict()
        ansible_vars['_meta'] = dict()
        ansible_vars['_meta']['hostvars'] = dict()
 
        for k,v in self._groups.items():
            group = dict()
            group.update({'children': v.children()})
            group.update({'vars': v.variables})
            group.update({'hosts': v.hosts()})
            ansible_vars.update({k:group})

        for k,v in self._hosts.items():
            host = dict()
            host.update(v.variables)
            ansible_vars['_meta']['hostvars'].update({k:host})

        return(ansible_vars)

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
