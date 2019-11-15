import pandas as pd
from collections import OrderedDict
import datetime
import random


class Brain:
    def __init__(self, course):
        # TODO: rename database and results files
        self.course = course
        self.database = self.load_database(course)
        self.latest_results = self.load_results(course)
        self.wrong = []
        self.correct = []
        self.topic = None
        self.questions_left = []

    def load_database(self, course):
        try:
            database = pd.read_csv(f'databases/{course}.csv', sep='\t')
            return database
        except:
            # TODO: figure out if better than raise
            print(
                f'Invalid course name or database does not exist for {course}.'
            )
            return None

    def load_results(self, course):
        try:
            results = pd.read_csv(f'results/{course}.csv', sep='\t')
            return results
        except:
            # TODO: figure out if better than raise
            print(f'No previous results found for {course}.')
            return None

    def display_latest_results(self):
        # TODO: add improvement info between sessions
        if self.results:
            date = self.results['Date'].iloc[-1]
            correct = self.results['Correct'].iloc[-1]
            answered = self.results['Answered'].iloc[-1]
            topic = self.results['Topic'].iloc[-1]
            print(f'Latest results: {date} {correct}/{answered} at {topic}\n')
        else:
            print('No latest results at the moment')

    def save_results(self):
        results_dict = OrderedDict()
        # TODO: look for a better date formatter
        results_dict['Date'] = [datetime.datetime.now().strftime('%a %d %b')]
        results_dict['Correct'] = [
            len(self.questions_answered) - len(self.questions_failed)
        ]
        results_dict['Answered'] = [len(self.questions_answered)]
        results_dict['Wrong'] = [sorted(self.questions_failed)]
        results_dict['Topic'] = [self.topic]
        results_df = pd.DataFrame(data=results_dict)
        try:
            results_dict = pd.read_csv(f'results/{self.course}.csv', sep='\t')
            results_dict = results_dict.append(results_df)
            results_dict.to_csv(f'results/{self.course}.csv',
                                sep='\t',
                                index=False)
        except:
            results_df.to_csv(f'results/{self.course}.csv',
                              sep='\t',
                              index=False)

    def ran_out_of_questions(self):
        if len(self.questions_left) == 0:
            return True
        return False

    def choose_topic(self):
        topics = list(self.database['Topic'].unique())
        topics_str = ''
        for idx, topic in enumerate(topics):
            topics_str += f'{str(idx + 1)}. {topic}\n'
        topics_str += f'{str(len(topics) + 1)}. All\n'
        topic_choice = input(f'Choose a topic: \n{topics_str}')

        if topic_choice == str(len(topics) + 1):
            self.topic = topics
        else:
            if '-' in topic_choice:
                topic_idxs = topic_choice.split('-')
                topics_chosen = (topics[int(topic_idxs[0]) - 1], )
                database_reduced = self.database[self.database['Topic'] ==
                                                 topics_chosen[0]]
                for idx in topic_idxs[1:]:
                    topic = topics[int(idx) - 1]
                    database_reduced = database_reduced.append(
                        self.database[self.database['Topic'] == topic],
                        ignore_index=True)
                    topics_chosen = topics_chosen + (topic, )
                self.database = database_reduced
            else:
                self.topic = topic[int(topic_choice) - 1]
                self.database = self.database[self.database['Topic'] ==
                                              self.topic]
        num_questions = len(self.database.index)
        self.questions_left = random.sample(range(0, num_questions),
                                            num_questions)

    def get_next_question(self):
        idx = self.questions_left.pop()
        question = self.database['Question'].iloc[idx]
        answer = self.database['Answer'].iloc[idx].replace("\\n", "\n")
        topic = self.database['Topic'].iloc[idx]

        return question, answer, topic, idx

    def add_correct(self, idx):
        self.correct.append(idx)

    def add_wrong(self, idx):
        self.wrong(idx)
