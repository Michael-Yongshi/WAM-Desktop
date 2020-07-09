# Warhammer Army Manager (WAM) Desktop
An application in order to create, update, view and save your warband details for use in the Mordheim Warhammer world. Using this application there is no need anymore for manually calculating skills or looking up your warbands details, including references to all item, spells, abilities, etc. that are ingame and the rules governing engagements.

The desktop frontend for the WAM application, used for Linux, Windows and MacOS.

Uses WAM-Core as a submodule
https://github.com/Michael-Yongshi/WAM-Core.git

Uses Py-library-nfc as a submodule
https://github.com/Michael-Yongshi/Py-Library-NFC

#### Notice
For Missile and Blackpowder weapons an additional strength modifier is created named 'Impact', in order to seperate the strength skill of melee and ranged attacks.

## Release Notes
### Release 1.10
Win10-64: https://www.jottacloud.com/s/130542021d8feef4f458ee5a2d6bf74862a

Ubuntu18-64: https://www.jottacloud.com/s/1305442054280194dfaa20c392243302191

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

### PyQt5
GUI package

```
pip3 install --user pyqt5
sudo apt-get install python3 pyqt5           # (prod) if pip3 doesn't work
```

### yongshi-guidarktheme
Dark Theme settings package
```
pip3 install --user yongshi-guidarktheme
```

### Pyscard
NFC reader package
```
pip3 install --user pyscard
```

### NDEF
NFC interpretation package
```
pip3 install --user ndef
```

## Running the tests


### Break down into end to end tests


### And coding style tests


## Deployment


## Built With PyInstaller 
(deploy cross platform desktop gui)

### install
```
pip3 install --user pyinstaller         # (dev) to create an installer for desktop OS like windows, ubuntu, ios
```

### Create distribution
Windows 10 (64bit)
```
python -m PyInstaller cli.py --add-data "lib/wam_core/database/references/*.json";"lib/wam_core/database/references/" --icon="gui\warhammer_icon.ico" --name WAM-Win10-64
```

Ubuntu 18 (64bit)
```
pyinstaller cli.py --add-data "lib/wam_core/database/references/*.json":"lib/wam_core/database/references/" --icon="gui\warhammer_icon.ico" --name WAM-Ubuntu18-64
```

### create a distribution from spec file with 
```
python -m PyInstaller WAM.spec
```
<!-- python -m PyInstaller WAM_OF.spec -->


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
