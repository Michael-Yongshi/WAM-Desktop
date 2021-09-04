# Warhammer Army Manager (WAM) Desktop
An application in order to create, update, view and save your warband details for use in the Mordheim Warhammer world. Using this application there is no need anymore for manually calculating skills or looking up your warbands details, including references to all item, spells, abilities, etc. that are ingame and the rules governing engagements.

The desktop frontend for the WAM application, used for Linux and Windows

#### Notice
For Missile and Blackpowder weapons an additional strength modifier is created named 'Impact', in order to seperate the strength skill of melee and ranged attacks.

## Release Notes
### Release 1.3: SQLite
- Database is now based on SQLite3
- Cleaned up code
- Switched back to submodule for WAM-Core; wamcore will be removed from Pip in the near future.

### Release 1.10
Hotfix 2020-07-20
- Fixed nfc for ubuntu
- Fixed database crashes and other optimizations

Individual Henchman release 1.10 (beta) - 2020-07-07
- Changed squad view to tabs with individual henchman that you can rename and select
- Added buttons for removing a character (release means you get money back, perish and you don't)

- Added NFC functionality
  - tested using NFC Mifare tags NTAG213, NTAG215, NTAG216
  - tested using NFC Reader/Writer ACR122U
- Added button for linking character to a NFC tag using a unique id
- Added button for reading NFC and find character (will be changed to automatic later)

### Release 1.00
Win10-64: https://www.jottacloud.com/s/130dc76091c06c94f73a7b79378122252f5

Ubuntu18-64: https://www.jottacloud.com/s/13099be5dc95aae4139a0ca0328c19b71cf

Hotfix for release 1.00 - 2020-06-14
- Error handling for item creation to prevent crashes and added error message

Hotfix for release 1.00 - 2020-06-13
- fixed some item crashes and descriptions
- changed blackpowder weapons from strength to impact

## Roadmap
- Add more warbands from broheim.net/warbands
- test if mutations work correctly
- adjust code for individual henchmen (registering optional henchmen names and events)
- add linking physical unit with app through nfc (sticker)

## Development

### install code dependencies
```
pip3 install --upgrade -r requirements.txt 
```

#### PyQt5
GUI package

```
pip3 install pyqt5
sudo apt-get install python3 pyqt5           # (prod) if pip3 doesn't work
```

#### PyQt5 Dark Theme
Dark Theme settings package (>= v1.0)
```
pip3 install darktheme
```

#### NFC
NFC reader package

##### windows
```
pip3 install pyscard
pip3 install yongshi-pynfc
```

##### ubuntu
```
sudo apt install swig # may be needed to install pyscard
sudo apt install pcscd # may be needed to scan for readers on ubuntu
sudo apt install libpcsclite-dev # may be needed for the winscard.h file that is in this dependency
pip3 install pyscard
```

```
# if you get errors (ARC nfc reader has this with ubuntu)
sudo vim /etc/modprobe.d/blacklist-libnfc.conf
# Add this line: blacklist pn533_usb
# Reboot
```

```
pip3 install yongshi-pynfc
```

#### WAM core
pip package of WAM core replaced with submodule under 'wamcore'

### Install build dependencies

## Running the tests


### Break down into end to end tests


### And coding style tests


## Deployment


## Built With PyInstaller 
(deploy cross platform desktop gui)

### install
```
pip3 install pyinstaller         # (dev) to create an installer for desktop OS like windows, ubuntu, ios
```

### Create distribution
#### Windows 10 (64bit)
directory
```
python3 -m PyInstaller -F cli.py --name WAM-Win10-64-major-minor-patch-ext --add-data "./wamcore/core/database/database.sqlite;./wamcore/core/database" --icon="gui\warhammer_icon.ico" 
```

#### Ubuntu 21 (64bit)
appimage
```
python3 -m PyInstaller -F cli.py --name WAM-Ubuntu21-64-major-minor-patch-ext --add-data "./wamcore/core/database/database.sqlite:./wamcore/core/database"
```

remove the '-F' if you want a directory instead of a single file executable.

### create a distribution from spec file with 
<!-- ```
python -m PyInstaller WAM.spec
``` -->


## Contributing



## Versioning



## Authors

**Michael-Yongshi** 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

Licensed under GPL-3.0-or-later, see LICENSE file for details.

Copyright © 2020 WAM-Desktop contributors.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.


## Acknowledgments

### Icon

Icon by Lorc under CC BY 3.0
http://lorcblog.blogspot.com/
