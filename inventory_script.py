import sys
import os
import json

cwd = os.getcwd()
sys.path.append(f'{cwd}/pylibs')
import clab_inventory

inv = clab_inventory.Inventory(f'{cwd}/inventory/inventory.yml')
inv.load()

print()

for k,v in inv.groups.items():
  print(k, v.children, v.variables, v.hosts())
  print(json.dumps(v.merged_vars, indent=2))

print()

for k,v in inv.hosts.items():
  print(k)
  print(v.groups())
  print(v.ordered_groups)
  print(json.dumps(v.merged_vars, indent=2))

print()

for item in inv.ordered_groups:
  print(item)


print('#########################################')
print(json.dumps(inv.ansible_inventory(), indent=2))

