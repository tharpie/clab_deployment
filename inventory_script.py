import sys
import os
import json

cwd = os.getcwd()
sys.path.append(f'{cwd}/pylibs')
import clab_inventory

inv = clab_inventory.Inventory(f'{cwd}/inventory/inventory.yml', [f'{cwd}/inventory/groups', f'{cwd}/inventory/groups'], 'file_name', 'dir_list')
inv.load()

print()

for k,v in inv._groups.items():
  print(k, v.children(), v.parent, v.hosts())

print()

for k,v in inv._hosts.items():
  print(k)
  print(v.groups())

print()

for k,v in inv._groups_index.items():
  print(k, v)


print('#########################################')
print(json.dumps(inv.ansible_inventory(), indent=2))

