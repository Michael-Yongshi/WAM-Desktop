# WAM-Desktop
The desktop frontend for the WAM application, used for Linux, Windows and MacOS.

Uses WAM-Core as a submodule
https://github.com/Michael-Yongshi/WAM-Core.git

## Roadmap

## Getting Started

To install a working desktop application grab the zip folder from:

<b>Windows 10 64 bit</b>: https://www.jottacloud.com/s/13030f55cae66fb428698777e670d3a052a. 

<b>Ubuntu 18 64 bit</b>: https://www.jottacloud.com/s/130ab5742a54b87443a896a37062196affa.

Unzip the folder and run the exe / app file within.

## Development

see for some basic installation stuff in wam_core:
https://github.com/Michael-Yongshi/WAM-Core/README.md#git

### GUI requisites

```
pip3 install --user pyqt5
apt-get install python3 pyqt5           # (prod) if pip3 doesn't work
sudo apt-get install python3-pyqt5      # ubuntu
```

## Running the tests


### Break down into end to end tests



### And coding style tests



## Deployment

### PyInstaller (deploy cross platform desktop gui)
```
pip3 install --user pyinstaller         # (dev) to create an installer for desktop OS like windows, ubuntu, ios
```

sometimes you need to run this for path to find pip package:
```
export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.6/site-packages:/usr/lib/python3.6/site-packages"
```

### create a distribution manually: 
```
python -m PyInstaller cli.py --add-data "lib/wam_core/database/references/*.json";"lib/wam_core/database/references/" --icon="gui\war_72R_icon.ico" --name WAM-Win10-64

pyinstaller cli.py --add-data "lib/wam_core/database/references/*.json":"lib/wam_core/database/references/" --icon="gui\war_72R_icon.ico" --name WAM-Ubuntu18-64
```


### create a distribution from spec with 
```
python -m PyInstaller WAM.spec
```
<!-- python -m PyInstaller WAM_OF.spec -->

## Built With



## Contributing



## Versioning



## Authors

* **Michael-Yongshi** 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License



## Acknowledgments