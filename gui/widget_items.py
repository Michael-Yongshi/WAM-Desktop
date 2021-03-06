
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
from gui.widget_abilitymagic import WidgetAbility

class WidgetItemsWarband(QBorderlessFrame):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        itemlistbox = QVBoxLayout() # create a vertical layout to show them in a neat line
        for item in self.mainwindow.wbid.itemlist:
            label = QClickLabel()
            label.setText(f"<b>{item.subcategory}<b/>")
            label.setToolTip(f"<font><b>{item.subcategory} </b>{item.name} <br/> category: {item.category} <br/> distance: {item.distance} <br/> <nobr>{item.skill.to_string()}</nobr> <br/> price: {item.price} <br/> {item.description}</font>")
            label.clicked.connect(self.create_method_remove(warband = self.mainwindow.wbid, item = item))
            box = QVBoxLayout()
            box.addWidget(label)
            frame = QRaisedFrame()
            frame.setLayout(box)
            itemlistbox.addWidget(frame) #adds the item to a label and at it to the vertical item layout
            
        self.setLayout(itemlistbox)
            
        label = QClickLabel()
        label.setText(f"<font>New Item<font/>")
        label.clicked.connect(self.new)
        itemlistbox.addWidget(label) #adds the new item to a label and at it to the vertical item layout

        self.setToolTip("These are your warbands items.")
        self.setLayout(itemlistbox)
        
    def new(self):

        """Create a new item and store it in this warband"""
        new_item = dialog_choose_item(self)
        if new_item != "Cancel":
            wbidgold = self.mainwindow.wbid.treasury.gold
            itemprice = new_item.price
            if wbidgold >= itemprice:
                self.mainwindow.wbid.treasury.gold = wbidgold - itemprice
                self.mainwindow.wbid.itemlist.append(new_item)
                self.mainwindow.initUI()
            else:
                message = QMessageBox.information(self, 'Lack of funds!', "Can't add new item, lack of funds", QMessageBox.Ok)

    def create_method_remove(self, warband, item):          

        def remove():

            remove = QMessageBox.question(self, 'Remove item', f"Do you want to remove this item?", QMessageBox.Yes | QMessageBox.No)
            if remove == QMessageBox.Yes:
                process_gold = QMessageBox.question(self, "Process gold", "Do you want to process an exchange for gold?", QMessageBox.Yes | QMessageBox.No)
                itemprice = 0

                for i in warband.itemlist:
                    if i is item:
                        if process_gold == QMessageBox.Yes:
                            itemprice += item.price
                        index = warband.itemlist.index(item)
                        warband.itemlist.pop(index)
                        break

                self.mainwindow.wbid.treasury.gold += itemprice
                self.mainwindow.initUI()
        
        return remove



class WidgetItemsUnit(QBorderlessFrame):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow
        unit = self.mainwindow.currentunit

        itemlistbox = QVBoxLayout() # create a vertical layout to show them in a neat line

        for item in unit.itemlist:
            itembox = QHBoxLayout()

            label = QClickLabel()
            label.setText(f"<b>{item.subcategory}<b/>") # label.setText(f"<b>{item.subcategory} - {item.name}<b/>")
            label.setToolTip(f"<font><b>{item.subcategory} </b>{item.name} <br/> category: {item.category} <br/> distance: {item.distance} <br/> <nobr>{item.skill.to_string()}</nobr> <br/> price: {item.price} <br/> {item.description}</font>")
            label.clicked.connect(self.create_method_remove(unit = unit, item = item))
            itembox.addWidget(label)
            itembox.addWidget(WidgetAbility(self.mainwindow, abilitylist = item.abilitylist, skip = True)) # adds the ability layout to the grid

            frame = QRaisedFrame()
            frame.setLayout(itembox)
            itemlistbox.addWidget(frame) #adds the item to a label and at it to the vertical item layout

        # add new item widget
        label = QClickLabel()
        label.setText(f"<font>New Item<font/>")
        label.setToolTip(f"Buy a new item for this unit.")
        label.clicked.connect(self.create_method_new(unit=unit))
        itemlistbox.addWidget(label) #adds the item to a label and at it to the vertical item layout

        self.setLayout(itemlistbox)
        self.setToolTip("These are your units items.")

    def create_method_new(self, unit):
        """Method for creating a new item and receiving as attribute the unit it should be added to."""
        
        def new():
            new_item = dialog_choose_item(self)
            if new_item != "Cancel":
                if unit.ishero == True:
                    message = unit.buy_item(self.mainwindow.wbid, new_item)

                elif unit.ishero == False:
                    for squad in self.mainwindow.wbid.squadlist:
                        for henchman in squad.henchmanlist:
                            if unit is henchman:
                                message = squad.buy_item(self.mainwindow.wbid, new_item)
                                break
                
                if message == "Lack of funds!":
                    message = QMessageBox.information(self, 'Lack of funds!', "Can't add new item, lack of funds", QMessageBox.Ok)
                
                self.mainwindow.initUI()
            
        return new

    def create_method_remove(self, unit, item):          
        """ """

        def remove():

            remove = QMessageBox.question(self, 'Remove item', f"Do you want to remove this item?", QMessageBox.Yes | QMessageBox.No)
            if remove == QMessageBox.Yes:

                if unit.ishero == True:
                    unit.sell_item(self.mainwindow.wbid, item.subcategory)

                elif unit.ishero == False:
                    for squad in self.mainwindow.wbid.squadlist:
                        if unit is squad.henchmanlist[0]:
                            squad.sell_item(self.mainwindow.wbid, item.subcategory)
                            break

                self.mainwindow.initUI()
        
        return remove


def dialog_choose_item(self):
    
    datadict = load_reference("items")
    
    # categories
    categories = []
    for key in datadict:
        categories.append(key)

    category, okPressed = QInputDialog.getItem(self, "Create", "Choose a category", categories, 0, False)
    if okPressed and category:

        # sources
        sources = []
        for key in datadict[category]:
            sources.append(key)

        source, okPressed = QInputDialog.getItem(self, "Select source", "Choose a source", sources, 0, False)
        if okPressed and source:
        
            # subcategories
            subcategories = []
            for key in datadict[category][source]:
                subcategories.append(key)

            subcategory, okPressed = QInputDialog.getItem(self, "Create", "Choose an item", subcategories, 0, False)
            if okPressed and subcategory:
                new_item = Item.create_item(
                    subcategory = subcategory,
                    category = category,
                    source = source,
                )
                
                if new_item == None:
                    new_item = "Cancel"
                    message = QMessageBox.information(self, f"Coulnd't add item!", f"Can't add item {subcategory} from database, please create an issue at https://github.com/Michael-Yongshi/WAM-Desktop/issues", QMessageBox.Ok)
                
                return new_item
                
            else:
                string = "Cancel"
                return string
        else:
            string = "Cancel"
            return string
    else:
        string = "Cancel"
        return string