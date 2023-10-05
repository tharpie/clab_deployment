import sys
import os
import deepdiff
sys.path.append(f'{os.getcwd()}/pylibs')
import clab_inventory


class InventoryFunctions(object):
    """Test library for testing Inventory Helper Functions.

    Interacts with clab_inventory using its non-class method(s).
    """
    def __init__(self):
        self._input = ''
        self._str_status = ''
        self._dict_status = dict()

    def is_name_valid(self, name):
        self._input = name
        self._str_status = clab_inventory.is_name_valid(name)

    def label_from_fname(self, fname):
        self._input = fname
        self._str_status = clab_inventory.label_from_fname(fname)

    def merge_variables(self, update):
        self._dict_status = clab_inventory.merge_variables(self._dict_status, update)

    def load_from_dict(self, d):
        self._dict_status = clab_inventory.load_from_dict(d)

    def load_from_file(self, fname):
        self._dict_status = clab_inventory.load_from_file(fname)

    def load_from_file_list(self, flist):
        self._dict_status = clab_inventory.load_from_file_list(flist)

    def load_from_dir(self, dir):
        self._dict_status = clab_inventory.load_from_dir(dir)

    def load_from_dir_list(self, dirlist):
        self._dict_status = clab_inventory.load_from_dir_list(dirlist)

    def name_result_should_be(self, expected):
        e = expected
        v = self._str_status
        if e != v:
            diff = deepdiff.DeepDiff(e, v, verbose_level=2)
            raise AssertionError(f'input={self._input}\n\nDiff=\n{diff.pretty()}\n')

    def dict_result_should_be(self, expected):
        e = expected
        v = self._dict_status
        if e != v:
            diff = deepdiff.DeepDiff(e, v, verbose_level=2)
            raise AssertionError(f'{e}\n{v}\nDiff=\n{diff.pretty()}\n')
