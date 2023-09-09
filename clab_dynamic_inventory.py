import sys
import os

cwd = os.getcwd()
sys.path.append(f'{cwd}/pylibs')
import clab_inventory

inv = clab_inventory.Inventory(f'{cwd}/inventory/inventory.yml')

print()

for k,v in inv.groups.items():
  print(k, v.children)

print()

for k,v in inv.devices.items():
  print(k)
  print(v.groups())

