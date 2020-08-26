import sys

from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    )

from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton, 
    QSizePolicy,
    QVBoxLayout,
    QWidget, 
    )

from PyQt5.QtGui import (
    QFont,
    QFontDatabase,
    QIcon,
    )

from wamcore.database import (
    get_database_records,
)

from wamcore.methods_engine import (
    save_warband,
    load_warband,
    show_warbands,
    save_reference,
    load_reference,
    )

from wamcore.class_hierarchy import (
    Warband,
    Squad,
    Character,
    Hero,
    Henchman,
    Rule,
    Treasury,
    Item,
    Skill,
    Ability,
    Magic,
    )

from guidarktheme.widget_template import *


class WidgetSystem(QBorderedWidget):
    def __init__(self, mainwindow):
        super().__init__()
        
        self.mainwindow = mainwindow
        
        sysbox = QGridLayout()
        
        # buttons for interaction
        btnchoose = QPushButton('Choose Warband', self)
        btnchoose.setToolTip('Choose an existing <b>Warband</b>')
        btnchoose.clicked.connect(self.choose_warband)

        btncreate = QPushButton('Create Warband', self)
        btncreate.setToolTip('Create a new <b>Warband</b>')
        btncreate.clicked.connect(self.create_warband)

        btnsave = QPushButton('Save Warband', self)
        btnsave.setShortcut("Ctrl+S")
        btnsave.setToolTip('Save current <b>Warband</b>')
        btnsave.clicked.connect(self.call_save_warband)

        # btnquit = QPushButton('Quit', self)
        # btnquit.setToolTip('Quit the program')
        # btnquit.clicked.connect(QApplication.instance().quit)

        sysbox.addWidget(btncreate, 0, 0)
        sysbox.addWidget(btnsave, 0, 1)
        sysbox.addWidget(btnchoose, 1, 0)
        # sysbox.addWidget(btnquit, 1, 1)

        self.setToolTip("Create a new warband, load a warband from memory or save current warband.")
        self.setLayout(sysbox)

    def call_save_warband(self):
        datadict = self.mainwindow.wbid.to_dict()
        save_warband(datadict)
        QMessageBox.information(self, "Saved", "Save successful!", QMessageBox.Ok)

    def choose_warband(self):
        """Choose a warband to be loaded into cache and then shown on screen"""
        
        # get list of save files
        warbands = show_warbands()

        # Let user choose out of save files
        wbname, okPressed = QInputDialog.getItem(self, "Choose", "Choose your warband", warbands, 0, False)
        if okPressed and wbname:
            # Load warband dictionary 
            wbdict = load_warband(wbname)
            # convert warband dict to object
            wbobj = Warband.from_dict(wbdict)
            # set chosen warband as object in main window
            self.mainwindow.wbid = wbobj

            # set empty current unit to main window
            self.mainwindow.currentunit = Character.create_template()

            # Restart the main window to force changes
            self.mainwindow.initUI() 
            
    def create_warband(self):
        """Create a new warband and store it in cache"""
        name, okPressed = QInputDialog.getText(self, "Create", "Name your warband:")
        if okPressed and name:
            
            # get all races in references
            warband_records = get_database_records("warbands")
            if warband_records == None:
                QMessageBox(self, f"Error", f"Could not load database files")
                return

            warbands = []
            for record in warband_records:
                warband = f"{record.primarykey}-"
                for valuepair in record.valuepairs[:3]:
                    warband += f"{valuepair[1]}-"
            
            warband, okPressed = QInputDialog.getItem(self, "Create", "Choose a warband", warbands, 0, False)
            if okPressed and warband:

                for record in warband_records:
                    if record.primarykey == warband.split('-', 1)[0]:
                        warbanddict = record.recorddict
                        print(f"recorddict {warbanddict}")

                # Create new warband object
                wbobj = Warband.create_warband(name=name, race=warbanddict["race"], source=warbanddict["source"], warband=warband["name"])
                
                # Load warband object to main window
                self.mainwindow.wbid = wbobj

                # set an empty character as currentunit
                self.mainwindow.currentunit = Character.create_template()
                
                # restart ui to force changes
                self.mainwindow.initUI()