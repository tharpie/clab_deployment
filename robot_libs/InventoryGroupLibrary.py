import sys
import os
import json
import deepdiff
sys.path.append(f'{os.getcwd()}/pylibs')
import clab_inventory


#class InventoryGroup(object):
#    def __init__(self, name):
#        self.name = name
#        if not self._is_valid():
#            raise Exception(f'{name} has invalid InventoryGroup name')
#
#        self.set_children = set()
#        self.set_hosts = set()
#        self.hosts = self._hosts
#        self.children = self._children
#        self.variables = dict()
#        self._vars = dict()
#        self._supported_types = ['dict', 'file_name', 'url']
#
#    def _is_valid(self):
#        return(is_name_valid(self.name))
#
#    def _add_child(self, child):
#        self.set_children.add(child)
#        return()
#    
#    def _add_host(self, host):
#        self.set_hosts.add(host)
#        return()
#    
#    def _hosts(self):
#        return(list(sorted(self.set_hosts)))
#
#    def _children(self):
#        return(list(sorted(self.set_children)))
#
#    def _load_variables(self, variables, var_type):
#        self._vars = load_variables(variables, var_type)
#        self.variables = copy.deepcopy(self._vars)
#
#    def _merge_vars(self, update=dict()):
#        self.variables = merge_variables(self.variables, update)


class InventoryGroupLibrary(object):
    """Test library for testing InventoryGroup logic.

    Interacts with InventoryGroup object using its method(s).
    """

    def __init__(self):
        self._group = None

    def create_valid_group(self, name):
        self._group = clab_inventory.InventoryGroup(name)
    
    def create_invalid_group(self, name):
        try:
            self._group = clab_inventory.InventoryGroup(name)
        except Exception as e:
            return(str(e))
        else:
            raise AssertionError(f'creating a group with {name} should have caused an error but did not')

    def set_children(self, child):
        self._group._add_child(child)

    def set_host(self, host):
        self._group._add_host(host)

    def name_should_be(self, expected):
        if self._group.name != expected:
            raise AssertionError(f'{self._group.name} != {expected}')

    def set_variables(self, variables, var_type):
        if var_type == 'file_name':
            variables = os.path.realpath(f'{os.getcwd()}/{variables}')
        self._group._load_variables(variables, var_type)

    def merge_variables(self, update_vars):
        self._group._merge_vars(update_vars)
    
    def children_should_be(self, expected):
        e = expected
        c = sorted(list(self._group.children()))
        if e != c:
            raise AssertionError(f'EXPECTED={str(e)}\n!=\nACTUAL={str(c)}')

    def hosts_should_be(self, expected):
        e = expected
        h = sorted(list(self._group.hosts()))
        if e != h:
            raise AssertionError(f'EXPECTED={str(e)}\n!=\nACTUAL={str(h)}')

    def variables_should_be(self, expected):
        e = expected
        v = self._group.variables
        if e != v:
            diff = deepdiff.DeepDiff(e,dict(v))
            raise AssertionError(f'Diff=\n{diff.pretty()}\n')