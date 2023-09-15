*** Settings ***
Documentation     Testing for InventoryGroup Object
...
...               All tests contain a workflow constructed from keywords in
...               ``../robot_libs/inventory_group_library.py``.
...

Library           ../robot_libs/InventoryGroupLibrary.py


*** Test Cases ***
Good Group Creation
    Create Valid Group    tharpie
    Name Should Be        tharpie

Bad Group Creation
    Create Invalid Group    12tharpie
    Create Invalid Group    1234
    Create Invalid Group    tharpie-house
    Create Invalid Group    tharpie.house

Create Tharpie Group Create Children
    Create valid group    tharpie
    Set children          river_north lincoln_park
    Children should be    lincoln_park,river_north

Create Tharpie Group Test Duplicate Children
    Create valid group    tharpie
    Set children          river_north lincoln_park river_north lincoln_park
    Children should be    lincoln_park,river_north

#Push button
#    Push button    1
#    Result should be    1
#
#Push multiple buttons
#    Push button    1
#    Push button    2
#    Result should be    12
#
#Simple calculation
#    Push button    1
#    Push button    +
#    Push button    2
#    Push button    =
#    Result should be    3
#
#Longer calculation
#    Push buttons    5 + 4 - 3 * 2 / 1 =
#    Result should be    3
#
#Clear
#    Push button    1
#    Push button    C
#    Result should be    ${EMPTY}    # ${EMPTY} is a built-in variable



