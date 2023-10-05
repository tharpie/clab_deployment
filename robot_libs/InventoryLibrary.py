import sys
import os
import json
import deepdiff
sys.path.append(f'{os.getcwd()}/pylibs')
import clab_inventory


class InventoryLibrary(object):
    """Test library for testing Inventory logic.

    Interacts with Inventory object using its method(s).
    """
    def __init__(self):
        self._inventory = None

    def create_valid_inventory(self, base, object_vars, vars_type, object_vars_type=None):
        self._inventory = clab_inventory.Inventory(base, object_vars, vars_type, object_vars_type)
    
    def merge_variables(self, update_vars):
        self._inventory._merge_vars(update_vars)

    def create_inventory_objects(self):
        self._inventory._create_inventory_objects()

    def load_merge_variables(self):
        self._inventory._load_merge_variables()

    def host_variables_should_be(self, hostname, expected):
        e = expected
        h = self._inventory.group(hostname).variables
        self.expectation(h, e)

    def groups_should_be(self, expected):
        e = expected
        g = self._inventory.groups()
        self.expectation(g, e)

    def hosts_should_be(self, expected):
        e = expected
        h = self._inventory.hosts()
        self.expectation(h, e)

    def children_should_be(self, parent_name, expected):
        e = expected
        c = self._inventory.group(parent_name).children()
        self.expectation(c, e)

    def parent_should_be(self, group_name, expected):
        e = expected
        p = self._inventory.group(group_name).parent
        self.expectation(p, e)

    def private_variables_should_be(self, expected):
        e = expected
        v = self._inventory._vars
        self.expectation(v, e)

    def private_object_variables_should_be(self, expected):
        e = expected
        v = self._inventory._object_vars
        self.expectation(v, e)

    def expectation(self, a, e):
        if e != a:
            diff = deepdiff.DeepDiff(a, e, verbose_level=2)
            raise AssertionError(f'Diff=\n{diff.pretty()}\n')
