import sys

from PyQt5.QtWidgets import (
    QGridLayout,
    QInputDialog,
    QMessageBox,
    QPushButton, 
    )

from wamcore.core.methods_engine import (
    save_warband,
    load_warband,
    show_warbands,
    load_reference,
    )

from wamcore.core.class_hierarchy import (
    Warband,
    Character,
    )

from darktheme.widget_template import *


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

        save_warband(warband=self.mainwindow.wbid)
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
            
            # get all warbands from the database
            wbtable = load_reference("warbands")
            if wbtable == None:
                QMessageBox(self, f"Error", f"Could not load database files")
                return

            # create a list of choices
            warbands = []
            for record in wbtable:
                pk = record.primarykey
                race = record.recorddict["race"]
                source = record.recorddict["source"]
                base = record.recorddict["base"]
                warbandtext = f"{pk}-{race}-{source}-{base}"

                warbands += [warbandtext]
            
            # let user choose from the list
            warband, okPressed = QInputDialog.getItem(self, "Create", "Choose a warband", warbands, 0, False)
            if okPressed and warband:
                
                # take the primary key from the chosen awnser and get the python object
                pk = int(warband.split('-', 1)[0])
                warband_object = Warband.from_database(primarykey=pk)
                warband_object.name = name

                # Load warband object to main window
                self.mainwindow.wbid = warband_object

                # set an empty character as currentunit
                self.mainwindow.currentunit = Character.create_template()
                
                # restart ui to force changes
                self.mainwindow.initUI()