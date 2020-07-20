import os
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
    QTabWidget,
    QVBoxLayout,
    QWidget, 
    )

from PyQt5.QtGui import (
    QFont,
    QFontDatabase,
    QIcon,
    )

from pynfc.class_nfc import NFCconnection

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
    Event,
    )

from guidarktheme.widget_template import *
from gui.widget_items import WidgetItemsUnit
from gui.widget_abilitymagic import WidgetAbility, WidgetMagic

# from gui.widget_currentbox import *


class WidgetCurrent(QRaisedFrame):
    def __init__(self, mainwindow, configfile = {}):
        super().__init__()

        self.mainwindow = mainwindow

        if self.mainwindow.currentunit.ishero == True:
            currentbox = self.set_hero_box()

        elif self.mainwindow.currentunit.ishero == False:
            currentbox = self.set_henchman_box()

        else:
            currentbox = QVBoxLayout()

        self.setToolTip("This is the currently selected unit")
        self.setLayout(currentbox)

    def set_hero_box(self):
        currentbox = QVBoxLayout()

        self.configfile = {
            'namebox': {'row': 0, 'column': 0, 'width': 1, 'height': 1, 'children': {
                'namelabel': {'row': 0, 'column': 0, 'width': 1, 'height': 1, 'text': f"Name: <b>{self.mainwindow.currentunit.name}</b>", 'tooltip': "Name", 'connect': self.create_method_change_name(self.mainwindow.currentunit),},
                'catlabel': {'row': 1, 'column': 0, 'width': 1, 'height': 1, 'text': f"Category: <b>{self.mainwindow.currentunit.category}</b>", 'tooltip': "Category", 'connect': "",},
                'pricelabel': {'row': 2, 'column': 0, 'width': 1, 'height': 1, 'text': f"Price: <b>{self.mainwindow.currentunit.price}</b>", 'tooltip': "Price", 'connect': "",},
                'advlabel': {'row': 0, 'column': 1, 'width': 1, 'height': 1, 'text': f"Advance: <b>{self.mainwindow.currentunit.get_current_advance()}</b>", 'tooltip': f"Next is Advance <b>{self.mainwindow.currentunit.get_next_advance()}</b> at experience <b> {self.mainwindow.currentunit.get_xpneeded()} </b>", 'connect': "",},
                'explabel': {'row': 1, 'column': 1, 'width': 1, 'height': 1, 'text': f"Experience: <b>{self.mainwindow.currentunit.experience}</b>", 'tooltip': f"This characters current experience", 'connect': self.create_method_change_experience(),},
                'maxlabel': {'row': 2, 'column': 1, 'width': 1, 'height': 1, 'text': f"Maximum: <b>{self.mainwindow.currentunit.maxcount}</b>", 'tooltip': "Maximum", 'connect': "",},
                'levellabel': {'row': 0, 'column': 2, 'width': 1, 'height': 1, 'text': f"<b>{self.mainwindow.currentunit.get_levelup_notification()}</b>", 'tooltip': "", 'connect': self.create_method_levelup(),},                
                'eventslabel': {'row': 1, 'column': 2, 'width': 1, 'height': 1, 'text': f"Events", 'tooltip': f"This characters history: <br/>{self.mainwindow.currentunit.get_historystring()}", 'connect': "",},
                # 'removelabel': {'row': 2, 'column': 2, 'width': 1, 'height': 1, 'text': f"<b>Remove</b>", 'tooltip': f"Remove this character", 'connect': self.remove_unit(),},
                }
            },
            'skillbox': {'row': 1, 'column': 0, 'width': 1, 'height': 1,
            },
            'listbox': {'row': 2, 'column': 0, 'width': 4, 'height': 1,
            },
        }

        unitbox = QGridLayout()

        config = self.configfile['namebox']
        unitbox.addWidget(self.set_namebox(), config['row'], config['column'], config['width'], config['height'])

        config = self.configfile['skillbox']
        unitbox.addWidget(self.set_skillbox(), config['row'], config['column'], config['width'], config['height'])

        config = self.configfile['listbox']
        unitbox.addWidget(self.set_listbox(), config['row'], config['column'], config['width'], config['height'])

        unitwidget = QWidget()
        unitwidget.setLayout(unitbox)

        buttonwidget = self.set_buttonwidget()
        
        currentbox.addWidget(unitwidget)
        currentbox.addWidget(buttonwidget)

        return currentbox

    def set_henchman_box(self):

        currentbox = QVBoxLayout()
        currentsquad = None

        for squad in self.mainwindow.wbid.squadlist:
            for henchman in squad.henchmanlist:
                if self.mainwindow.currentunit is henchman:
                    currentsquad = squad
                    break
                    break

        if currentsquad != None:
            tabs = QTabWidget()

            for henchman in currentsquad.henchmanlist:

                self.configfile = {
                    'namebox': {'row': 0, 'column': 0, 'width': 1, 'height': 1, 'children': {
                        'namelabel': {'row': 0, 'column': 0, 'width': 1, 'height': 1, 'text': f"Name: <b>{henchman.name}</b>", 'tooltip': "Name", 'connect': self.create_method_change_name(henchman),},
                        'catlabel': {'row': 1, 'column': 0, 'width': 1, 'height': 1, 'text': f"Category: <b>{henchman.category}</b>", 'tooltip': "Category", 'connect': "",},
                        'pricelabel': {'row': 2, 'column': 0, 'width': 1, 'height': 1, 'text': f"Price: <b>{henchman.price}</b>", 'tooltip': "Price", 'connect': "",},
                        'advlabel': {'row': 0, 'column': 1, 'width': 1, 'height': 1, 'text': f"Advance: <b>{henchman.get_current_advance()}</b>", 'tooltip': f"Next is Advance <b>{henchman.get_next_advance()}</b> at experience <b> {henchman.get_xpneeded()} </b>", 'connect': "",},
                        'explabel': {'row': 1, 'column': 1, 'width': 1, 'height': 1, 'text': f"Experience: <b>{henchman.experience}</b>", 'tooltip': f"This characters current experience", 'connect': self.create_method_change_experience(),},
                        'maxlabel': {'row': 2, 'column': 1, 'width': 1, 'height': 1, 'text': f"Maximum: <b>{henchman.maxcount}</b>", 'tooltip': "Maximum", 'connect': "",},
                        'levellabel': {'row': 0, 'column': 2, 'width': 1, 'height': 1, 'text': f"<b>{henchman.get_levelup_notification()}</b>", 'tooltip': "", 'connect': self.create_method_levelup(),},                
                        'eventslabel': {'row': 1, 'column': 2, 'width': 1, 'height': 1, 'text': f"Events", 'tooltip': f"This characters history: <br/>{henchman.get_historystring()}", 'connect': "",},
                        # 'removelabel': {'row': 2, 'column': 2, 'width': 1, 'height': 1, 'text': f"<b>Remove</b>", 'tooltip': f"Remove this character", 'connect': self.remove_unit(),},
                        }
                    },
                    'skillbox': {'row': 1, 'column': 0, 'width': 1, 'height': 1,
                    },
                    'listbox': {'row': 2, 'column': 0, 'width': 4, 'height': 1,
                    },
                }

                unitbox = QGridLayout()
                config = self.configfile['namebox']
                unitbox.addWidget(self.set_namebox(), config['row'], config['column'], config['width'], config['height'])
                config = self.configfile['skillbox']
                unitbox.addWidget(self.set_skillbox(), config['row'], config['column'], config['width'], config['height'])
                config = self.configfile['listbox']
                unitbox.addWidget(self.set_listbox(), config['row'], config['column'], config['width'], config['height'])

                unitwidget = QWidget()
                unitwidget.setLayout(unitbox)
                tabs.addTab(unitwidget, f"{henchman.name}", )

                # set default tab to currentunit
                lenght = tabs.__len__()
                if henchman is self.mainwindow.currentunit:
                    tabs.setCurrentIndex(lenght - 1)
            
            tabs.addTab(QWidget(), f"+")

            tabs.currentChanged.connect(self.onclick)
            
            buttonwidget = self.set_buttonwidget()

            currentbox.addWidget(tabs)
            currentbox.addWidget(buttonwidget)
                
            return currentbox

    def onclick(self, signal):
        
        for squad in self.mainwindow.wbid.squadlist:
            for henchman in squad.henchmanlist:
                #just check if currentunit is part of this squad, doesnt matter which specific henchman it is, just which squad it is part of.
                if henchman is self.mainwindow.currentunit:
                    length = squad.henchmanlist.__len__()
                    
                    if signal == length and henchman.get_price() < self.mainwindow.wbid.treasury.gold:
                        # if signal is equal to length of henchman than the last tab has been selected to add a new unit
                        self.mainwindow.wbid.treasury.gold -= henchman.get_price()
                        squad.add_new_henchman()

                    elif signal == length and henchman.get_price() > self.mainwindow.wbid.treasury.gold:
                        # not enough money to add unit
                        message = QMessageBox.information(self, f"Not enough funds!", f"Current gold is {self.mainwindow.wbid.treasury.gold}, but {henchman.get_price()} is needed.", QMessageBox.Ok)
                        break

                    # set currentunit to this squads selected henchman based on the onclick signal if a character is selected
                    self.mainwindow.currentunit = squad.henchmanlist[signal]
                    break
        
        self.mainwindow.initUI()

    def set_buttonwidget(self):

        buttonbox = QHBoxLayout()

        btnrelease = QPushButton('Released from service', self)
        btnrelease.setToolTip(f"Remove unit from this warband. Paid gold is returned completely for base cost ({self.mainwindow.currentunit.price}) and items carried ({self.mainwindow.currentunit.get_item_costs()}).")
        btnrelease.clicked.connect(self.release_unit)

        btnkill = QPushButton('Perished in battle', self)
        btnkill.setToolTip(f"Remove unit from this warband. The unit fell in battle and items are not recovered / refunded.")
        btnkill.clicked.connect(self.kill_unit)

        btnnfc = QPushButton('Link to NFC (BETA)', self)
        btnnfc.setToolTip(f"Link character to a physical model (that has nfc capability)")
        btnnfc.clicked.connect(self.set_nfc_link)

        btnnfc_demo = QPushButton('check NFC (BETA)', self)
        btnnfc_demo.clicked.connect(self.get_nfc_link)

        buttonbox.addWidget(btnrelease)
        buttonbox.addWidget(btnkill)
        buttonbox.addWidget(btnnfc)
        buttonbox.addWidget(btnnfc_demo)

        buttonwidget = QWidget()
        buttonwidget.setLayout(buttonbox)
        buttonwidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        return buttonwidget

    def set_nfc_link(self):

        try:
            nfcdata = os.urandom(8)
            print(nfcdata)
            unique_id = int(nfcdata.hex(), 16)
            print(unique_id)
            
            # connect to card
            nfcconnect = NFCconnection.initialize()

            # make sure the card is clean
            nfcconnect.wipe_card()

            # write to nfc tag
            nfcconnect.write_card(nfcdata)

            # write to current unit
            self.mainwindow.currentunit.unique_id = unique_id
            message = QMessageBox.information(self, f"NFC written", f"Character ID ({self.mainwindow.currentunit.unique_id}) for character {self.mainwindow.currentunit.name} written succesfully to NFC.", QMessageBox.Ok)
            self.mainwindow.initUI()

        except:
            message = QMessageBox.information(self, f"Failed to connect to NFC!", f"Please try again and hold the NFC tag near the NFC reader (< 10 cm)!", QMessageBox.Ok)
            return

    def get_nfc_link(self):
        
        try:
            #connect to card
            nfcconnect = NFCconnection.initialize()

            # read tag
            nfcdata = nfcconnect.read_card()
            print(nfcdata)
            unique_id = int(nfcdata.hex(), 16)
            print(unique_id)

            idfound = False
            # check if id matches a hero
            for hero in self.mainwindow.wbid.herolist:

                if hero.unique_id == unique_id:
                    self.mainwindow.currentunit = hero
                    self.mainwindow.initUI()
                    idfound = True
                    break
            
            # If it didnt match any hero, check the squads
            if idfound == False:
                for squad in self.mainwindow.wbid.squadlist:
                        for henchman in squad.henchmanlist:
                            if henchman.unique_id == unique_id:
                                self.mainwindow.currentunit = henchman
                                self.mainwindow.initUI()
                                idfound = True
                                break

            if idfound == False:
                message = QMessageBox.information(self, f"Character not found!", f"Character with {unique_id} not found!", QMessageBox.Ok)

        except:
            message = QMessageBox.information(self, f"Failed to connect to NFC!", f"Please try again and hold the NFC tag near the NFC reader (< 10 cm)!", QMessageBox.Ok)
            return

    def set_namebox(self):
        namebox = QGridLayout()
        
        config = self.configfile['namebox']
        children = config['children']
        
        for key in children:
            config = children[key]
            label = QClickLabel()
            label.setText(config['text'])
            label.setToolTip(config['tooltip'])
            if config['connect'] != "":
                label.clicked.connect(config['connect'])
            namebox.addWidget(label, config['row'], config['column'], config['width'], config['height'])

        nameframe = QBorderlessFrame()
        nameframe.setLayout(namebox)
        
        return nameframe

    def set_skillbox(self):
        #show skills in middle
        skillbox = QHBoxLayout() # create a horizontal layout to show the skills in a neat line
        
        skilldict = self.mainwindow.currentunit.get_total_skilldict()
        for key in skilldict:
            label = QLabel()
            label.setText(f"{key[:2]}<br/><b>{skilldict[key]['total']}</b>")
            
            # build tooltip - base
            tooltip = f"The total <b>{key}</b> skill of this character<br/><br/>The base {key} of this character is: {skilldict[key]['children']['base']}<br/>"
            # add events
            tooltip += "<br/>The change due to events is: <br/>"
            for key2 in skilldict[key]['children']:
                if key2[:7] == 'Advance' or key2[:5] == 'event':
                    tooltip += f" - {key2}: {skilldict[key]['children'][key2]}<br/>"
            # add items
            tooltip += "<br/>The change due to items is: <br/>"
            for key2 in skilldict[key]['children']:
                if key2[:4] == 'item':
                    tooltip += f" - {key2[6:]}: {skilldict[key]['children'][key2]}<br/>"

            label.setToolTip(tooltip)

            label.setAlignment(Qt.AlignCenter)
            box = QVBoxLayout()
            box.addWidget(label)
            frame = QFlatFrame()
            frame.setLayout(box)
            skillbox.addWidget(frame)

        skillframe = QBorderlessFrame()
        skillframe.setLayout(skillbox)

        return skillframe

    def set_listbox(self):
        
        listbox = QGridLayout()

        # for character
        listbox.addWidget(WidgetAbility(self.mainwindow, abilitylist = self.mainwindow.currentunit.abilitylist, skip = False), 0, 0) # adds the ability layout to the grid
        listbox.addWidget(WidgetMagic(self.mainwindow), 1, 0) # adds the magic layout to the grid

        # now for every item repeated
        listbox.addWidget(WidgetItemsUnit(self.mainwindow), 0, 1, 2, 2)
        
        listframe = QBorderlessFrame()
        listframe.setLayout(listbox)
        
        return listframe

    def create_method_change_name(self, unit):
        
        def change_name():
            new_name, okPressed = QInputDialog.getText(self, "Choose a name", "Name your unit:", text="default")
            if okPressed and new_name:
                unit.name = new_name
                self.mainwindow.currentunit = unit
                self.mainwindow.initUI()
        
        return change_name

    def create_method_change_experience(self):
        
        def change_experience():

            unit = self.mainwindow.currentunit

            change_experience, okPressed = QInputDialog.getInt(self, "Change Experience", "How much to increase the experience?", 0, -99, 99, 1)
            if okPressed and change_experience:
                if unit.ishero == True:
                    unit.add_experience(change_experience)
                    self.mainwindow.initUI()
                else:
                    for squad in self.mainwindow.wbid.squadlist:
                        if unit is squad.henchmanlist[0]:
                            squad.add_experience(change_experience)
                            self.mainwindow.initUI()
                            break
        
        return change_experience

    def create_method_levelup(self):

        def levelup():

            # Check if something has to be done at all, can the unit level up
            currentunit = self.mainwindow.currentunit
            tbd_advance_events = currentunit.get_tbd_advance_events()
            process = self.mainwindow.currentunit.get_advance_process()  

            # check if there are any open advance events
            if len(tbd_advance_events) > 0:
                # Trow roll1 (2D6)
                roll1, okPressed = QInputDialog.getInt(self, "Roll 2D6 for advance", process, 2, 2, 12, 1)
                if okPressed and roll1 and currentunit.ishero == True:
                    # get first advance event of the hero
                    event = tbd_advance_events[0]
                    if roll1 <= 5 or roll1 >= 10:
                        items = ["Ability", "Magic"]
                        choice, okPressed = QInputDialog.getItem(self, "Choose ability or magic", "Choose if you would prefer to add ability or add magic (magic users only)", items, 0, False)
                        if okPressed and choice == "Ability":
                            new_ability = WidgetAbility.dialog_new_ability(self.mainwindow)
                            result = currentunit.set_event_ability(event, new_ability)

                        elif okPressed and choice == "Magic":
                            new_magic = WidgetMagic.dialog_new_magic(self.mainwindow)
                            result = currentunit.set_event_magic(event, new_magic)
                                           
                    elif roll1 == 7:
                        items = ["Weapon Skill", "Ballistic Skill"]
                        choice, okPressed = QInputDialog.getItem(self, "Choose weapon skill or Ballistic skill", "Choose if you would prefer to add 1 to your weapon skill or to your ballistic skill", items, 0, False)
                        if okPressed and choice:
                            result = currentunit.set_event_roll7(event, choice)

                    elif roll1 == 6 or roll1 == 8 or roll1 == 9:
                        if roll1 == 6:
                            characteristics = "strength or attack."
                        elif roll1 == 8:
                            characteristics = "initiative or leadership."
                        elif roll1 == 9:
                            characteristics = "wounds or toughness"

                        roll2, okPressed = QInputDialog.getInt(self, "Roll 1D6", f"Trow 1D6 to see if your character gains +1 to their {characteristics}", 1, 1, 6, 1)
                        if okPressed and roll2:
                            result = currentunit.set_event_characteristic(event, roll1, roll2)

                    message = QMessageBox.information(self, f"Character gained {event.category}!", result, QMessageBox.Ok)

                # Trow roll1 (2D6)
                elif okPressed and roll1 and currentunit.ishero == False:
                    # get squad
                    for squad in self.mainwindow.wbid.squadlist:
                        for henchman in squad.henchmanlist:
                            if currentunit is henchman:
                                currentsquad = squad
                                break
                                break

                    Squadalive = True
                    if roll1 >= 10 and roll1 <= 12:

                        currentunit.ishero = True
                        self.mainwindow.wbid.herolist += [currentunit]
                        currentunit.eventlist.append(Event.create_event(
                            category = "Became Hero", 
                            skill = Skill.create_skill_empty(), 
                            description = "This character showed to be above its peers and became a hero of its people!"
                        ))
                        index = currentsquad.henchmanlist.index(currentunit)
                        currentsquad.henchmanlist.pop(index)

                        result = f"Character {currentunit.name} of your squad {currentsquad.name} proved himself beyond his peers and became a hero!"
                        message = QMessageBox.information(self, f"This lads got talent!", result, QMessageBox.Ok)

                        if currentsquad.get_totalhenchman() == 0:
                            index = self.mainwindow.wbid.squadlist.index(currentsquad)
                            self.mainwindow.wbid.squadlist.pop(index)
                            Squadalive = False

                        self.mainwindow.initUI()

                        # Trow roll1 (2D6)
                        if Squadalive == True:
                            roll1, okPressed = QInputDialog.getInt(self, "Roll 2D6 for advance", process, 2, 2, 9, 1)

                    if Squadalive == True:
                        for henchman in currentsquad.henchmanlist:

                            # get first advance event of the henchman
                            event = henchman.get_tbd_advance_events()[0]

                            if roll1 >= 6 and roll1 <= 7:
                                items = ["Weapon Skill", "Ballistic Skill"]
                                choice, okPressed = QInputDialog.getItem(self, "Choose weapon skill or Ballistic skill", "Choose if you would prefer to add 1 to your weapon skill or to your ballistic skill", items, 0, False)
                                if okPressed and choice:
                                    result = henchman.set_event_roll7(event, choice)

                            else:
                                if roll1 >= 2 and roll1 <= 4:
                                    characteristics = "initiative"
                                    changeroll1 = 8
                                    changeroll2 = 1
                                elif roll1 == 5:
                                    characteristics = "strength"
                                    changeroll1 = 6
                                    changeroll2 = 1
                                elif roll1 == 8:
                                    characteristics = "attack"
                                    changeroll1 = 6
                                    changeroll2 = 6
                                elif roll1 == 9:
                                    characteristics = "leadership"
                                    changeroll1 = 8
                                    changeroll2 = 6
                                result = henchman.set_event_characteristic(event, changeroll1, changeroll2)

                        message = QMessageBox.information(self, f"Character gained {event.category}!", result, QMessageBox.Ok)
                    else:
                        message = QMessageBox.information(self, f"Squad disbanded!", f"Squad {currentsquad.name} lost all its henchmen!", QMessageBox.Ok)
                else:
                    print("advancement canceled")

                self.mainwindow.initUI()

            # input dialog with process and choice add skill or add characteristic

            # input dialog for the process of adding a skill and input items combobox
            #  adding new abilities: There are several types of skill and each has a separate list. You may not choose the same skill twice for the same warrior. The skills a Hero may have are restricted by the warband he belongs to and what type of Hero he is. To select a new skill for a Hero, pick the type of skill you want from those available, then choose which skill has been learned. 

            # input dialog for the process of adding a characteristic and input items combobox
            # Characteristics for certain warriors may not be increased beyond the maximum limits shown on the following profiles. If a characteristic is at its maximum, take the other option or roll again if you can only increase one characteristic. If both are already at their racial maximum, you may increase any other (that is not already at its racial maximum) by +1 instead. Note that this is the only way to gain the maximum Movement for some races. Remember that Henchmen can only add +1 to any characteristic.
            
            # insert limit of the current race (to be implemented)
            # HUMAN (Witch Hunters, Flagellants, Mercenaries, Dregs, Freelancers, Warlocks, Pit Fighters, Magisters, Darksouls, Mutants, Brethren, Warrior Priests, Zealots, Sisters of Sigmar, etc.) Profile M WS BS S T W I A Ld Human 4 66443649 
            # ELF (Elf Ranger Hired Sword) Profile M WS BS S T W I A Ld Elf 5 7 7 4 4 3 9 4 10 
            # DWARF (Troll Slayer Hired Sword) Profile M WS BS S T W I A Ld Dwarf 3 7 6 4 5 3 5 4 10
            # OGRE (Ogre Bodyguard Hired Sword) Profile M WS BS S T W I A Ld Ogre 6 65555659 
            # HALFLING (Halfling Scout Hired Sword) Profile M WS BS S T W I A Ld Halfling 4 5 7 3 3 3 9 4 10 
            # BEASTMAN Profile M WS BS S T W I A Ld Gor 4 7 6 4 5 4 6 4 9
            # POSSESSED Profile M WS BS S T W I A Ld Possessed 6 8 0 6 6 4 7 5 10
            # VAMPIRE Profile M WS BS S T W I A Ld Vampire 6 8 6 7 6 4 9 4 10
            # SKAVEN Profile M WS BS S T W I A Ld Skaven 6 66443747 
            # GHOUL Profile M WS BS S T W I A Ld Ghoul 5 52453557

        return levelup

    def release_unit(self):
        
        remove = QMessageBox.question(self, "Release unit?", "Are you sure to release this unit?", QMessageBox.Yes | QMessageBox.No)
        if remove == QMessageBox.Yes:

            self.mainwindow.wbid.treasury.gold += self.mainwindow.currentunit.get_price()
            self.remove_unit()

    def kill_unit(self):

        remove = QMessageBox.question(self, "Unit perished", "Are you sure to remove this character from the game?", QMessageBox.Yes | QMessageBox.No)
        if remove == QMessageBox.Yes:

            self.remove_unit()

    def remove_unit(self):

        if self.mainwindow.currentunit.ishero == True:
            index = self.mainwindow.wbid.herolist.index(self.mainwindow.currentunit)
            self.mainwindow.wbid.herolist.pop(index)
            self.mainwindow.currentunit = Character.create_template()

        elif self.mainwindow.currentunit.ishero == False:
            # get squad
            for squad in self.mainwindow.wbid.squadlist:
                for henchman in squad.henchmanlist:
                    if self.mainwindow.currentunit is henchman:
                        index = squad.henchmanlist.index(henchman)
                        squad.henchmanlist.pop(index)

                        try:
                            self.mainwindow.currentunit = squad.henchmanlist[0]
                        except:
                            index = self.mainwindow.wbid.squadlist.index(squad)
                            self.mainwindow.wbid.squadlist.pop(index)
                            self.mainwindow.currentunit = Character.create_template()

        self.mainwindow.initUI()