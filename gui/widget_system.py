import sys

from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    )

from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
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

from wamcore.database.database_methods import (
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
            
        # get all races in references
        warband_records = get_database_records("warbands")
        if warband_records == None:
            QMessageBox(self, f"Error", f"Could not load database files")
            return
        
        dialog = CreateDialog(self.mainwindow, warband_records)
        if dialog.exec():

            for record in warband_records:
                if record.primarykey == dialog.getSelectedID():
                    warbanddict = record.recorddict
                    print(f"recorddict {warbanddict}")
                    name = dialog.name
                    warband = warbanddict["name"]
                    race = warbanddict["race"]
                    source = warbanddict["source"]
                    break

            # Create new warband object
            wbobj = Warband.create_warband(name=name, race=race, source=source, warband=warband)
            
            # Load warband object to main window
            self.mainwindow.wbid = wbobj

            # set an empty character as currentunit
            self.mainwindow.currentunit = Character.create_template()
            
            # restart ui to force changes
            self.mainwindow.initUI()


class CreateDialog(QDialog):
    def __init__(self, mainwindow, warband_records):
        super().__init__()

        self.mainwindow = mainwindow
        self.setWindowTitle("Create a new warband")

        self.name = QLineEdit(self)
        self.name.setText("warband")
        self.name.setToolTip("Insert a name")

        self.warband = QComboBox()
        for record in warband_records:
            warbandtext = f""
            for valuepair in record.recordpairs:
                print(valuepair)
                if valuepair[0] == "id":
                    warbandid = valuepair[1]
                elif (valuepair[0] == "race") or (valuepair[0] == "source") or (valuepair[0] == "name"):
                    warbandtext += f"{valuepair[1]} - "
            self.warband.addItem(warbandtext, warbandid)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Name", self.name)
        layout.addRow("Warband", self.warband)

        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getSelectedID(self):
        index = self.warband.currentIndex()
        warbandId = self.warband.itemData(index)

        return warbandId