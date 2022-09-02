import random

triads = ['000',
          '001',
          '010',
          '011',
          '100',
          '101',
          '110',
          '111']


def new_numbers():
    numbers = input('Print a random string containing 0 or 1:\n\n')
    return numbers


def filter_inappropiate(random_string):
    for character in random_string:
        if character not in ('0', '1'):
            random_string = random_string.replace(character, '')
    return random_string


def groups_string(random_string, size_group=4):
    groups = []
    size = len(random_string)
    for i in range(size_group, size + 1):
        groups.append(random_string[i - size_group:i])
    return groups


def count_triad(triad, groups):
    count0 = 0
    count1 = 0
    for group in groups:
        if triad + '0' == group:
            count0 += 1
        if triad + '1' == group:
            count1 += 1
    return [count0, count1]


def create_dict_count(total_triads, groups):
    return {triad: count_triad(triad, groups) for triad in total_triads}


def start_prediction():
    first = random.sample(('0', '1'), 1)
    second = random.sample(('0', '1'), 1)
    third = random.sample(('0', '1'), 1)
    combine_random = [first[0], second[0], third[0]]
    return combine_random


def predict_next(random_triad, dict_statistics):
    stat_triad = dict_statistics[random_triad]
    if stat_triad[0] > stat_triad[1]:
        return '0'
    elif stat_triad[0] < stat_triad[1]:
        return '1'
    else:
        return random.sample(('0', '1'), 1)[0]


def predict_string(random_string, dict_statistics):
    test_groups = groups_string(random_string, size_group=3)[:-1]
    predictions = start_prediction()
    for group in test_groups:
        predictions.append(predict_next(group, dict_statistics))
    return ''.join(predictions)


def performance(random_string, prediction):
    count = 0
    for i in range(3, len(random_string)):
        if random_string[i] == prediction[i]:
            count += 1
    percent = round(100 * count / (len(random_string) - 3), 2)
    print(f'Computer guessed right {count} out of {len(random_string) - 3} symbols ({percent} %)')
    return {'total': len(random_string) - 3, 'correct': count}


def update_balance(balance, dict_performance):
    new_balance = balance - dict_performance['correct'] + (dict_performance['total'] - dict_performance['correct'])
    print(f'Your balance is now ${new_balance}\n')
    return new_balance


def game(test_string, balance, dict_statistics):
    my_prediction = predict_string(test_string, dict_statistics)
    print(test_string)
    print('prediction:')
    print(my_prediction)
    print()
    perf = performance(test_string, my_prediction)
    return update_balance(balance, perf)


def random_behaviour():
    print('Please give AI some data to learn...')
    print('The current data length is 0, 100 symbols left')
    random_string = filter_inappropiate(new_numbers())
    while len(random_string) < 100:
        print('Current data length is {}, {} symbols left'.format(len(random_string), 100 - len(random_string)))
        random_string += filter_inappropiate(new_numbers())
    print('\nFinal data string:')
    print(random_string)
    print()
    groups = groups_string(random_string)
    dict_stat = create_dict_count(triads, groups)
    print('You have $1000. Every time the system successfully predicts your next press, you lose $1.')
    print('Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!\n')
    balance = 1_000
    while True:
        print('Print a random string containing 0 or 1:')
        test_string = input()  # filtar inaporpiados
        if test_string == 'enough':
            break
        elif len(set(test_string)) > 2:
            continue
        else:
            my_prediction = predict_string(test_string, dict_stat)
            print('prediction:', my_prediction, sep='\n')
            dict_perf = performance(test_string, my_prediction)
            balance = update_balance(balance, dict_perf)
    print('Game over!')


random_behaviour()
