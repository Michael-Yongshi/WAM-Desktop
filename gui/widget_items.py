

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QMessageBox,
    QVBoxLayout,
    )

from wamcore.core.methods_engine import (
    load_reference,
    )

from wamcore.core.class_hierarchy import (
    Item,
    )

from darktheme.widget_template import *

from gui.widget_abilitymagic import (
    WidgetAbility,
    )

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

            choose = ("Undo","Sell","Loss")
            choice, okPressed = QInputDialog.getItem(self, "Item action","What needs to happen to this item?", choose, 0, False)
            if okPressed and choice:

                for i in warband.itemlist:
                    if i is item:

                        # check if a complete refund is necessary
                        itemprice = 0
                        if choice == "Undo":
                            itemprice += item.price
                        # check if half a refund is necessary
                        elif choice == "Sell":
                            itemprice += (item.price / 2)
                        # add the amount to the warbands treasury
                        self.mainwindow.wbid.treasury.gold += itemprice

                        # removing the item
                        index = warband.itemlist.index(item)
                        warband.itemlist.pop(index)
                        break

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

            choose = ("Undo","Sell","Loss")
            choice, okPressed = QInputDialog.getItem(self, "Item action","What needs to happen to this item?", choose, 0, False)
            if okPressed and choice:

                if unit.ishero == True:

                    for i in unit.itemlist:
                        if i is item:

                            # check if a complete refund is necessary
                            itemprice = 0
                            if choice == "Undo":
                                itemprice += item.price
                            # check if half a refund is necessary
                            elif choice == "Sell":
                                itemprice += (item.price / 2)
                            # add the amount to the warbands treasury
                            self.mainwindow.wbid.treasury.gold += itemprice

                            # removing the item
                            index = unit.itemlist.index(item)
                            unit.itemlist.pop(index)
                            break

                elif unit.ishero == False:

                    for squad in self.mainwindow.wbid.squadlist:
                        if unit is squad.henchmanlist[0]:
                            # this squad is the current unit part of

                            for henchman in squad.henchmanlist:
                                # do for all squad henchmen

                                for i in henchman.itemlist:
                                    # find all items with the same name

                                    if i.subcategory == item.subcategory:

                                        # check if a complete refund is necessary
                                        itemprice = 0
                                        if choice == "Undo":
                                            itemprice += item.price
                                        # check if half a refund is necessary
                                        elif choice == "Sell":
                                            itemprice += (item.price / 2)
                                        # add the amount to the warbands treasury
                                        self.mainwindow.wbid.treasury.gold += itemprice

                                        # removing the item
                                        index = henchman.itemlist.index(item)
                                        henchman.itemlist.pop(index)
                                        break

                self.mainwindow.initUI()
        
        return remove


def dialog_choose_item(self):
    
    records = load_reference("items")
    
    # categories
    categories = []
    for record in records:
        pk = record.primarykey
        category = record.recorddict["category"]
        subcategory = record.recorddict["subcategory"]
        source = record.recorddict["source"]
        itemtext = f"{pk}-{source}-{category}-{subcategory}"
        categories.append(itemtext)

    item, okPressed = QInputDialog.getItem(self, "Select", "Choose an item", categories, 0, False)
    if okPressed and item:

        # take the primary key from the chosen awnser and get the python object
        pk = int(item.split('-', 1)[0])
        new_item = Item.from_database(primarykey=pk)
        
        return new_item
              
    else:
        string = "Cancel"
        return string