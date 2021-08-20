import pandas as pd
import random
import torch
from sklearn.model_selection import train_test_split
from torchtext.legacy.data import Field, TabularDataset, BucketIterator

from fetch_db import reddit_data

subreddit_labels = {1: "askhistorians", 2: "writingprompts", 
                    3: "television", 4: "explainlikeimfive", 
                    5: "lifeprotips", 6: "relationship_advice",
                    7: "science", 8: "books",
                    9: "nba", 10: "philosophy"}

train_test_ratio = 0.90
train_valid_ratio = 0.90

mod_data = []
for i in reddit_data:
    title_index = list(subreddit_labels.keys())[list(subreddit_labels.values()).index(i[2])]
    mod_data.append((title_index, i[1]))
    
random.shuffle(mod_data)

df_data = {"label": [], "text": []}

for i in mod_data:
    df_data["label"].append(i[0])
    df_data["text"].append(i[1])
    
df_data = pd.DataFrame(df_data)

df_1 = df_data[df_data['label'] == 1]
df_2 = df_data[df_data['label'] == 2]
df_3 = df_data[df_data['label'] == 3]
df_4 = df_data[df_data['label'] == 4]
df_5 = df_data[df_data['label'] == 5]
df_6 = df_data[df_data['label'] == 6]
df_7 = df_data[df_data['label'] == 7]
df_8 = df_data[df_data['label'] == 8]
df_9 = df_data[df_data['label'] == 9]
df_10 = df_data[df_data['label'] == 10]

df_1_full_train, df_1_test = train_test_split(df_1, train_size = train_test_ratio, random_state = 1)
df_2_full_train, df_2_test = train_test_split(df_2, train_size = train_test_ratio, random_state = 1)
df_3_full_train, df_3_test = train_test_split(df_3, train_size = train_test_ratio, random_state = 1)
df_4_full_train, df_4_test = train_test_split(df_4, train_size = train_test_ratio, random_state = 1)
df_5_full_train, df_5_test = train_test_split(df_5, train_size = train_test_ratio, random_state = 1)
df_6_full_train, df_6_test = train_test_split(df_6, train_size = train_test_ratio, random_state = 1)
df_7_full_train, df_7_test = train_test_split(df_7, train_size = train_test_ratio, random_state = 1)
df_8_full_train, df_8_test = train_test_split(df_8, train_size = train_test_ratio, random_state = 1)
df_9_full_train, df_9_test = train_test_split(df_9, train_size = train_test_ratio, random_state = 1)
df_10_full_train, df_10_test = train_test_split(df_10, train_size = train_test_ratio, random_state = 1)

df_1_train, df_1_valid = train_test_split(df_1_full_train, train_size = train_valid_ratio, random_state = 1)
df_2_train, df_2_valid = train_test_split(df_2_full_train, train_size = train_valid_ratio, random_state = 1)
df_3_train, df_3_valid = train_test_split(df_3_full_train, train_size = train_valid_ratio, random_state = 1)
df_4_train, df_4_valid = train_test_split(df_4_full_train, train_size = train_valid_ratio, random_state = 1)
df_5_train, df_5_valid = train_test_split(df_5_full_train, train_size = train_valid_ratio, random_state = 1)
df_6_train, df_6_valid = train_test_split(df_6_full_train, train_size = train_valid_ratio, random_state = 1)
df_7_train, df_7_valid = train_test_split(df_7_full_train, train_size = train_valid_ratio, random_state = 1)
df_8_train, df_8_valid = train_test_split(df_8_full_train, train_size = train_valid_ratio, random_state = 1)
df_9_train, df_9_valid = train_test_split(df_9_full_train, train_size = train_valid_ratio, random_state = 1)
df_10_train, df_10_valid = train_test_split(df_10_full_train, train_size = train_valid_ratio, random_state = 1)

df_train = pd.concat([df_1_train, df_2_train,
                      df_3_train, df_4_train,
                      df_5_train, df_6_train,
                      df_7_train, df_8_train,
                      df_9_train, df_10_train,], ignore_index=True, sort=False)
df_valid = pd.concat([df_1_valid, df_2_valid,
                      df_3_valid, df_4_valid,
                      df_5_valid, df_6_valid,
                      df_7_valid, df_8_valid,
                      df_9_valid, df_10_valid,], ignore_index=True, sort=False)
df_test = pd.concat([df_1_test, df_2_test,
                     df_3_test, df_4_test,
                     df_5_test, df_6_test,
                     df_7_test, df_8_test,
                     df_9_test, df_10_test,], ignore_index=True, sort=False)

destination_folder = 'Data'

df_train.to_csv(destination_folder + '/train.csv', index=False)
df_valid.to_csv(destination_folder + '/valid.csv', index=False)
df_test.to_csv(destination_folder + '/test.csv', index=False)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

label_field = Field(sequential=False, use_vocab=False, batch_first=True, dtype=torch.float)
text_field = Field(tokenize='spacy', lower=True, include_lengths=True, batch_first=True)
fields = [('label', label_field), ('text', text_field)]

train, valid, test = TabularDataset.splits(path=destination_folder, train='train.csv', validation='valid.csv', test='test.csv',
                                           format='CSV', fields=fields, skip_header=True)

train_iter = BucketIterator(train, batch_size=32, sort_key=lambda x: len(x.text),
                            device=device, sort=True, sort_within_batch=True)
valid_iter = BucketIterator(valid, batch_size=32, sort_key=lambda x: len(x.text),
                            device=device, sort=True, sort_within_batch=True)
test_iter = BucketIterator(test, batch_size=32, sort_key=lambda x: len(x.text),
                            device=device, sort=True, sort_within_batch=True)

text_field.build_vocab(train, min_freq=3)