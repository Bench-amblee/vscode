'''
You're launched high into the atmosphere! The apex of your trajectory just barely reaches the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow. He'll be happy to explain the situation, but it's a bit of a walk, so you have some time. They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
'''

bag = {'Red': 12, 'Green': 13, "Blue": 14}

G1 = 'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green'
G2 = 'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue'
G3 = 'Game 3: 8 green, 6 blue, 20 red; 5 blue, 13 green; 5 green'
G4 = 'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red'
G5 = 'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'


def data_clean(text):
    data_dict = {}
    results_dict = {}
    round_list = []

    # seperate Game header from item data
    clean1 = text.strip().split(":")

    # seperate games into list of games
    clean2 = clean1[1].strip().split("; ")

    # turn item list data into dictionary to match bag format
    for i in range(len(clean2)):
        round = clean2[i].split(', ')

        for colors in round:
            quantity, color = colors.split(' ')
            quantity = int(quantity)  
            results_dict[color] = quantity

        round_list.append(results_dict)
        
    data_dict[clean1[0]] = round_list
    return data_dict

def valid_bag_game(game):
    game_clean = data_clean(game)
    game_name = list(game_clean.keys())[0]
    round_count = len(list(game_clean.values())[0])

    global red_count
    global green_count
    global blue_count

    red_count = 0
    green_count = 0
    blue_count = 0

    for i in range(round_count):

        red_round = game_clean[game_name][i-1]['red']
        if red_round > red_count:
            red_count = red_round

        green_round = game_clean[game_name][i-1]['green']
        if green_round > green_count:
            green_count = green_round

        blue_round = game_clean[game_name][i-1]['blue']
        if blue_round > blue_count:
            blue_count = blue_round

    if red_count > bag['Red']:
        text = game_name + ' is NOT a valid game'

    elif green_count > bag['Green']:
        text = game_name + ' is NOT a valid game'

    elif blue_count > bag['Blue']:
        text = game_name + ' is NOT a valid game'

    elif (red_count+green_count+blue_count) > (bag['Red']+bag['Green']+bag['Blue']):
        text = game_name + ' is NOT a valid game'

    else:
        text = game_name + ' is a valid game!'


    return text

list_of_games = [G1,G2,G3,G4,G5]

for game in list_of_games:
    print(valid_bag_game(game))
