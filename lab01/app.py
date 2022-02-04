
from flask import Flask, render_template
from random import choice, randint
app = Flask(__name__)

@app.route('/rps/<player>')
def rps(player:str):

    '''
    Logic to Solve:
    There is a cyclical relationship, therefore if the computer choice immediately follows the player choice in the cycle, the computer wins.
    Hence, the player wins if the computer choice immediately precedes the user choice.

    To show this relationship the modulo operator can be used like so:

    (options.index(player) + 1) % # == options.index(computer) % #

    Replace the '#' with the number of options in the cycle.

    Note: for this solution to work, the options must entered to the list in the correct cyclical order.
    '''
    options = ['rock', 'paper', 'scissors']
    computer = choice(options)

    comp_win = 'Computer wins!'
    player_win = 'Player wins!'
    draw = "It's a draw"

    adjective_list = ['blunts','wraps','cuts']

    result = ''

    if player == computer:
        result = draw
        winner = 'x'
    
    elif (options.index(player) + 1) % 3 == options.index(computer) % 3:
        result = comp_win
        winner = 'C'

    else: 
        result = player_win
        winner = 'P'

    if winner == 'P':
        adjective = adjective_list[options.index(player)]
    elif winner == 'C':
        adjective = adjective_list[options.index(computer)]
    else:
        adjective = 'boring'

    return render_template('rps.html', result=result, computer=computer, player=player, adjective=adjective, winner=winner)



@app.route('/could_it_be_me/<int:num_lines>')
def send_lotto_numbers(num_lines):
    list_of_lines = []

    for i in range(num_lines):
        line = []
        for i in range(0,6):
            n = randint(1,47)
            while True:
                if n in line:
                    n = randint(1,47)
                else:
                    break
            line.append(n)

    
        list_of_lines.append(line)

    return render_template('lotto.html', line=line, list_of_lines=list_of_lines)


@app.route('/could_it_me2/<int:num_lines>')
def send_lotto_numbers2(num_lines):
    list_of_lines = []

    for i in range(num_lines):
        line = []
        for i in range(0,6):
            n = randint(1,47)
            line.append(n)

    
        list_of_lines.append(line)

    return render_template('lotto.html', line=line, list_of_lines=list_of_lines)

@app.route('/rps15/<player>')
def rps15(player:str):
    player = player.lower()
    options = (
                'rock','fire', 'scissors','snake','human','tree','wolf','sponge',
                'paper','air','water','dragon','devil','lightning','gun'
            )

    computer = choice(options)

    comp_win = 'Computer wins!'
    player_win = 'Player wins!'
    draw = "It's a draw"

    result = ''

    player_beats = []

    beatIndex = options.index(player)
    i = 1

    endLoop = (len(options)-1)//2
    for i in range(1, endLoop+1):
        if beatIndex == len(options)-1:
            beatIndex = 0
        player_beats.append(options[beatIndex + i])
        i +=1
    
    if computer == player:
        result = draw


    elif computer in player_beats:
        result = player_win

    else:
        result = comp_win
    
    
    return render_template('rps15.html', result=result, computer=computer, player=player)