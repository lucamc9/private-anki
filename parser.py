''' Grab questions and answers from txt file and convert to csv  '''

import pandas as pd
import sys
from collections import OrderedDict

filename = sys.argv[1]
output_name = sys.argv[2]

is_first_df = True
topic = ''
df_columns = ['Topic', 'Question', 'Answer']
for line in open(filename, 'r'):
	line_lst = line.split()
	if len(line_lst) > 0:
		if line_lst[0].isdigit():
			topic = ' '.join(line_lst[1:])
		elif line_lst[0] == '•':
			question = ' '.join(line_lst[1:])
		elif line_lst[0] == '-':
			answer = ' '.join(line_lst[1:])
			df_dict = OrderedDict()
			df_dict['Topic'] = [topic]
			df_dict['Question'] = [question]
			df_dict['Answer'] = [answer]
			df = pd.DataFrame(data=df_dict)
			if is_first_df:
				df_master = df
				is_first_df = False
			else:
				df_master = df_master.append(df, ignore_index=True)

df_master.to_csv(output_name, sep='\t', index=False)
