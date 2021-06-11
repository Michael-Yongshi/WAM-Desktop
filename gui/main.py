import sys

from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QMessageBox,
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

from darktheme.widget_template import *

from gui.widget_warband import WidgetWarband
from gui.widget_system import WidgetSystem
from gui.widget_heroes import WidgetHeroes
from gui.widget_squads import WidgetSquads
from gui.widget_current import WidgetCurrent


class QMainApplication(QApplication):
    """A Dark styled application."""
    def __init__(self, *__args):
        super().__init__(*__args)
        
        QFontDatabase.addApplicationFont("source/schoensperger.otf")
        self.setStyle("Fusion")
        self.setPalette(DarkPalette())
        # self.setFont(QFont("schoensperger", 20))
        self.setStyleSheet("QToolTip { color: #ffffff; background-color: grey; border: 1px solid white; }")
    

class WarbandOverview(QMainWindow):
    """The main window that everything runs in"""
    def __init__(self):
        super().__init__()
        self.wbid = Warband.create_template()
        self.currentunit = Character.create_template()
        self.currentthing = None
        self.autosave = False

        self.initUI()

    def initUI(self):

        if self.autosave == True:
            print(f"autosaved!")
            self.call_save_warband()

        # Some window settings
        self.setWindowTitle('Warhammer Army Manager')
        self.setWindowIcon(QIcon('war_72R_icon.ico'))     

        # build overview
        nested_widget = self.set_nested_widget()

        self.setCentralWidget(nested_widget)
        self.showMaximized()

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

    def call_save_warband(self):
        print(f"Saving warband {self.wbid.name}")
        datadict = self.wbid.to_dict()
        save_warband(datadict)
        QMessageBox.information(self, "Saved", "Save successful!", QMessageBox.Ok)

def run():
    global app
    app = QMainApplication(sys.argv)
    global main
    main = WarbandOverview()
    sys.exit(app.exec_())
