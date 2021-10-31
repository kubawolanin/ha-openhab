## Map Item types

Color - light
Contact - binary_sensor
DateTime - sensor
Dimmer - light
Group - depending on groupType
Image - camera
Location - zone
Number - sensor
Number:<dimension> - sensor
Player - media_player
Rollershutter - cover
String - sensor
Switch - switch

https://www.openhab.org/docs/concepts/items.html

https://python-openhab.readthedocs.io/en/latest/api_items/

https://github.com/sim0nx/python-openhab

# TODO

- [ ] Connect to OH instance
- [ ] Username/Password vs Token authentication
- [ ] Dynamically create entities for all items
  - [ ] Handle Group items
- [ ] Add attributes (tags, groupNames, editable, link)
- [ ] Configuration - filter entities by Item types
