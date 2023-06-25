import numpy as np
import pandas as pd


def loadData():
    users = {'Alice': {'A': 5, 'B': 3, 'C': 4, 'D': 4},
             'user1': {'A': 3, 'B': 1, 'C': 2, 'D': 3, 'E': 3},
             'user2': {'A': 4, 'B': 3, 'C': 4, 'D': 3, 'E': 5},
             'user3': {'A': 3, 'B': 3, 'C': 1, 'D': 5, 'E': 4},
             'user4': {'A': 1, 'B': 5, 'C': 5, 'D': 2, 'E': 1}
             }
    return users


user_data = loadData()
print(user_data)
simliarity_matrix = pd.DataFrame(
    np.identity(len(user_data)),
    index=user_data.keys(),
    columns=user_data.keys()
)

for u1, items1 in user_data.items():
    for u2, item2 in user_data.items():
        if u1 == u2:
            continue
        vec1, vec2 = [], []
        for item, rating1 in items1.items():
            rating2 = item2.get(item, -1)
            if rating2 == -1:
                continue
            vec1.append(rating1)
            vec2.append(rating2)
        simliarity_matrix[u1][u2] = np.corrcoef(vec1, vec2)[0][1]
print(simliarity_matrix)

target_user = "Alice"
num = 2
sim_users = simliarity_matrix[target_user].sort_values(ascending=False)[1:num+1].index.tolist()
print(f'与用户{target_user}最相似的{num}个用户为:{sim_users}')

weighted_scores = 0.
corr_values_sum = 0.

target_item = 'E'
for user in sim_users:
    corr_value = simliarity_matrix[target_user][user]
    user_mean_rating = np.mean(list(user_data[user].values()))
    weighted_scores += corr_value * (user_data[user][target_item] - user_mean_rating)
    corr_values_sum += corr_value

target_user_mean_rating = np.mean(list(user_data[target_user].values()))
target_item_pred = target_user_mean_rating + weighted_scores / corr_values_sum
print(f'用户{target_user}对物品{target_item}的预测评分为：{target_item_pred}')


