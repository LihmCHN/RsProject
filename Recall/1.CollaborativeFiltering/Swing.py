from itertools import combinations
import pandas as pd

alpha = 0.5
top_k = 20


def load_data(train_path):
    train_data = pd.read_csv(train_path, sep="\t", engine="python", names=["userid", "itemid", "rate"])
    print(train_data.head(3))
    return train_data


def get_uitems_iusers(train):
    u_items = dict()
    i_users = dict()

