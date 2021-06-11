
from os import name
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

from wamcore.core.methods_engine import (
    save_warband,
    load_warband,
    show_warbands,
    save_reference,
    load_reference,
    )

from wamcore.core.class_hierarchy import (
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

from darktheme.widget_template import *



class WidgetAbility(QBorderlessFrame):
    def __init__(self, mainwindow, abilitylist, skip):
        super().__init__()

        self.mainwindow = mainwindow
        self.abilitylist = abilitylist
        self.skip = skip

        #show abilities
        abilitybox = QVBoxLayout() # create a vertical layout to show them in a neat line

        for ability in abilitylist:
            label = QClickLabel()
            label.setText(f"{ability.name}")
            label.setToolTip(f"<font><b>{ability.name}</b> <br/><br/> {ability.description}</font>")
            label.clicked.connect(self.create_method_remove(unit = self.mainwindow.currentunit, ability = ability))
            box = QVBoxLayout()
            box.addWidget(label)
            frame = QRaisedFrame()
            frame.setLayout(box)
            abilitybox.addWidget(frame) #adds the ability to a label and at it to the vertical ability layout
        
        # add new ability widget
        if skip == False:
            label = QClickLabel()
            label.setText("New Ability")
            label.setToolTip(f"Add manually a new ability for this unit.")
            label.clicked.connect(self.create_method_new_ability(unit=self.mainwindow.currentunit))
            abilitybox.addWidget(label) #adds the ability to a label and at it to the vertical item layout

        self.setLayout(abilitybox)

    def create_method_new_ability(self, unit):
        """Method for creating a new ability and receiving as attribute the unit it should be added to.
                    """
        def create_ability_for_unit():

            new_ability = WidgetAbility.dialog_new_ability(self.mainwindow)
         
            if new_ability:
                if unit.ishero == True:
                    for hero in self.mainwindow.wbid.herolist:
                        if unit is hero:
                            hero.abilitylist.append(new_ability)
                            self.mainwindow.initUI()
                            
                else:
                    for s in self.mainwindow.wbid.squadlist:
                        if unit is s.henchmanlist[0]:
                            for henchman in s.henchmanlist:
                                henchman.abilitylist.append(new_ability)
                            self.mainwindow.initUI()

        return create_ability_for_unit

    @staticmethod
    def dialog_new_ability(mainwindow):
        records = load_reference("abilities")
        
        # categories
        categories = []
        for record in records:
            pk = record.primarykey
            category = record.recorddict["maincategory"]
            subcategory = record.recorddict["category"]
            source = record.recorddict["source"]
            name = record.recorddict["name"]
            text = f"{pk}-{source}-{category}-{subcategory}-{name}"
            categories.append(text)

        ability, okPressed = QInputDialog.getItem(mainwindow, "Select Main category", "Choose a main category", categories, 0, False)
        if okPressed and ability:

            # take the primary key from the chosen awnser and get the python object
            pk = int(ability.split('-', 1)[0])
            new_ability = Ability.from_database(primarykey=pk)

            return new_ability

    def create_method_remove(self, unit, ability):          
        """ """

        def remove():

            remove = QMessageBox.question(self, 'Remove ability', f"Do you want to remove this ability?", QMessageBox.Yes | QMessageBox.No)
            if remove == QMessageBox.Yes:

                if unit.ishero == True:
                    for hero in self.mainwindow.wbid.herolist:
                        if hero is unit:
                            for a in hero.abilitylist:
                                if a is ability:
                                    index = hero.abilitylist.index(ability)
                                    hero.abilitylist.pop(index)
                                    break

                elif unit.ishero == False:
                    for squad in self.mainwindow.wbid.squadlist:
                        if unit is squad.henchmanlist[0]:
                            for henchman in squad.henchmanlist:
                                for a in henchman.abilitylist:
                                    if a is ability:
                                        index = henchman.abilitylist.index(ability)
                                        henchman.abilitylist.pop(index)
                                        break

                self.mainwindow.initUI()
        
        return remove

class WidgetMagic(QBorderlessFrame):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        #show magic
        magicbox = QVBoxLayout() # create a vertical layout to show them in a neat line

        for magic in self.mainwindow.currentunit.magiclist:
            label = QClickLabel()
            label.setText(str(magic.name))
            label.setToolTip(f"<font><b>{magic.name}</b> <br/>Difficulty: {magic.difficulty} <br/><br/> {magic.description}</font>")
            label.clicked.connect(self.create_method_remove(unit = self.mainwindow.currentunit, magic = magic))
            box = QVBoxLayout()
            box.addWidget(label)
            frame = QRaisedFrame()
            frame.setLayout(box)
            magicbox.addWidget(frame) #adds the magic to a label and at it to the vertical magic layout

        # add new magic widget
        label = QClickLabel()
        label.setText("New Magic")
        label.setToolTip(f"Add manually a new magic skill for this unit.")
        label.clicked.connect(self.create_method_new_magic(unit=self.mainwindow.currentunit))
        magicbox.addWidget(label) #adds the magic to a label and at it to the vertical item layout

        self.setLayout(magicbox)

    def create_method_new_magic(self, unit):
        """Method for creating a new magic and receiving as attribute the unit it should be added to.
                    """
        def create_magic_for_unit():
            
            new_magic = WidgetMagic.dialog_new_magic(self.mainwindow)

            if new_magic:
                if unit.ishero == True:
                    for hero in self.mainwindow.wbid.herolist:
                        if unit is hero:
                            hero.magiclist.append(new_magic)
                            self.mainwindow.initUI()
                            
                else:
                    for s in self.mainwindow.wbid.squadlist:
                        if unit is s.henchmanlist[0]:
                            for henchman in s.henchmanlist:
                                henchman.magiclist.append(new_magic)
                            self.mainwindow.initUI()

        return create_magic_for_unit

    @staticmethod
    def dialog_new_magic(mainwindow):
        records = load_reference("magics")

        # categories
        categories = []
        for record in records:
            pk = record.primarykey
            category = record.recorddict["category"]
            subcategory = record.recorddict["name"]
            source = record.recorddict["source"]
            text = f"{pk}-{source}-{category}-{subcategory}"
            categories.append(text)

        magic, okPressed = QInputDialog.getItem(mainwindow, "Select Magic", "Choose a Magic", categories, 0, False)
        if okPressed and magic:

            # take the primary key from the chosen awnser and get the python object
            pk = int(magic.split('-', 1)[0])
            new_magic = Magic.from_database(primarykey=pk)

            return new_magic


    def create_method_remove(self, unit, magic):          
        """ """

        def remove():
            
            remove = QMessageBox.question(self, 'Remove magic', f"Do you want to remove this magic?", QMessageBox.Yes | QMessageBox.No)
            if remove == QMessageBox.Yes:

                if unit.ishero == True:
                    for hero in self.mainwindow.wbid.herolist:
                        if hero is unit:
                            for m in hero.magiclist:
                                if m is magic:
                                    index = hero.magiclist.index(m)
                                    hero.magiclist.pop(index)
                                    break

                elif unit.ishero == False:
                    for squad in self.mainwindow.wbid.squadlist:
                        if unit is squad.henchmanlist[0]:
                            for henchman in squad.henchmanlist:
                                for m in henchman.magiclist:
                                    if m is magic:
                                        index = henchman.magiclist.index(magic)
                                        henchman.magiclist.pop(index)
                                        break

                self.mainwindow.initUI()
        
        return remove