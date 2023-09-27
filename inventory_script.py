import sys
import os
import json

cwd = os.getcwd()
sys.path.append(f'{cwd}/pylibs')
import clab_inventory

inv = clab_inventory.Inventory(f'{cwd}/inventory/inventory.yml', 'file_name')
inv.load()

print()

for k,v in inv._groups.items():
  print(k, v.children(), v.parent, v.hosts())

print()

for k,v in inv._hosts.items():
  print(k)
  print(v.groups())

print()

for item in inv.ordered_groups:
  print(item)


print('#########################################')
print(json.dumps(inv.ansible_inventory(), indent=2))

