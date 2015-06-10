import pickle #Module which stores data in a file
import operator #Module that allows sorting
import pygame #GUI module
import sys #System module
from pygame.locals import * #Imports everything from the pygame locals module
from itertools import groupby #Module that segregates lists
from time import sleep #Imports sleep method from time module

#create Contact class
class Contact():
    #Initialise Contact object with following parameters
    def __init__(self, firstName, lastName, address, groupType,
                 telephone, mobile, email, photoField):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.groupType = groupType
        self.telephone = telephone
        self.mobile = mobile
        self.email = email
        self.photoField = photoField

    #Create class method for AddressBook class to call on; defines Contact object
    #'cls' class method's version of 'self'
    @classmethod
    def from_input(cls):
        firstName = ffName.capitalize()
        lastName = llName.capitalize()
        address = aaddRess
        telephone = ttelPhone
        mobile = mmoBile
        email = eeMail
        return cls(firstName, lastName, address, None, ttelPhone,
                   
                   mobile, eeMail, None)
    
#create Address Book class
class AddressBook():
    def __init__(self):
        self.contactsList = pickle.load(open("save.p", "rb")) #Sets list to pickle file storing contact data

    def addContact(self, contact = None):
        if contact is None: #checks if object 'contact' returns None
            contact = Contact.from_input() #Calls on class method from Contact class to add a new contact
        self.contactsList.append(contact) #Appends Contact object to list
        pickle.dump(self.contactsList, open("save.p", "wb")) #Saves latest list to pickle file

    def delContact(self, contact = None):
        if contact is None:
            for j in self.contactsList: #loops through each Contact object in pickle file
                #checks if contact in pickle file matches the contact selected from end-user
                if j.firstName == indexedContacts[i].firstName and j.lastName == indexedContacts[i].lastName and j.mobile == indexedContacts[i].mobile:
                    indexed = self.contactsList.index(j) #returns contact's index value in list
                    del self.contactsList[indexed] #removes contact from list
                    pickle.dump(self.contactsList, open("save.p", "wb")) #saves updated list in pickle file
                else:
                    continue

#creates Page class; default template for all pages in app
class Page():
    #Initialises pygame screen, surfaces and window caption
    def __init__(self, screen = pygame.display.set_mode((320, 480)), caption = pygame.display.set_caption("Contacts"),
                 intermediate = pygame.Surface((320, 4000)), intermediate2 = pygame.Surface((320, 4000))):
        self.screen = screen
        self.caption = caption
        self.intermediate = intermediate
        self.intermediate2 = intermediate2

    #Defines the style of all pages
    def style(self):
        pygame.draw.rect(self.intermediate, (171,0,0), (0,0,320,63), 0) #Page header
        pygame.draw.line(self.intermediate, (120,0,0), (5,61), (320, 61), 2) #Page header and body divider
        i_a = self.intermediate2.get_rect() #retrieves dimensions of intermediate2 surface
        x1 = i_a[1] #sets value to 1st value of tuple from i_a
        x2 = x1 + i_a[2] #adds the value of 2nd value of tuple to x1
        y1 = 0
        y2 = 4000

        #draws Page body; needed so that scrolling can take place
        for line in range(y1,y2):
            pygame.draw.line(self.intermediate2, (230,230,230), (x1, line), (x2, line))

#inherits Page class attributes
class MainPage(Page):
    def __init__(self, screen = pygame.display.set_mode((320, 480)), caption = pygame.display.set_caption("Contacts"),
                 title = "Contacts", intermediate = pygame.Surface((320, 4000)), intermediate2 = pygame.Surface((320, 4000))):
        Page.__init__(self, screen, caption, intermediate, intermediate2)
        self.title = title #points to MainPage's title

    def style(self):
        Page.style(self) #retrives style from Page class
        titleFont = pygame.font.SysFont("trebuchet ms", 38) #defines font type and size for MainPage title
        textSurface = titleFont.render(self.title, True, (255,255,255)) #renders title
        self.intermediate.blit(textSurface, (5, 18)) #draws title on to header

        #draws "Add Contact" button; difficulties in creating separate Button class and
        #drawing on to intermediate surface
        pygame.draw.rect(self.intermediate, (120,0,0), (270,12,40,40), 0)
        pygame.draw.line(self.intermediate, (255,255,255), (289.75, 15), (289.75,48))
        pygame.draw.line(self.intermediate, (255,255,255), (272, 32), (307, 32))


    #draws each contact in pickle file on to intermediate2 surface
    def printContacts(self):
        addressBook = AddressBook() #sets addressBook as instance of AddressBook class
        addressBook.contactsList #calls on contactList object from AddressBook class

        #sorts contactList by last name; if no last name, then orders by first name with same precedance
        addressBook.contactsList.sort(key = lambda c: (c.lastName, c.firstName) if c.lastName else (c.firstName, ""))
        contactFont = pygame.font.SysFont("trebuchet ms", 18) #sets font type and size for Contact objects
        global indexedContacts #creates global dictionary; y value of a printed contact is unique to the contact being printed
        indexedContacts = {} #y value key defined by contact object
        global yIndex #creates global list; appends each y value
        yIndex = [] #used for adjusting y values when page is scrolled
        y = 20 #initial y value to print from


        #First for loop generates alphabetical dividers to categorise each contact in to
        for (key, g) in groupby(addressBook.contactsList, lambda c: c.lastName[0] if c.lastName else c.firstName[0]):
            groupName = contactFont.render(key, True, (171,0,0))
            self.intermediate2.blit(groupName, (5, y))
            pygame.draw.line(self.intermediate2, (0,0,0), (5,(y+20)), (320, (y+20)), 1)
            y += 30

            #Sub for loop prints contact under respective divider
            for i in g:
                name = i.firstName + " " + i.lastName
                textName = contactFont.render(name, True, (0,0,0))
                pygame.draw.line(self.intermediate2, (210,210,210), (5,(y+20)), (320, (y+20)), 1)
                self.intermediate2.blit(textName, (5, y))
                indexedContacts[(y+72)] = i #y value key defined by contact value 'i'
                yIndex.append((y+72)) #stores y value in yIndex list
                y += 30

        global finalY #global variable which provides the length of list; needed for scroll limitation
        finalY = y * -1

#takes inheritence from Page class        
class AddPage(Page):
    def __init__(self, screen = pygame.display.set_mode((320, 480)), caption = pygame.display.set_caption("Contacts"),
                 title = "Add Contact", intermediate = pygame.Surface((320, 4000)), intermediate2 = pygame.Surface((320, 4000))):
        Page.__init__(self, screen, caption, intermediate, intermediate2)
        self.title = title

    def style(self):
        Page.style(self)
        titleFont = pygame.font.SysFont("trebuchet ms", 38)
        textSurface = titleFont.render(self.title, True, (255,255,255))
        self.intermediate.blit(textSurface, (5, 18))

        #draws 'Confirm Add Contact' and 'cancel' button
        pygame.draw.rect(self.intermediate, (120,0,0), (270,12,40,40), 0)
        pygame.draw.aaline(self.intermediate, (255,255,255), (284.5, 43), (303,21))
        pygame.draw.aaline(self.intermediate, (255,255,255), (276.5, 31.5), (284.5, 43))
        pygame.draw.rect(self.intermediate, (120,0,0), (245,20,25,25), 0)
        pygame.draw.aaline(self.intermediate, (255,255,255), (252,32.5), (263,26))
        pygame.draw.aaline(self.intermediate, (255,255,255), (252,32.5), (263,39))

    #instance method which prints each field of the Add Contact page
    def textInputs(self):
        fields = ["First Name: ", "Last Name: ", "Address: ", "Mobile: ", "Telephone: ", "Email: "]
        Y = 20
        contactFont = pygame.font.SysFont("trebuchet ms", 18)
        
        for i in fields:
            prompts = contactFont.render(i, True, (0,0,0))
            self.intermediate2.blit(prompts, (5,Y))
            #Address field requires more lines than other fields; if statement does this
            if i == "Address: ":
                Y += 30
                for j in range(4):
                    pygame.draw.line(self.intermediate2, (210,210,210), (5,Y), (320, Y), 1)
                    Y += 30
            elif i != "Address: ":
                pygame.draw.line(self.intermediate2, (210,210,210), (5, (Y+30)), (320, (Y+30)), 1)
                Y += 50

        global finalY
        finalY = Y * -1

#takes inheritence from Page class
class EditPage(Page):
    def __init__(self, screen = pygame.display.set_mode((320, 480)), caption = pygame.display.set_caption("Contacts"),
                 title = "Details", intermediate = pygame.Surface((320, 4000)), intermediate2 = pygame.Surface((320, 4000))):
        Page.__init__(self, screen, caption, intermediate, intermediate2)
        self.title = title

    def style(self):
        Page.style(self)
        titleFont = pygame.font.SysFont("trebuchet ms", 38)
        textSurface = titleFont.render(self.title, True, (255,255,255))
        self.intermediate.blit(textSurface, (5, 18))

        #draws 'Back' button
        pygame.draw.rect(self.intermediate, (120,0,0), (270,12,40,40), 0)
        pygame.draw.aaline(self.intermediate, (255,255,255), (279.5,32), (297.5,23))
        pygame.draw.aaline(self.intermediate, (255,255,255), (279.5,32), (297.5,41))

        #draws 'Delete Contact' button
        pygame.draw.rect(self.intermediate2, (120,0,0), (5, 410, 310, 40), 0)
        deleteFont = pygame.font.SysFont("trebuchet ms", 25)
        delButtonSurface = deleteFont.render("Delete", True, (255,255,255))
        self.intermediate2.blit(delButtonSurface, (124, 414.5))

    def contactFields(self):
        thinChar = ["f","i","j","l","s","t","I"] #Characters that are thin
        fatChar = ["m","w","G","H","M","N","O","Q","U","V","W","@"] #Characters that are fat
        AddPage.textInputs(self)
        global finalY
        finalY = -430

        #prints paramters of selected contact into each field
        contactSelected = indexedContacts[i]
        contactFont = pygame.font.SysFont("trebuchet ms", 18)
        contact = contactFont.render(contactSelected.firstName, True, (0,0,0))
        self.intermediate2.blit(contact, (106,20))
        contact = contactFont.render(contactSelected.lastName, True, (0,0,0))
        self.intermediate2.blit(contact, (106,70))
        contact = contactFont.render(contactSelected.mobile, True, (0,0,0))
        self.intermediate2.blit(contact, (77,271))
        contact = contactFont.render(contactSelected.telephone, True, (0,0,0))
        self.intermediate2.blit(contact, (112,321))
        contact = contactFont.render(contactSelected.email, True, (0,0,0))
        self.intermediate2.blit(contact, (72,370))

        #showing address parameter of selected contact requires unique code
        #to present properly
        x = 87
        address = []
        for char in contactSelected.address:
            address.append(char)
        for char in address:
            if x <= 306:
                contact = contactFont.render(char, True, (0,0,0))
                self.intermediate2.blit(contact, (x,120))
                if char in thinChar:
                    x += 7
                elif char in fatChar:
                    x += 15
                else:
                    x += 10
            elif x > 306 and x <= 612:
                contact = contactFont.render(char, True, (0,0,0))
                self.intermediate2.blit(contact, (x - 301,156))
                if char in thinChar:
                    x += 7
                elif char in fatChar:
                    x += 15
                else:
                    x += 10
            elif x > 612 and x <= 918:
                contact = contactFont.render(char, True, (0,0,0))
                self.intermediate2.blit(contact, (x - 613,186))
                if char in thinChar:
                    x += 7
                elif char in fatChar:
                    x += 15
                else:
                    x += 10
            elif x > 918 and x <= 1224:
                contact = contactFont.render(char, True, (0,0,0))
                self.intermediate2.blit(contact, (x - 921,216))
                if char in thinChar:
                    x += 7
                elif char in fatChar:
                    x += 15
                else:
                    x += 10

                    
global scroll_y
scroll_y = 63 #y value for scroll

global originalScroll_y
originalScroll_y = scroll_y #used to adjust yIndex values when screen scrolled

control2 = 0 #variable which looks at the difference between originalScroll_y and new scroll_y value

pygame.init() #initialises pygame module
page = MainPage() #sets object page to MainPage class
page.style() #calls on style method from MainPage class
page.printContacts() #calls on printContacts method

#sets object to sound file; used for significant events
buttonSound = pygame.mixer.Sound("pop.ogg")

#sets object to module which regulates framerate for app
clock = pygame.time.Clock()

xX = 106 #First Name Field x value
xXX = 106 #Last Name Field x value
xXXX = 87 #Address Fields x value
xXXXX = 77 #Mobile Field x value
xXXXXX =  112 #Telephone Field x value
xXXXXXX = 72 #Email Field x value

invalidChar = ["\r","\x08","","\t","\x1b"] #Characters not allowed in text fields 
thinChar = ["f","i","j","l","s","t","I"] #Characters that are thin
fatChar = ["m","w","G","H","M","N","O","Q","U","V","W","@"] #Characters that are fat

fName = [] #List for storing First Name characters
lName = [] #List for storing Last Name characters
addRess = [] #List for storing Address characters
moBile = [] #List for storing Mobile numbers
telPhone = [] #List for storing Telephone numbers
eMail = [] #List for storing Email

global ffName #Global var that stores First Name
global llName #Global var that stores Last Name
global aaddRess #Global var that stores Address
global mmoBile #Global var that stores Mobile
global ttelPhone #Global var that stores Telephone
global eeMail #Global var that stores Email

while True: #Main App Loop

    #captures events
    for event in pygame.event.get():
        #Checks whether user has quit application
        #can be exit button or escape button
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
            
        #Checks if user has scrolled
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #can only scroll up if scroll_y isn't 63
            if event.button == 4 and scroll_y != 63:
                scroll_y = min(scroll_y + 15, 63) #adds 15 to scroll_y

            #scroll down
            if event.button == 5:
                #as scroll down subtracts 15, numbers will eventually go negative
                #therefore a sine graph effect takes place, where numbers less
                #than -63 will react the same as positive numbers
                if scroll_y < 0:
                    if scroll_y > -63 and -scroll_y < -finalY:
                            scroll_y = max(scroll_y - 15, finalY + 470)
                    elif scroll_y < -63 and -(scroll_y-470) < -(finalY) :
                        scroll_y = max(scroll_y - 15, finalY + 470)
                    else:
                        scroll_y = scroll_y
                else:
                    if -finalY >= 430 and (isinstance(page, MainPage) or isinstance(page, AddPage)):
                        scroll_y = max(scroll_y - 15, finalY + 470)
                    elif -finalY >= 420 and isinstance(page, EditPage):
                        scroll_y = max(scroll_y - 15, finalY + 452)
                    

        #event code for either clicking on the Add Contact Button or a contact    
        elif event.type == MOUSEBUTTONUP and event.button == 1 and isinstance(page, MainPage):
            x, y = pygame.mouse.get_pos() #unpacks mouse coordinates into x and y variables
            
            #Checks if user has clicked Add Contact button
            if (x >= 270) and (x <= 310) and (y >= scroll_y - 50) and (y <= scroll_y - 10):
                buttonSound.play()
                sleep(0.5)
                scroll_y = 63
                page = AddPage()
                page.style()
                page.textInputs()

            #Checking to see if user has clicked on a contact
            else:
                #Sine graph effect
                if scroll_y < 0:
                    if scroll_y > -63:
                        scrollvalue = scroll_y * -1
                        control = originalScroll_y - scrollvalue
                    elif scroll_y <= -63:
                        scrollvalue = scroll_y
                        control = originalScroll_y - scrollvalue
                else:
                    scrollvalue = scroll_y
                    #uses the difference between scroll values to adjust yIndex values
                    control = originalScroll_y - scrollvalue

                #making sure the control value hasn't already been used
                #therefore adjusting the yIndex values incorrectly
                if control != control2:
                    for k, j in enumerate(yIndex):
                        l = j - control #new yIndex value
                        indexedContacts[l] = indexedContacts.pop(j) #replaces original value with new value in dictionary
                        yIndex[k] = l #changes the value at specified index in yIndex list
                        control2 = control #sets control2 to current control value
                        
                #looping through each item in yIndex           
                for i in yIndex:
                    #allows for error range in user click
                    if y >= (i - 10) and y <= (i + 20):
                        #if y value matches value in yIndex, switch pages with relative
                        #contact details
                        if i in indexedContacts:
                            buttonSound.play() #plays sound
                            sleep(0.5) #using sleep to synchronise sound with page switch
                            scroll_y = 63
                            page = EditPage()
                            page.style()
                            page.contactFields()
                            break #return to main app loop

        #Event code for Add Contact Page
        elif event.type == MOUSEBUTTONUP and event.button == 1 and isinstance(page, AddPage):
            x, y = pygame.mouse.get_pos()
            #Checks if user has clicked the Add Contact Confirm button
            if (x >= 270) and (x <= 310) and (y >= scroll_y - 50) and (y <= scroll_y - 10):
                #Contact cannot be processed if first name is empty
                if fName != []:
                    ffName = "".join(fName)
                    #checks whether or not each field is completed
                    #and applies appropriate action
                    if lName != []:
                        llName = "".join(lName)
                    else:
                        llName = ""
                    if addRess != []:
                        aaddRess = "".join(addRess)
                    else:
                        aaddRess = ""
                    if moBile != []:
                        mmoBile = "".join(moBile)
                    else:
                        mmoBile = ""
                    if telPhone != []:
                        ttelPhone = "".join(telPhone)
                    else:
                        ttelPhone = ""
                    if eMail != []:
                        eeMail = "".join(eMail)
                    else:
                        eeMail = ""
                    #contact object calls on addContact method from AddressBook class
                    contact = AddressBook().addContact()
                    #resets everything and takes you back to the Main Page
                    fName = []
                    lName = []
                    addRess = []
                    moBile = []
                    telPhone = []
                    eMail = []
                    xX = 106
                    xXX = 106
                    xXXX = 87
                    xXXXX = 77
                    xXXXXX = 112
                    xXXXXXX = 72
                    buttonSound.play()
                    sleep(0.5)
                    scroll_y = 63
                    control2 = 0
                    page = MainPage()
                    page.style()
                    page.printContacts()
                else:
                    continue
                
            #Checks if user has clicked the Cancel button
            #resets everything
            elif (x >= 245) and (x <= 270) and (y >= scroll_y - 43) and (y <= scroll_y - 18):
                fName = []
                lName = []
                addRess = []
                moBile = []
                telPhone = []
                eMail = []
                xX = 106
                xXX = 106
                xXXX = 87
                xXXXX = 77
                xXXXXX = 112
                xXXXXXX = 72
                buttonSound.play()
                sleep(0.5)
                scroll_y = 63
                control2 = 0
                page = MainPage()
                page.style()
                page.printContacts()

            #Below is the code for typing into each field in the AddContact page
            #Due to inappropriate widgets/modules available for allowing text input from the
            #user, I created the code which captures every key pressed, checked
            #against the invalid keys in the invalidChar list. Each key is then
            #blitted on the screen.

            #However, it essentially becomes repeatable code, with the only changes in
            #the starting x value and y value. Since writing the code to process one
            #input took so much time, I couldn't develop a function which reduced the
            #code to just calling the function name. If I was to create a function,
            #I would have done some thing like 'def keyInput(x, y)', where x is the starting
            #x value, and y the starting y value, defined when calling the function.

            #I took the wrong approach with the Address field, instead of having separate
            #variables for street, town, city, I had it as one, making the text input
            #far more difficult than it needed to be.

            #First Name Field
            elif (x >= 5) and (x <= 320) and (y >= 16 + scroll_y) and (y < 46 + scroll_y):
                pygame.draw.line(page.intermediate2, (0,0,0), (5, 50), (320, 50), 1)
                while True: #Sub App Loop, needed for the capture of typing events
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP and event.button == 1:
                            x, y = pygame.mouse.get_pos()
                        elif event.type == KEYDOWN and (event.unicode not in invalidChar)  and xX <= 306:
                            char = event.unicode
                            fName.append(char)
                            contactFont = pygame.font.SysFont("trebuchet ms", 18)
                            textName = contactFont.render(char, True, (0,0,0))
                            page.intermediate2.blit(textName, (xX, 20))
                            if event.unicode in thinChar:
                                xX += 7
                            elif event.unicode in fatChar:
                                xX += 15
                            else:
                                xX += 10
                        elif event.type == KEYDOWN and event.key == 8 and xX >= 112:
                            if len(fName) >= 1:
                                charDel = len(fName) - 1
                                if char in thinChar:
                                    xX -= 7
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xX,20,7,25), 0)
                                    del fName[charDel]
                                    if len(fName) >= 1:
                                        char = fName[charDel - 1]
                                    else:
                                        continue
                                elif char in fatChar:
                                    xX -= 15
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xX,20,15,25), 0)
                                    del fName[charDel]
                                    if len(fName) >= 1:
                                        char = fName[charDel - 1]
                                    else:
                                        continue
                                else:
                                    xX -= 10
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xX,20,10,25), 0)
                                    del fName[charDel]
                                    if len(fName) >= 1:
                                        char = fName[charDel - 1]
                                    else:
                                        continue
                            else:
                                continue

                    #prints the page appropriate to the scroll_y value
                    Page().screen.blit(page.intermediate, (0, scroll_y - 63))
                    Page().screen.blit(page.intermediate2, (0, scroll_y))
                    clock.tick(60) #set the framerate to 60fps
                        
                    pygame.display.update() #updates the screen
                    
                    #breaks from the sub loop
                    if (y < 16 + scroll_y) or (y > 46 + scroll_y):
                        pygame.draw.line(page.intermediate2, (210,210,210), (5, 50), (320, 50), 1)
                        break
                    else:
                        continue

            #Last Name Field   
            elif (x >= 5) and (x <= 320) and (y >= 46 + scroll_y) and (y < 97 + scroll_y):
                pygame.draw.line(page.intermediate2, (0,0,0), (5, 100), (320, 100), 1)
                while True:
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP and event.button == 1:
                            x, y = pygame.mouse.get_pos()
                        elif event.type == KEYDOWN and (event.unicode not in invalidChar)  and xXX <= 306:
                            char = event.unicode
                            lName.append(char)
                            contactFont = pygame.font.SysFont("trebuchet ms", 18)
                            textName = contactFont.render(char, True, (0,0,0))
                            page.intermediate2.blit(textName, (xXX, 70))
                            if event.unicode in thinChar:
                                xXX += 7
                            elif event.unicode in fatChar:
                                xXX += 15
                            else:
                                xXX += 10
                        elif event.type == KEYDOWN and event.key == 8 and xXX >= 112:
                            if len(lName) >= 1:
                                charDel = len(lName) - 1
                                if char in thinChar:
                                    xXX -= 7
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXX,70,7,25), 0)
                                    del lName[charDel]
                                    if len(lName) >= 1:
                                        char = lName[charDel - 1]
                                    else:
                                        continue
                                elif char in fatChar:
                                    xXX -= 15
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXX,70,15,25), 0)
                                    del lName[charDel]
                                    if len(lName) >= 1:
                                        char = lName[charDel - 1]
                                    else:
                                        continue
                                else:
                                    xXX -= 10
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXX,70,10,25), 0)
                                    del lName[charDel]
                                    if len(lName) >= 1:
                                        char = lName[charDel - 1]
                                    else:
                                        continue
                            else:
                                continue

                    Page().screen.blit(page.intermediate, (0, scroll_y - 63))
                    Page().screen.blit(page.intermediate2, (0, scroll_y))
                    clock.tick(60)
                        
                    pygame.display.update()

                    if (y < 46 + scroll_y) or (y > 97 + scroll_y):
                        pygame.draw.line(page.intermediate2, (210,210,210), (5, 100), (320, 100), 1)
                        break
                    else:
                        continue

            #Address Field
            elif (x >= 5) and (x <= 320) and (y >= 107 + scroll_y) and (y < 237 + scroll_y):
                pygame.draw.line(page.intermediate2, (0,0,0), (5,150), (320, 150), 1)
                pygame.draw.line(page.intermediate2, (0,0,0), (5,180), (320, 180), 1)
                pygame.draw.line(page.intermediate2, (0,0,0), (5,210), (320, 210), 1)
                pygame.draw.line(page.intermediate2, (0,0,0), (5,240), (320, 240), 1)
                while True:
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP and event.button == 1:
                            x, y = pygame.mouse.get_pos()
                        elif event.type == KEYDOWN and (event.unicode not in invalidChar):
                            if xXXX <= 306:
                                char = event.unicode
                                addRess.append(char)
                                contactFont = pygame.font.SysFont("trebuchet ms", 18)
                                textName = contactFont.render(char, True, (0,0,0))
                                page.intermediate2.blit(textName, (xXXX, 120))
                                if event.unicode in thinChar:
                                    xXXX += 7
                                elif event.unicode in fatChar:
                                    xXXX += 15
                                else:
                                    xXXX += 10
                            elif xXXX > 306 and xXXX <= 612:
                                char = event.unicode
                                addRess.append(char)
                                contactFont = pygame.font.SysFont("trebuchet ms", 18)
                                textName = contactFont.render(char, True, (0,0,0))
                                page.intermediate2.blit(textName, (xXXX - 301, 156))
                                if event.unicode in thinChar:
                                    xXXX += 7
                                elif event.unicode in fatChar:
                                    xXXX += 15
                                else:
                                    xXXX += 10
                            elif xXXX > 612 and xXXX <= 918:
                                char = event.unicode
                                addRess.append(char)
                                contactFont = pygame.font.SysFont("trebuchet ms", 18)
                                textName = contactFont.render(char, True, (0,0,0))
                                page.intermediate2.blit(textName, (xXXX - 613, 186))
                                if event.unicode in thinChar:
                                    xXXX += 7
                                elif event.unicode in fatChar:
                                    xXXX += 15
                                else:
                                    xXXX += 10
                            elif xXXX > 918 and xXXX <= 1224:
                                char = event.unicode
                                addRess.append(char)
                                contactFont = pygame.font.SysFont("trebuchet ms", 18)
                                textName = contactFont.render(char, True, (0,0,0))
                                page.intermediate2.blit(textName, (xXXX - 921, 216))
                                if event.unicode in thinChar:
                                    xXXX += 7
                                elif event.unicode in fatChar:
                                    xXXX += 15
                                else:
                                    xXXX += 10
                        elif event.type == KEYDOWN and event.key == 8:
                            if xXXX >= 930:
                                if len(addRess) >= 1:
                                    charDel = len(addRess) - 1
                                    if char in thinChar:
                                        xXXX -= 7
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX - 921,216,7,22), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                    elif char in fatChar:
                                        xXXX -= 15
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX - 921,216,15,22), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                    else:
                                        xXXX -= 10
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX - 921,216,10,22), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                else:
                                    continue
                            elif xXXX >= 616:
                                if len(addRess) >= 1:
                                    charDel = len(addRess) - 1
                                    if char in thinChar:
                                        xXXX -= 7
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX - 613,186,7,22), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                    elif char in fatChar:
                                        xXXX -= 15
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX - 613,186,15,22), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                    else:
                                        xXXX -= 10
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX - 613,186,10,22), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                else:
                                    continue
                            elif xXXX >= 310:
                                if len(addRess) >= 1:
                                    charDel = len(addRess) - 1
                                    if char in thinChar:
                                        xXXX -= 7
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX - 301,156,7,22), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                    elif char in fatChar:
                                        xXXX -= 15
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX - 301,156,15,22), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                    else:
                                        xXXX -= 10
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX - 301,156,10,22), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                else:
                                    continue
                            elif xXXX >= 93:
                                if len(addRess) >= 1:
                                    charDel = len(addRess) - 1
                                    if char in thinChar:
                                        xXXX -= 7
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX,120,7,25), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                    elif char in fatChar:
                                        xXXX -= 15
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX,120,15,25), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                    else:
                                        xXXX -= 10
                                        pygame.draw.rect(page.intermediate2, (230,230,230), (xXXX,120,10,25), 0)
                                        del addRess[charDel]
                                        if len(addRess) >= 1:
                                            char = addRess[charDel - 1]
                                        else:
                                            continue
                                else:
                                    continue

                    Page().screen.blit(page.intermediate, (0, scroll_y - 63))
                    Page().screen.blit(page.intermediate2, (0, scroll_y))
                    clock.tick(60)
                        
                    pygame.display.update() 

                    if (y < 107 + scroll_y) or (y > 237 + scroll_y):
                        pygame.draw.line(page.intermediate2, (210,210,210), (5,150), (320, 150), 1)
                        pygame.draw.line(page.intermediate2, (210,210,210), (5,180), (320, 180), 1)
                        pygame.draw.line(page.intermediate2, (210,210,210), (5,210), (320, 210), 1)
                        pygame.draw.line(page.intermediate2, (210,210,210), (5,240), (320, 240), 1)
                        break
                    else:
                        continue
                    
            #Mobile Field   
            elif (x >= 5) and (x <= 320) and (y >= 247 + scroll_y) and (y < 295 + scroll_y):
                pygame.draw.line(page.intermediate2, (0,0,0), (5, 300), (320, 300), 1)
                while True:
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP and event.button == 1:
                            x, y = pygame.mouse.get_pos()
                        elif event.type == KEYDOWN and (event.unicode not in invalidChar)  and xXXXX <= 306:
                            char = event.unicode
                            moBile.append(char)
                            contactFont = pygame.font.SysFont("trebuchet ms", 18)
                            textName = contactFont.render(char, True, (0,0,0))
                            page.intermediate2.blit(textName, (xXXXX, 271))
                            if event.unicode in thinChar:
                                xXXXX += 7
                            elif event.unicode in fatChar:
                                xXXXX += 15
                            else:
                                xXXXX += 10
                        elif event.type == KEYDOWN and event.key == 8 and xXXXX >= 81:
                            if len(moBile) >= 1:
                                charDel = len(moBile) - 1
                                if char in thinChar:
                                    xXXXX -= 7
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXXXX,271,7,25), 0)
                                    del moBile[charDel]
                                    if len(moBile) >= 1:
                                        char = moBile[charDel - 1]
                                    else:
                                        continue
                                elif char in fatChar:
                                    xXXXX -= 15
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXXXX,271,15,25), 0)
                                    del moBile[charDel]
                                    if len(moBile) >= 1:
                                        char = moBile[charDel - 1]
                                    else:
                                        continue
                                else:
                                    xXXXX -= 10
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXXXX,271,10,25), 0)
                                    del moBile[charDel]
                                    if len(moBile) >= 1:
                                        char = moBile[charDel - 1]
                                    else:
                                        continue
                            else:
                                continue

                    Page().screen.blit(page.intermediate, (0, scroll_y - 63))
                    Page().screen.blit(page.intermediate2, (0, scroll_y))
                    clock.tick(60)
                        
                    pygame.display.update()

                    if (y < 247 + scroll_y) or (y > 295 + scroll_y):
                        pygame.draw.line(page.intermediate2, (210,210,210), (5, 300), (320, 300), 1)
                        break
                    else:
                        continue

            #Telephone Field   
            elif (x >= 5) and (x <= 320) and (y >= 307 + scroll_y) and (y < 349 + scroll_y):
                pygame.draw.line(page.intermediate2, (0,0,0), (5, 350), (320, 350), 1)
                while True:
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP and event.button == 1:
                            x, y = pygame.mouse.get_pos()
                        elif event.type == KEYDOWN and (event.unicode not in invalidChar)  and xXXXXX <= 306:
                            char = event.unicode
                            telPhone.append(char)
                            contactFont = pygame.font.SysFont("trebuchet ms", 18)
                            textName = contactFont.render(char, True, (0,0,0))
                            page.intermediate2.blit(textName, (xXXXXX, 321))
                            if event.unicode in thinChar:
                                xXXXXX += 7
                            elif event.unicode in fatChar:
                                xXXXXX += 15
                            else:
                                xXXXXX += 10
                        elif event.type == KEYDOWN and event.key == 8 and xXXXXX >= 81:
                            if len(telPhone) >= 1:
                                charDel = len(telPhone) - 1
                                if char in thinChar:
                                    xXXXXX -= 7
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXXXXX,321,7,25), 0)
                                    del telPhone[charDel]
                                    if len(telPhone) >= 1:
                                        char = telPhone[charDel - 1]
                                    else:
                                        continue
                                elif char in fatChar:
                                    xXXXXX -= 15
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXXXXX,321,15,25), 0)
                                    del telPhone[charDel]
                                    if len(telPhone) >= 1:
                                        char = telPhone[charDel - 1]
                                    else:
                                        continue
                                else:
                                    xXXXXX -= 10
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXXXXX,321,10,25), 0)
                                    del telPhone[charDel]
                                    if len(telPhone) >= 1:
                                        char = telPhone[charDel - 1]
                                    else:
                                        continue
                            else:
                                continue

                    Page().screen.blit(page.intermediate, (0, scroll_y - 63))
                    Page().screen.blit(page.intermediate2, (0, scroll_y))
                    clock.tick(60)
                        
                    pygame.display.update()

                    if (y < 307 + scroll_y) or (y > 349 + scroll_y):
                        pygame.draw.line(page.intermediate2, (210,210,210), (5, 350), (320, 350), 1)
                        break
                    else:
                        continue

            #Email Field   
            elif (x >= 5) and (x <= 320) and (y >= 359 + scroll_y) and (y < 399 + scroll_y):
                pygame.draw.line(page.intermediate2, (0,0,0), (5, 400), (320, 400), 1)
                while True:
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP and event.button == 1:
                            x, y = pygame.mouse.get_pos()
                        elif event.type == KEYDOWN and (event.unicode not in invalidChar)  and xXXXXXX <= 306:
                            char = event.unicode
                            eMail.append(char)
                            contactFont = pygame.font.SysFont("trebuchet ms", 18)
                            textName = contactFont.render(char, True, (0,0,0))
                            page.intermediate2.blit(textName, (xXXXXXX, 370))
                            if event.unicode in thinChar:
                                xXXXXXX += 7
                            elif event.unicode in fatChar:
                                xXXXXXX += 15
                            else:
                                xXXXXXX += 10
                        elif event.type == KEYDOWN and event.key == 8 and xXXXXXX >= 76:
                            if len(eMail) >= 1:
                                charDel = len(eMail) - 1
                                if char in thinChar:
                                    xXXXXXX -= 7
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXXXXXX,370,7,25), 0)
                                    del eMail[charDel]
                                    if len(eMail) >= 1:
                                        char = eMail[charDel - 1]
                                    else:
                                        continue
                                elif char in fatChar:
                                    xXXXXXX -= 15
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXXXXXX,370,15,25), 0)
                                    del eMail[charDel]
                                    if len(eMail) >= 1:
                                        char = eMail[charDel - 1]
                                    else:
                                        continue
                                else:
                                    xXXXXXX -= 10
                                    pygame.draw.rect(page.intermediate2, (230,230,230), (xXXXXXX,370,10,25), 0)
                                    del eMail[charDel]
                                    if len(eMail) >= 1:
                                        char = eMail[charDel - 1]
                                    else:
                                        continue
                            else:
                                continue

                    Page().screen.blit(page.intermediate, (0, scroll_y - 63))
                    Page().screen.blit(page.intermediate2, (0, scroll_y))
                    clock.tick(60)
                        
                    pygame.display.update()

                    if (y < 359 + scroll_y) or (y > 399 + scroll_y):
                        pygame.draw.line(page.intermediate2, (210,210,210), (5, 400), (320, 400), 1)
                        break
                    else:
                        continue

        #Event code for Edit Contact Page
        elif event.type == MOUSEBUTTONUP and event.button == 1 and isinstance(page, EditPage):
            x, y = pygame.mouse.get_pos()
            
            #Checks if user has clicked the Cancel button
            if (x >= 270) and (x <= 310) and (y >= scroll_y - 50) and (y <= scroll_y - 10):
                buttonSound.play()
                sleep(0.5)
                scroll_y = 63
                control2 = 0
                page = MainPage()
                page.style()
                page.printContacts()
            #Checks to see if user has clicked the delete button
            elif (x >= 5) and (x <= 310) and (y >= 407 + scroll_y) and (y <= 447 + scroll_y):
                buttonSound.play()
                contact = AddressBook().delContact() #calls on delContact method from AddressBook class
                sleep(0.5)
                scroll_y = 63
                control2 = 0
                page = MainPage()
                page.style()
                page.printContacts()
                

    #adjusts the blitting of objects on screen, appropriate to how much
    #the user has scrolled
    Page().screen.blit(page.intermediate, (0, scroll_y - 63))
    Page().screen.blit(page.intermediate2, (0, scroll_y))
    clock.tick(60) #Runs app at 60 frames a second
                        
    pygame.display.update() #Updates app based on captured event
              


