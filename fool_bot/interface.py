from fool_bot import replics
from fool_bot.game import *

import argparse
import requests


url = None
game_keys = dict()
user_games = dict()
user_names = dict()

def authorize():
    parser = argparse.ArgumentParser(description='fool tg bot')
    parser.add_argument('tocken', type=str, help='bot tocken')
    args = parser.parse_args()
    global url
    url = f'https://api.telegram.org/bot{args.tocken}/'

def make_request(name, params=None):
    response = requests.get(url + name, params=params)
    if response.status_code != 200:
        print('Something wrong with request, status code:', response.status_code)
        return None
    data = response.json()
    if not data['ok']:
        print('Something wrong with tg request')
        return None
    return data['result']

def update_name(user):
    user_names[user['id']] = user['first_name']

def greeting(uid):
    make_request('sendMessage', {'chat_id': uid, 'text': replics.greeting})

def make_replic(uid, result):
    who = user_names[result.who]
    card = result.card
    if result.who == uid:
        who = replics.you

    text = None
    if result.attacked:
        text = replics.attacked(who, card)
    elif result.defended:
        text = replics.defended(who, card)
    elif result.took:
        text = replics.took(who)
    elif result.finish:
        text = replics.finish
    else:
        text = 'Error (1)'
    return text

def send_info(player, result, game):
    uid = player.user_id
    if result != None:
        if result.replic:
            make_request('sendMessage', {'chat_id': uid, 'text': result.replic})
        else:
            make_request('sendMessage', {'chat_id': uid, 'text': make_replic(uid, result)})

    text = None
    next_player = game.next_player()
    if next_player == uid:
        text = replics.your_move(player.cards, game.table)
    else:
        text = replics.move_of(user_names[next_player], player.cards, game.table)

    make_request('sendMessage', {'chat_id': uid, 'text': text})

def handle_move(uid, text):
    game = game_keys[user_games[uid]]
    result = game.move(uid, text)
    if result.error:
        for player in game.players:
            if player.user_id == uid:
                send_info(player, result, game)
    else:
        for player in game.players:
            send_info(player, result, game)

def create_game(uid, text):
    key = text[len('/create'):].strip()
    if key == '':
        make_request('sendMessage', {'chat_id': uid, 'text': replics.empty_key})
    elif uid in user_games:
        make_request('sendMessage', {'chat_id': uid, 'text': replics.already_in_game})
    elif key in game_keys:
        make_request('sendMessage', {'chat_id': uid, 'text': replics.key_exist})
    else:
        game_keys[key] = Game(key, uid)
        user_games[uid] = key
        game_keys[key].add_player(uid)
        make_request('sendMessage', {'chat_id': uid, 'text': replics.game_created(key)})

def join_game(uid, text):
    key = text[len('/join'):].strip()
    if key == '':
        make_request('sendMessage', {'chat_id': uid, 'text': replics.empty_key})
    elif uid in user_games:
        make_request('sendMessage', {'chat_id': uid, 'text': replics.already_in_game})
    elif key in game_keys:
        game = game_keys[key]
        if uid in map(lambda player: player.user_id, game.players):
            make_request('sendMessage', {'chat_id': uid, 'text': replics.already_in_game})
        else:
            user_games[uid] = key
            for player in game.players:
                make_request('sendMessage', {'chat_id': player.user_id, 'text': replics.joined_game_player(user_names[uid])})

            game.add_player(uid)
            make_request('sendMessage', {'chat_id': uid, 'text': replics.joined_game_key(key)})
    else:
        make_request('sendMessage', {'chat_id': uid, 'text': replics.no_such_key})

def give_help(uid):
    make_request('sendMessage', {'chat_id': uid, 'text': replics.help})

def send_game_info(game):
    for player in game.players:
        make_request('sendMessage', {'chat_id': player.user_id,
            'text': replics.game_started + '\n' + replics.game_info(game)})
        send_info(player, None, game)

def start_game(uid):
    if not (uid in user_games):
        make_request('sendMessage', {'chat_id': uid, 'text': replics.not_in_game})
    else:
        game = game_keys[user_games[uid]]
        if game.creator != uid:
            make_request('sendMessage', {'chat_id': uid, 'text': replics.cant_start_not_creator})
        elif len(game.players) < 2 or len(game.players) > 6:
            make_request('sendMessage', {'chat_id': uid, 'text': replics.cant_start_wrong_players_number})
        else:
            game.initialise()
            game.started = True
            send_game_info(game)


def handle_another_action(uid, text):
    make_request('sendMessage', {'chat_id': uid, 'text': replics.not_known_action})

def handle_message(message):
    uid = message['from']['id']
    if not ('text' in message):
        return
    text = message['text']

    update_name(message['from'])

    if text.startswith('/start_game'):
        start_game(uid)
    elif text.startswith('/start'):
        greeting(uid)
    elif text.startswith('/create'):
        create_game(uid, text)
    elif text.startswith('/join'):
        join_game(uid, text)
    elif text.startswith('/help'):
        give_help(uid)
    elif uid in user_games and game_keys[user_games[uid]].started:
        handle_move(uid, text)
    else:
        handle_another_action(uid, text)

offset = 0
def handle_updates():
    global offset
    updates = make_request('getUpdates', {'offset': offset})
    for update in updates:
        offset = max(offset, update['update_id'] + 1)
        if not ('message' in update):
            continue
        handle_message(update['message'])
