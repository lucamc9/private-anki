from utils import *
import random

# Prep
print ('\n#####################\n')
print ('Welcome to the jungle\n')
print ('#####################\n')
print('Choose your battle mode:\n')
print('1) Advanced Vision\n')
print('2) PMR\n')
print('3) Fuck it, imma play fifa\n')
selection = input()

if selection == '1':
    course = 'av'
elif selection == '2':
    course = 'pmr'

if selection not in ['1']:
    print('\nJokes on you!\n')
print('\nAight {} it is then\n'.format(course))

# Load database and compute probabilities
db = load_db(course)
db, num_questions, topic = get_preferred_topic_or_none(db)
stats_exists = True
try:
    stats = load_stats(course)
    # last_wrong = ast.literal_eval(stats['Wrong'].iloc[-1])
    # last_right = [v for v in list(range(num_questions)) if v not in last_wrong]
    # p = 0.5
    display_stats(stats)
except:
    stats_exists = False

# Inits
correct_qs = []
wrong_qs = []
num_qs_left = num_questions


in_  = input('Ready?\n')

if in_ == '':
    if False:
        for i in range(num_questions):
            a, q, last_right, last_wrong = get_random_q_with_stats(db, last_right, last_wrong)
            if not a:
                break
            next = input('\nQ{} '.format(i) + q + '\n')
            if next == '':
                result = input('\nA: ' + a + ' ...Correct?\n')
                if result == '1':
                    correct_qs.append(idx)
                else:
                    wrong_qs.append(idx)
            else:
                print('\nDunno what to do now...\n')
        all_qs = correct_qs + wrong_qs
        print('\nAnswered all questions, result: {}/{}\n'.format(len(correct_qs), len(all_qs)))
    else:
        possible_idx = list(range(num_questions))
        for i in range(num_questions):
            rnd_idx = random.randint(0, num_questions-1)
            num_questions -= 1
            idx = possible_idx[rnd_idx]
            del possible_idx[rnd_idx]
            # Grab q&a
            q = db['Question'].iloc[idx]
            a = db['Answer'].iloc[idx].replace("\\n", "\n")
            top = db['Topic'].iloc[idx]
            next = input('\nQ{} '.format(i) + q + ' [' + top + ']' + '\n')
            if next == '':
                print('Answer\n' + '------')
                result = input(a + ' \n\n...Correct?\n')
                if result == '1':
                    correct_qs.append(idx)
                elif result == 'end':
                    break
                else:
                    wrong_qs.append(idx)
            elif next == 'end':
                break
            else:
                print('\nDunno what to do now...\n')
        all_qs = correct_qs + wrong_qs
        print('\nAnswered all questions, result: {}/{}\n'.format(len(correct_qs), len(all_qs)))

save_stats(course, wrong_qs, all_qs, topic)
