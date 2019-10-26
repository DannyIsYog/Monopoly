import random
import os

#Name, Action
Community_Cards = [
    ('Name', 'Action')
]

#Name, Action
Chance_Cards = [
    ('Name', 'Action')
]

# Propriedadas -> (Name, Group, Price, (house price, 0 houses, 1 house, 2 houses, 3 houses, 4 houses, hotel, mortage))
# -1: Comunidade ; -2: Sorte ; -3: Impostos ; -4: Cadeia ; -5: Vai para a prisão
# -6: Estacionamento ; -7: Partida
Propertys = [
    ('Partida', 'Partida', -7, 2000),
    ('Campo Grande (Lisboa)','Castanho', 60, (50, 2, 10, 30, 90, 160, 250)),
    ('Caixa da Comunidade','Comunidade', -1, Community_Cards),
    ('Rua Faria Guimarães (Porto)', 'Castanho', 60, (50, 4, 20, 60, 180, 320, 450)),
    ('Pague Imposto sobre Capitais', 'Impostos', -3, 200),
    ('Estação do Rossio (Lisboa)', 'Estações', 200),
    ('Alameda das Linhas de Torres (Lisboa)', 'Azul Claro', 100, (50, 6, 30, 90, 270, 400, 550)),
    ('Sorte', 'Sorte', -2, Chance_Cards),
    ('Avenida das Nações Unidas (Lisboa)', 'Azul Claro', 100, (50, 6, 30, 90, 270, 400, 550)),
    ('Avenida 24 de Julho (Lisboa)', 'Azul Claro', 120, (50, 8, 40, 100, 300, 450, 600)),
    ('Cadeia', 'Cadeia', -4),
    ('Avenida Central (Braga)', 'Rosa', 140,(100, 10, 50, 150, 450, 625, 750)),
    ('Companhia de Electricidade', 'Companhias', 150),
    ('Rua Ferreira Borges (Coimbra)', 'Rosa', 140, (100, 10, 50, 150, 450, 625, 750)),
    ('Avenida de Roma (Lisboa)', 'Rosa', 160, (100, 12, 60, 180, 500, 700, 900)),
    ('Gare do Oriente (Lisboa)', 'Estações', 200),
    ('Avenida da Boavista (Porto)','Laranja', 180, (100, 14, 70, 200, 550, 750, 950)),
    ('Caixa da Comunidade', 'Comunidade', -1, Community_Cards),
    ('Avenida da República (Lisboa)', 'Laranja', 180, (100, 14, 70, 200, 550, 750, 950)),
    ('Rua Mouzinho da Silveira (Porto)', 'Laranja', 200, (100, 16, 80, 220, 600, 800, 1000)),
    ('Estacionamento Livre', 'Estacionamento', -6),
    ('Rua de Santa Catarina (Porto)', 'Vermelho', 220, (150, 18, 90, 250, 700, 875, 1050)),
    ('Sorte', 'Sorte', -2, Chance_Cards),
    ('Avenida Infante Santo (Lisboa)', 'Vermelho', 220, (150, 18, 90, 250, 700, 875, 1050)),
    ('Rua Júlio Diniz (Porto)', 'Vermelho', 240, (150, 20, 100, 300, 750, 925, 1100)),
    ('Estação de S. Bento (Porto)', 'Estações', 200),
    ('Praça da República (Porto)', 'Amarelo', 260, (150, 22, 110, 330, 800, 975, 1150)),
    ('Avenida Fontes Pereira de Melo (Lisboa)', 'Amarelo', 260, (150, 22, 110, 330, 800, 975, 1150)),
    ('Companhia das Águas', 'Companhias', 150),
    ('Rotunda da Boavista (Porto)', 'Amarelo', 280, (150, 24, 120, 360, 850, 1025, 1200)),
    ('Vá para a cadeia ', 'Cadeia', -5, 'Prender'),
    ('Avenida da Liberdade (Lisboa)', 'Verde', 300, (200, 26, 130, 390, 900, 1100, 1275)),
    ('Rua dos Clérigos (Porto)', 'Verde', 300, (200, 26, 130, 390, 900, 1100, 1275)),
    ('Caixa da Comunidade', 'Comunidade', -1, Community_Cards),
    ('Avenida do Parque das Nações (Lisboa)', 'Verde', 320, (200, 28, 150, 450, 1000, 1200, 1400)),
    ('Estação de Sta Apolónia (Lisboa)', 'Estações', 200),
    ('Sorte','Sorte', -2, Chance_Cards),
    ('Rua das Amoreiras (Lisboa)','Azul Escuro', 350, (200, 35, 175, 500, 1100, 1300, 1500)),
    ('Imposto de Luxo','Impostos', -3, 200),
    ('Rossio (Lisboa)', 'Azul Escuro', 400, (200, 50, 200, 600, 1400, 1700, 2000))
]

#Which propreties can be bought
Buyable_groups = [
    'Castanho',
    'Azul Claro',
    'Rosa',
    'Laranja',
    'Vermelho',
    'Amarelo',
    'Verde',
    'Azul Escuroa',
    'Estações',
    'Companhias'
]


#FUTURE: Will be able to customize the rules
Game_settings = []

#Class of the game, needs a room and an admin to create a game.
class Monopoly:
    def __init__(self,room,admin):
        self.room = room                #Usefull for discord
        self.admin = admin              #Usefull for discord
        self.players = [Player(admin),] #List of all players
        self.num_players = 1            #number of total players
        self.running = False            #True if the game as started
        self.current_player = None      #Player that is currently playing
        self.dice1 = None
        self.dice2 = None
        self.dice_sum = None
        self.board = Board(Propertys)   #Creates the board
        self.next_plays = ['None']      #Next allowed plays
        self.property_in_auction = None #The property that is being auctioned
        self.bidders = None             #List of players bidding

    ###################################
    #Group of functions to print stuff#
    ###################################

    #Prints a list of all the player in the game and says who is currently playing
    def see_players(self):
        for player in self.players:
            if player.playing:
                print('Playing')
            print(player.name + ' Dice:' + str(player.dice_sum) + ' ')

    #Prints the room of the game
    def see_propreties(self):
        print('Room: ' + str(self.room))

    #Prints the last dice's values of a player and its sum
    def see_dice(self, w_player):
        for player in self.players:
            if player.name == w_player:
                    print(player.dice1)
                    print(player.dice2)
                    print(player.dice_sum)

    ###########################
    #Group of search functions#
    ###########################

    #Returs a player object that matches a given name
    def get_player(self, w_player):
        for player in self.players:
            if player.name == w_player:
                return player
        return None

    #Returns the index of a player in the self.players list
    def get_iplayer(self, player):
        i = 0
        for aplayer in self.players:
            if aplayer.name == player.name:
                return i
            i += 1
        return None

    #Returns the player that is playing right now if the game as already started
    def get_playing_player(self):
        return self.current_player

    #Returns a property object that matches a name given
    def get_property(self, w_property): #w_property -> wanted property
        for property in self.board.path:
            if property.name == w_property:
                print(property.group)

    def get_iproperty(self, property):
        i = 0
        for aproperty in self.board.path:
            if aproperty.name == property.name:
                return i
        return None

    ################################################
    #Group of functions for the setting up the game#
    ################################################

    #Adds a player to the gane
    def join(self, player):
        self.players.append(Player(player))
        self.num_players += 1

    #Removes a player from the game
    def leave(self, player):
        self.players.remove(player)
        self.num_players -= 1

    #Sets up the game to start
    def start(self):
        self.running = 1
        self.decide_order()
        self.board = Board(Propertys)
        for player in self.players:
            player.place = self.board.path[0]
        self.players[0].playing = True
        self.players[0].rolled = False
        self.next_plays = ['Roll']

    #Decides in which order the players will play
    def decide_order(self):
        high = 0
        re_rolled = True
        for player in self.players:
            self.roll_for(player)
        while re_rolled:
            re_rolled = False
            for player in self.players:
                for player2 in self.players:
                    if player.name != player2.name and player.dice_sum == player2.dice_sum:
                        self.roll_for(player)
                        self.roll_for(player2)
                        re_rolled = True
        self.players.sort(key=lambda player: player.dice_sum,reverse = True)

    ###########################################
    #Group of functions that controls the dice#
    ###########################################

    #Rolls the dices for a player
    def roll_for(self, player):
        self.roll_dices()
        player.dice1 = self.dice1
        player.dice2 = self.dice2
        player.dice_sum = self.dice_sum
        if player.dice1 == player.dice2:
            player.doubles += 1
            player.was_doubles = True
        else:
            player.was_doubles = False

    #Rolls the dices
    def roll_dices(self):
        self.dice1 = dice()
        self.dice2 = dice()
        self.dice_sum = self.dice1 + self.dice2

    ###########################################
    #Group of functions that controls the game#
    ###########################################

    #Moves a player on the board upon rolling dices
    def move(self, player):
        new_index = self.get_iproperty(player.place) + player.dice_sum
        player.place = self.board.path[new_index]
        #self.check(player)

    #Makes all the necessary checks before the player performs a roll
    def before_roll_check(self, player):
        if player.prison:
            if self.prison_time == 3:
                player.prison = False
                player.prison_time = 0
            else:
                self.next_plays = ['Pass', 'Roll_Prison', 'Pay_Prison']

    #Makes all the necessary checks after the player performs a roll
    def after_roll_check(self, player):
        if player.place.owner == 'Bank' and player.place.group in Buyable_groups:
            self.next_plays = ['Buy']

    #Places a property for auction
    def place_for_auction(self, player):
        self.property_in_auction = [player.place, 0, 'Bank'] # (property, highest bid, bidder)
        self.bidders = [bidder for bidder in self.players]

    #Ends an auction
    def end_auction(self):
        if self.property_in_auction[2] != 'Bank':
            self.property_in_auction[0].owner = self.property_in_auction[2]         #Changes the owner of the property
            self.property_in_auction[2].money -= self.property_in_auction[1]        #Makes the bank transaction
            self.property_in_auction[2].props.append(self.property_in_auction[0])   #Add the property to the player owned proerties
        self.property_in_auction = None                                             #Resets state of the game
        self.next_plays = ['Pass']                                                  #Next possible actions

    ############################
    #Property related functions#
    ############################
    #Buys the proprety for a player
    def buy(self, player):
        if 'Buy' in self.next_plays and player.place.group in Buyable_groups and player.playing == True and \
        (player.rolled == True or player.was_doubles == True) and player.place.owner == 'Bank':
            player.place.owner = player.name
            player.money -= player.place.value
            player.props.append(player.place)
            self.next_plays.remove('Buy')

    #Places a bid for the current auction
    def bid(self, player, amount):
        if self.property_in_auction != None:
            if amount > self.property_in_auction[1]:
                self.property_in_auction[1] = amount
                self.property_in_auction[2] = player
                print('Bid of ' + str(amount) + '$ placed on' + self.property_in_auction[0].name + ' by ' + player.name)
            else:
                print('You need to bid a higher value then ' + str(self.property_in_auction[1]) + '$')

    #Takes out a player of the current auction
    def pass_bid(self, player):
        if 'Pass_bid' in self.next_plays and player in self.bidders and self.property_in_auction[2].name != player.name :
            self.bidders.pop(self.get_iplayer(player))
            if len(self.bidders) == 1:
                self.end_auction()

    ##########################################
    #Actual game player interaction functions#
    ##########################################

    #Rolls the dice for a player and handles what are the next moves
    def roll(self, player):
        if 'Roll' in self.next_plays and self.running == True and player.playing == True and player.rolled == False:
            self.roll_for(player)
            self.next_plays = ['Roll']
            if player.was_doubles != True:
                player.rolled = True
                self.next_plays = ['Pass', 'Buy']
            self.move(player)

    #Rolls the dice for someone in prison and checks if they get out or not based on the out come
    def roll_prison(self, player):
        if 'Roll_Prison' in self.next_plays and player.playing and player.rolled == False:
            self.roll_for(player)
            if player.was_doubles:
                player.prison = False
            else:
                player.prison_time += 1
            self.next_plays = ['Pass']

    #A player pay to leave jail next turn
    def prison_pay(self, player):
        if 'Pay_Prison' in self.next_plays:
            player.money -= 50
            player.prison = False
            player.prison_time = 0

    #Passes a players turn
    def Pass(self, player):
        if 'Pass' in self.next_plays and self.running == True and player.playing == True and player.rolled == True and \
        player.place.owner == 'Bank' and player.place.group in Buyable_groups and self.property_in_auction == None:
            self.place_for_auction(player)
            self.next_plays = ['Bid','Pass_bid']
        elif 'Pass' in self.next_plays and self.running == True and player.playing == True and player.rolled == True:
            player.playing = False
            player.was_doubles = False
            i = self.get_iplayer(player) + 1
            if i == len(self.players):
                i = 0
            self.players[i].playing = True
            self.players[i].rolled = False
            self.current_player = self.players[i]
            self.next_plays = ['Roll']

class Player:
    def __init__(self,name):
        self.name = name
        self.money = 1500
        self.networth = self.money #Needs to add money + propreies + houses + hotels
        self.props = []            #List of all the properties a player owns
        self.dice1 = None
        self.dice2 = None
        self.dice_sum = None
        self.was_doubles = False
        self.doubles = 0     #counts the number of doubles
        self.playing = False #True if is this player playing
        self.rolled = True   #True if the player has already rolled dices
        self.place = None    #Current proprety of where the player is
        self.prison = False  #True if the player is in prison
        self.prison_time = 0 #Number of turn the player as passed in prison

class Board:

    #creates a board with a set of proreties
    def __init__(self, chosen):
        self.path = []   #List that represents the board internally
        self.groups = {} #Dictionary that has the propretys sorted by color

        #Sets up the board by appending the propretys to the list and dictionary above
        for prop in chosen:

            #Sets self.path list
            if prop[2] > 0:
                if prop[1] == 'Estações':
                    self.path.append(Train_proprety(prop[0],prop[1],prop[2]))
                elif prop[1] == 'Impostos':
                    self.path.append(Tax_property(prop[0],prop[1],prop[2]))
                else:
                    self.path.append(Property(prop[0],prop[1],prop[2]))
            elif prop[2] in (-1, -2):
                self.path.append(CC_cards(prop[0], prop[1], prop[3]))
            elif prop[2] in (-4,-6):
                self.path.append(Free_Property(prop[0],prop[1],prop[2]))
            elif prop[2] == -3:
                self.path.append(Tax_property(prop[0], prop[1], prop[3]))
            elif prop[2] == -5:
                self.path.append(Action_Card(prop[0], prop[3]))
            else:
                self.path.append(Go(prop[3]))

            #Sets self.groups dictionary
            if prop[1] in self.groups:
                self.groups[self.path[-1].group] += [self.path[-1]]
            else:
                self.groups[self.path[-1].group] = [self.path[-1]]

######################
#All Property Objects#
######################

class Property: #Normal property
    def __init__(self, name, group, value):
        self.name = name
        self.group = group
        self.value = value
        self.owner = 'Bank'

class Free_Property: #Property w/o any actions like jail
    def __init__(self, name, group, value):
        self.name = name
        self.group = group
        self.value = value
        self.owner = 'Bank'

class Tax_property: #Proprety that taxes players
    def __init__(self, name, group, amount):
        self.name = name
        self.group = group
        self.amount = amount
        self.owner = 'Bank'

class Train_proprety: #Proprety of stations
    def __init__(self, name, group, value):
        self.name = name
        self.group = group
        self.value = value
        self.owner = 'Bank'

class Utility_property:
    def __init__(self, name, group, value):
        self.name = name
        self.group = group
        self.value = value
        self.owner = 'Bank'

class Go: #Go, when a player passes by this gains an amount of money
    def __init__(self, amount):
        self.name = 'Go'
        self.amount = amount
        self.owner = 'Bank'
        self.group = 'Go'

#########################
#Cards and Decks objects#
#########################

#NOT DONE

#Chance or Community cards
class CC_cards:
    def __init__(self, name, group, deck):
        self.name = name
        self.group = group
        self.deck = Deck(deck)
        self.owner = 'Bank'

#deck class, stores all the cards
class Deck:
    def __init__(self, cards):
        self.cards = []
        #sets up a deck
        for card in cards:
            # Name, Action
            self.cards.append(Action_Card(card[0], card[1]))

class Action_Card:
    def __init__(self, name, action):
        self.name = name
        self.action = action
        self.group = 'Laranja'

#Rolls a dice and returns its value
def dice():
    return(random.randint(1,6))

#Draws the board of a game
def draw_board(game):
    new_l = 1
    for i in game.board.path:
        print(i.name + ' ', end='') #prints the name of the property
        #Needs otimization
        for j in game.players: #prints all the name in this prorety
            if j.place != None:
                if j.place.name == i.name:
                    print(' ' + j.name)
                    new_l = 0
        if new_l == 1:
            print()
        new_l = 1

#Displays all the owned propertys of a player
def dis_props(player):
    for prop in player.props:
        print(prop.name)


#This is only for debbuging, need to create a better interface later
while True:
    command = input()
    if command == 'n': #Create new Game
        game_1 = Monopoly(input('Room: '),input('Admin name: '));
    elif command == 'a': #add player
        game_1.join(input('Player name: '))
    elif command == 'r': #Remove Players
        game_1.leave(game_1.get_player(input('Player name: ')))
    elif command == 'l': #list all players
        game_1.see_players()
    elif command == 's': #start game
        game_1.start()
    elif command == 'd': #draws the board
        draw_board(game_1)
    elif command == 'p': # shows what you can do
        print(game_1.next_plays)
    elif command == 'roll': # rolls the dice for a player
        game_1.roll(game_1.get_player(input('Player name: ')))
    elif command == 'pass': # passes the turn
        game_1.Pass(game_1.get_player(input('Player name: ')))
    elif command == 'buy': #buys a property
        game_1.buy(game_1.get_player(input('Player name: ')))
    elif command == 'prop': #prints all the property of a player
        dis_props(game_1.get_player(input('Player name:')))
    elif command == 'bid':
        game_1.bid(game_1.get_player(input('Player name:')),int(input('Bid Ammount:')))
    elif command == 'pbid':
        game_1.pass_bid(game_1.get_player(input('Player name:')))
    elif command == 'x': #exits the program
        break;
