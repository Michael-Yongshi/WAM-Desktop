import sys

from PyQt5.QtCore import (
    QSettings
    )

from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QGridLayout,
    QInputDialog,
    QMessageBox,
    QMainWindow,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    )

from PyQt5.QtGui import (
    QFontDatabase,
    QIcon,
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

from darktheme.widget_template import (
    DarkPalette,
    QBorderlessFrame,
)

from gui.widget_warband import WidgetWarband
from gui.widget_system import WidgetSystem
from gui.widget_heroes import WidgetHeroes
from gui.widget_squads import WidgetSquads
from gui.widget_current import WidgetCurrent


class Application(QApplication):
    """A Dark styled application."""

    def __init__(self, *__args):
        super().__init__(*__args)

        self.setPalette(DarkPalette())
        QFontDatabase.addApplicationFont("source/schoensperger.otf")   

class WarbandOverview(QMainWindow):
    """The main window that everything runs in"""
    def __init__(self):
        super().__init__()

        # Some window settings
        self.setWindowTitle('Warhammer Army Manager')
        self.setWindowIcon(QIcon('war_72R_icon.ico'))  

        # create empty settings of the main window
        self.settings = QSettings("Michael-Yongshi", "WAM-Desktop")

        # store persistent variables
        self.wbid = Warband.create_template()
        self.currentunit = Character.create_template()
        self.currentthing = None

        # set menu bar
        bar = self.menuBar()

        file_menu = bar.addMenu('File')
        create_action = QAction('Create', self)
        create_action.setToolTip('Create a new <b>Warband</b>')
        create_action.triggered.connect(self.create_warband)
        open_action = QAction('Open', self)
        open_action.setToolTip('Choose an existing <b>Warband</b>')
        open_action.triggered.connect(self.choose_warband)
        save_action = QAction('Save', self)
        save_action.setShortcut("Ctrl+S")
        save_action.setToolTip('Save current <b>Warband</b>')
        save_action.triggered.connect(self.save_warband)
        close_action = QAction('Close', self)
        close_action.setToolTip('Close <b>Warband</b>')
        # close_action.triggered.connect(self.close_warband)
        quit_action = QAction('Quit', self)
        quit_action.setToolTip('Quit')
        quit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(create_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(close_action)
        file_menu.addAction(quit_action)

        edit_menu = bar.addMenu('Edit')
        undo_action = QAction('Undo', self)
        redo_action = QAction('Redo', self)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        lexi_menu = bar.addMenu('Lexicon')
        fight_action = QAction('Fights', self)
        lexi_menu.addAction(fight_action)

        # store nested widgets
        self.nested_widget = self.set_nested_widget()

        self.initUI()

    def initUI(self):

        # save window settings (size and position)
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        # autosave
        self.save_warband(autosave=True)   

        # update nested widget
        self.nested_widget = self.set_nested_widget()
        self.setCentralWidget(self.nested_widget)

        # Restore window settings (size and position)
        self.restoreGeometry(self.settings.value("geometry", bytes("", "utf-8")))
        self.restoreState(self.settings.value("windowState", bytes("", "utf-8")))
        self.show()

    def set_nested_widget(self):

        # vertical layout for top and char part
        overviewbox = QGridLayout()
        overviewbox.addWidget(self.set_topbox(), 0, 0, 1, 3)
        overviewbox.addWidget(self.set_botbox(), 1, 0, 3, 3)

        overviewboxframe = QBorderlessFrame()
        overviewboxframe.setLayout(overviewbox)

        return overviewboxframe

    def set_topbox(self):
        
        # top wrapping warband and system in the top horizontal layout
        topbox = QGridLayout()
        topbox.addWidget(WidgetWarband(self), 0, 0, 1, 4)
        # topbox.addWidget(WidgetSystem(self), 0, 4, 1, 1)

        topboxframe = QBorderlessFrame()
        topboxframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        topboxframe.setLayout(topbox)

        return topboxframe

    def set_botbox(self):

        # wrapping heroes, squads and extra details in the bottom horizontal layout
        botbox = QGridLayout()

        hero_scroll_widget = WidgetHeroes(self)
        hero_scroll = QScrollArea(self)
        hero_scroll.setWidget(hero_scroll_widget)
        hero_scroll.setWidgetResizable(True)
        # hero_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # hero_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        squad_scroll_widget = WidgetSquads(self)
        squad_scroll = QScrollArea(self)
        squad_scroll.setWidget(squad_scroll_widget)
        squad_scroll.setWidgetResizable(True)

        current_scroll_widget = WidgetCurrent(self)
        current_scroll = QScrollArea(self)
        current_scroll.setWidget(current_scroll_widget)
        current_scroll.setWidgetResizable(True)

        botbox.addWidget(hero_scroll, 0, 0)
        botbox.addWidget(squad_scroll, 0, 1)
        botbox.addWidget(current_scroll, 0, 2, 1, 2)

        botboxframe = QBorderlessFrame()
        botboxframe.clicked.connect(self.remove_focus)
        botboxframe.setLayout(botbox)

        return botboxframe

    def remove_focus(self):
        self.currentunit = None
        self.initUI

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
                self.wbid = warband_object

                # set an empty character as currentunit
                self.currentunit = Character.create_template()
                
                # restart ui to force changes
                self.initUI()

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
            self.wbid = wbobj

            # set empty current unit to main window
            self.currentunit = Character.create_template()

            # Restart the main window to force changes
            self.initUI() 

    def save_warband(self, autosave=False, backup=False, popup=False):

        if self.wbid.name != "":

            # collect warband info
            name = self.wbid.name

            if autosave == True or backup == True:
                add_timestamp = True
                if backup == True:
                    filename = name+"backup"
                
                elif autosave == True:
                    filename = name+"-autosave"

            else:
                filename = name
                add_timestamp = False

            try:
                save_warband(warband=self.wbid, filename=filename, add_timestamp=add_timestamp)
            except:
                QMessageBox.critical(self, "Error", "Save Failed!", QMessageBox.Ok)

def run():
    global app
    app = Application(sys.argv)
    global main
    main = WarbandOverview()
    sys.exit(app.exec_())
