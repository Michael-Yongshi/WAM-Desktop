
from PyQt5.QtWidgets import (
    QGridLayout,
    QInputDialog,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QWidget, 
    )

from wamcore.core.class_hierarchy import (
    Hero,
    )

from darktheme.widget_template import *
# from gui.widget_currentbox import *


class WidgetHeroes(QWidget):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        # def set_herobox(self, currentbox):
        # as we give this class a reference to currentbox, we can manipulate currentbox from here
        # currentbox.set_current_hero(hero)

        herobox = QVBoxLayout() # To show all heroes below each other dynamically (based on actual number of heroes)
        
        h = 0
        for hero in self.mainwindow.wbid.herolist: # First iterate over the heroes in your warband
            h += 1
            
            herogrid = QGridLayout() # create a grid layout to position all information more accurately
            
            namelabel = QLabel()
            if hero is self.mainwindow.currentunit:
                namelabel.setText(f"<b>{hero.name}<br/>(selected)<b/>")
            else:
                namelabel.setText(f"<b>{hero.name}<b/>")
            namelabel.setToolTip(f"This is your hero`s name")
            herogrid.addWidget(namelabel, 0, 0) # add the name and category box to the herogrid
            
            catlabel = QLabel()
            catlabel.setText(f"<b>{hero.category}<b/>")
            catlabel.setToolTip(f"This is your hero`s unit type. The unit type determines what the heroes abilities are, what kind of items it can carry and how expensive it is to replace.")
            herogrid.addWidget(catlabel, 0, 1) # add the cat and category box to the herogrid

            # bound a click on the hero to show details in character view
            heroframe = QRaisedFrame()
            heroframe.setLayout(herogrid)
            heroframe.clicked.connect(self.create_method_focus(hero))
            
            herobox.addWidget(heroframe)

        if h <= 5: # If there is still room in your warband add a new hero widget
            h += 1
            herogrid = QGridLayout()
            namelabel = QLabel()
            namelabel.setText("Add New Hero")
            herogrid.addWidget(namelabel, 0, 0)

            heroframe = QRaisedFrame()
            heroframe.setLayout(herogrid)
            heroframe.clicked.connect(self.create_new)
            herobox.addWidget(heroframe)
        
        while h <= 5: # if there is still room, add some empty widgets to fill up the space
            h += 1
            heroframe = QBorderlessFrame()
            herobox.addWidget(heroframe)

        self.setToolTip('These are your <b>heroes</b>')
        self.setLayout(herobox)
        
    def create_method_focus(self, hero):          
        """This method is used in order to create a new method that holds a reference to a passed attribute,
        this is used when a widget needs to be clickable but the signal needs to carry information other than the signal itself.
        This one specifically gets a current unit and then passes it to the currentunit attribute of the main window"""
        
        def focus_unit():
            
            self.mainwindow.currentunit = hero
            self.mainwindow.initUI()

        return focus_unit

    def create_method_remove(self, hero): 
        """This method is used in order to create a new method that holds a reference to a passed attribute,
        this is used when a widget needs to be clickable but the signal needs to carry information other than the signal itself.
        This one specifically gets a current hero and then creates a window based on the attribute"""

        def remove():

            remove = QMessageBox.question(self, 'Remove hero', f"Do you want to remove this hero?", QMessageBox.Yes | QMessageBox.No)
            if remove == QMessageBox.Yes:
                process_gold = QMessageBox.question(self, "Process gold", "Do you want to process an exchange for gold?", QMessageBox.Yes | QMessageBox.No)
                heroprice = 0

                for hero in self.mainwindow.wbid.herolist:
                    if hero is self.mainwindow.scurrentunit:
                        if process_gold == QMessageBox.Yes:
                            heroprice += hero.price
                            for item in hero.itemlist:
                                heroprice += item.price
                        index = self.mainwindow.wbid.herolist.index(hero)
                        self.mainwindow.wbid.herolist.pop(index)
                        break

                self.mainwindow.wbid.treasury.gold += heroprice
                self.mainwindow.initUI()
        
        return remove

    def create_new(self):
        
        """Create a new hero, store it in the warband object and set to currentunit"""
        name, okPressed = QInputDialog.getText(self, "Create", "Name your hero:")
        if okPressed and name:
            
            # get applicable characters to choose from
            character_list = self.mainwindow.wbid.get_characters()
            categories = []
            
            for character in character_list:
                if character.ishero == True:
                    pk = character.database_id
                    category = character.category
                    charactertext = f"{pk}-{category}"
                    categories.append(charactertext)

            category, okPressed = QInputDialog.getItem(self, "Create", "Choose a character", categories, 0, False)
            if okPressed and category:
                # take the primary key from the chosen awnser and get the character object
                pk = int(category.split('-', 1)[0])
                new_hero = Hero.from_database(primarykey=pk)
                new_hero.name = name

                # add hero to warband and deduct from gold
                wbidgold = self.mainwindow.wbid.treasury.gold
                if wbidgold >= new_hero.price:
                    self.mainwindow.wbid.treasury.gold = wbidgold - new_hero.price
                    self.mainwindow.wbid.herolist.append(new_hero)
                    self.mainwindow.currentunit = new_hero
                    self.mainwindow.initUI()
                else:
                    message = QMessageBox.information(self, 'Lack of funds!', "Can't add new hero, lack of funds", QMessageBox.Ok)

