import pandas as pd
import ast
from collections import OrderedDict
import datetime

# def load_database(course):
#     db = pd.read_csv(f'databases/{course}-db.csv', sep='\t')
#     return db

# def load_statistics(course):
#     statistics = pd.read_csv(f'statistics/{course}-stats.csv', sep='\t')
#     return statistics

# def display_stats(stats):
#     date_latest = stats['Date'].iloc[-1]
#     correct_latest = stats['Correct'].iloc[-1]
#     answered_latest = stats['Answered'].iloc[-1]
#     topic_latest = stats['Topic'].iloc[-1]
#     print('Latest score: {} {}/{} at {}\n'.format(date_latest, correct_latest,
#                                                   answered_latest,
#                                                   topic_latest))
# print('|Improvement| Since First: {}, Since Previous: {}')

# def save_stats(course, wrong_qs, all_qs, topic):
#     stats_dict = OrderedDict()
#     stats_dict['Date'] = [datetime.datetime.now().strftime('%a %d %b')]
#     stats_dict['Correct'] = [len(all_qs) - len(wrong_qs)]
#     stats_dict['Answered'] = [len(all_qs)]
#     stats_dict['Wrong'] = [sorted(wrong_qs)]
#     stats_dict['Topic'] = [topic]
#     stats_df = pd.DataFrame(data=stats_dict)
#     try:
#         stats_db = pd.read_csv(f'statistics/{course}-stats.csv', sep='\t')
#         stats_db = stats_db.append(stats_df)
#         stats_db.to_csv(f'statistics/{course}-stats.csv',
#                         sep='\t',
#                         index=False)
#     except:
#         stats_df.to_csv(f'statistics/{course}-stats.csv',
#                         sep='\t',
#                         index=False)


def get_random_q_with_stats(db, last_right, last_wrong):
    if len(last_wrong) > 0 and len(last_right) > 0:
        # Random questions
        if random.uniform(0, 1) <= p:
            rnd_idx = random.randint(0, len(last_wrong) - 1)
            idx = last_wrong[rnd_idx]
            del last_wrong[rnd_idx]
            # Grab q&a
            q = db['Question'].iloc[idx]
            a = db['Answer'].iloc[idx].replace("\\n", "\n")
        else:
            rnd_idx = random.randint(0, len(last_right) - 1)
            idx = last_right[rnd_idx]
            del last_right[rnd_idx]
            # Grab q&a
            q = db['Question'].iloc[idx]
            a = db['Answer'].iloc[idx].replace("\\n", "\n")
    else:
        # qs left from wrong
        if len(last_wrong) > 0:
            rnd_idx = random.randint(0, len(last_wrong) - 1)
            idx = last_wrong[rnd_idx]
            del last_wrong[rnd_idx]
            # Grab q&a
            q = db['Question'].iloc[idx]
            a = db['Answer'].iloc[idx].replace("\\n", "\n")
        # qs left from right
        elif len(last_right) > 0:
            rnd_idx = random.randint(0, len(last_right) - 1)
            idx = last_right[rnd_idx]
            del last_right[rnd_idx]
            # Grab q&a
            q = db['Question'].iloc[idx]
            a = db['Answer'].iloc[idx].replace("\\n", "\n")
        else:
            # No qs left
            q = False
            a = False
    return a, q, last_right, last_wrong


def get_preferred_topic_or_none(db):
    topics = list(db['Topic'].unique())
    topics_str = ''
    for topic_idx in range(len(topics)):
        topics_str += str(topic_idx + 1) + '. ' + topics[topic_idx] + '\n'
    topics_str += str(len(topics) + 1) + '. ' + 'All' + '\n'
    topic_choice = input('Choose a topic: \n' + topics_str)
    if topic_choice != str(len(topics) + 1):
        if '-' in topic_choice:
            topic_idxs = topic_choice.split('-')
            final_topics = (topics[int(topic_idxs[0]) - 1], )
            db_reduced = db[db['Topic'] == final_topics[0]]
            for idx in topic_idxs[1:]:
                topic = topics[int(idx) - 1]
                db_reduced = db_reduced.append(db[db['Topic'] == topic],
                                               ignore_index=True)
                final_topics = final_topics + (topic, )
            db = db_reduced
        else:
            final_topics = topics[int(topic_choice) - 1]
            db = db[db['Topic'] == final_topics]
    else:
        final_topics = topics

    return db, len(db.index), final_topics
