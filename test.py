from random import randint


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

    return list_of_lines

print(send_lotto_numbers(4))