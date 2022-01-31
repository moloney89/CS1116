from random import choice
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
    for i in range(1, endLoop):
        if beatIndex == len(options)-1:
            beatIndex = 1
        player_beats.append(options[beatIndex + i])
        i +=1
    
    if computer == player:
        result = draw


    elif computer in player_beats:
        result = comp_win

    else:
        result = player_win
        
    
    
    
    print('Player Choice:   ', player)
    print('Computer Choice: ', computer)
    print('Result:          ', result)

playerChoice = 'rock'
rps15(playerChoice)