from fool_bot.entities import *

you = 'You'
take = 'take'
finish = 'finish'
greeting = '''
Hello! I can lead the Russian card game "Fool".
Create new game with command /create <key>
Or join existing game with command /join <key>
Send /help to see more info
'''
help = f'''
I\'m a bot who can lead the Russian card game "Fool"
Commands:
/help - see this message
/create <key> - create new game with key <key>
/join <key> - join existing game with key <key>
/start_game - start game. Allowed only for game creator
Game process:
Wait for your move and chose a card to use
If you're attacking, you can type {finish} to end your move
If you're defending, you can type {take} to take cards
Good game!
'''
not_your_move = 'Wait, it\'s not your move'
have_not_card = 'You have not this card'
cant_use_card = 'You can\'t use this card'
key_exist = 'Key is already exist'
already_in_game = 'You\'re already in game'
no_such_key = 'Key is not found'
in_another_game = 'You\'re already in another game'
not_known_action = 'I don\'t understand, repeat please'
not_in_game = 'You\'re not in any game'
cant_start_not_creator = 'You can\'t start game since you\'re not a creator'
cant_start_wrong_players_number = 'You can\'t start game since number of players should be between 2 and 6'
empty_key = 'Please enter the key'
game_started = 'Game started!'

def attacked(who, card):
    return str(who) + ' attacked with card ' + str(card)

def defended(who, card):
    return str(who) + ' defended with card ' + str(card)

def took(who):
    return str(who) + ' took the cards'

def on_table(table):
    s = 'On table:\n'
    for card in table[0::2]:
        s += str(card) + ' '
    s += '\n'
    for card in table[1::2]:
        s += str(card) + ' '
    return s

def your_cards(cards):
    s = 'Your cards:\n'
    for card in cards:
        s += str(card) + ' '
    s = s[:-1]
    return s

def your_move(cards, table):
    s = 'It\'s your move now.\n'
    s += your_cards(cards)
    if len(table) > 0:
        s += '\n' + on_table(table)
    return s


def move_of(who, cards, table):
    s = 'Move of ' + str(who)
    s += '\n' + your_cards(cards)
    if len(table) > 0:
        s += '\n' + on_table(table)
    return s

def game_created(key):
    return 'Created game with key ' + str(key)

def joined_game_player(who):
    return str(who) + ' has joined game'

def joined_game_key(key):
    return 'You\'ve joined game with key ' + str(key)

def game_info(game):
    s = 'Trump : ' + Card.symbols[game.trump] + '\n'
    s += str(len(game.deck)) + ' card'
    if (len(game.deck)) != 1:
        s += 's'
    s += ' in deck'
    return s
