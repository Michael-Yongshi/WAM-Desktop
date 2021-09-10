import sys

from PyQt5.QtCore import (
    QSettings
    )

from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QSizePolicy,
    )

from PyQt5.QtGui import (
    QFontDatabase,
    QIcon,
    )

from wamcore.core.methods_engine import (
    save_warband,
    )

from wamcore.core.class_hierarchy import (
    Warband,
    Character,
    )

from darktheme.widget_template import (
    DarkApplication,
    QBorderlessFrame,
)

from gui.widget_warband import WidgetWarband
from gui.widget_system import WidgetSystem
from gui.widget_heroes import WidgetHeroes
from gui.widget_squads import WidgetSquads
from gui.widget_current import WidgetCurrent


class Application(DarkApplication):
    """A Dark styled application."""

    def __init__(self, *__args):
        super().__init__(*__args)

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

        # store nested widgets
        self.nested_widget = self.set_nested_widget()

        self.initUI()

    def initUI(self):

        # save window settings (size and position)
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        # autosave
        self.call_save_warband(autosave=True)   

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
        topbox.addWidget(WidgetSystem(self), 0, 4, 1, 1)

        topboxframe = QBorderlessFrame()
        topboxframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        topboxframe.setLayout(topbox)

        return topboxframe

    def set_botbox(self):

        # wrapping heroes, squads and extra details in the bottom horizontal layout
        botbox = QGridLayout()
        botbox.addWidget(WidgetHeroes(self), 0, 0)
        botbox.addWidget(WidgetSquads(self), 0, 1)
        botbox.addWidget(WidgetCurrent(self), 0, 2, 1, 2)

        botboxframe = QBorderlessFrame()
        botboxframe.clicked.connect(self.remove_focus)
        botboxframe.setLayout(botbox)

        return botboxframe

    def remove_focus(self):
        self.currentunit = None
        self.initUI

    def call_save_warband(self, autosave=False, backup=False):

        if self.wbid.name != "":

            # collect warband info
            name = self.wbid.name

            if autosave == True or backup == True:
                if backup == True:
                    filename = name+"backup"
                
                elif autosave == True:
                    filename = name+"-autosave"

                save_warband(warband=self.wbid, filename=filename, add_timestamp=True)

def run():
    global app
    app = Application(sys.argv)
    global main
    main = WarbandOverview()
    sys.exit(app.exec_())
