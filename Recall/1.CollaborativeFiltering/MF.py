import random
import math


def loadData():
    rating_data = {1: {'A': 5, 'B': 3, 'C': 4, 'D': 4},
                   2: {'A': 3, 'B': 1, 'C': 2, 'D': 3, 'E': 3},
                   3: {'A': 4, 'B': 3, 'C': 4, 'D': 3, 'E': 5},
                   4: {'A': 3, 'B': 3, 'C': 1, 'D': 5, 'E': 4},
                   5: {'A': 1, 'B': 5, 'C': 5, 'D': 2, 'E': 1}
                   }
    return rating_data


class BiasSVD():
    def __init__(self, rating_data, F=5, alpha=0.1, lmbda=0.1, max_iter=100):
        self.F = F
        self.P = dict()
        self.Q = dict()
        self.bu = dict()
        self.bi = dict()
        self.mu = 0
        self.alpha = alpha
        self.lmbda = lmbda
        self.max_iter = max_iter
        self.rating_data = rating_data

        for user, items in self.rating_data.items():
            self.P[user] = [random.random() / math.sqrt(self.F) for x in range(0, F)]
            self.bu[user] = 0
            for item, rating in items.items():
                if item not in self.Q:
                    self.Q[item] = [random.random() / math.sqrt(self.F) for x in range(0, F)]
                    self.bi[item] = 0

    def train(self):
        cnt, mu_sum = 0, 0
        for user, items in self.rating_data.items():
            for item, rui in items.items():
                mu_sum, cnt = mu_sum + rui, cnt + 1
        self.mu = mu_sum / cnt

        for step in range(self.max_iter):
            for user, items in self.rating_data.items():
                for item, rui in items.items():
                    rhat_ui = self.predict(user, item)
                    e_ui = rui - rhat_ui

                    self.bu[user] += self.alpha * (e_ui - self.lmbda * self.bu[user])
                    self.bi[item] += self.alpha * (e_ui - self.lmbda * self.bi[item])
                    for k in range(0, self.F):
                        self.P[user][k] += self.alpha * (e_ui * self.Q[item][k] - self.lmbda * self.P[user][k])
                        self.Q[item][k] += self.alpha * (e_ui * self.P[user][k] - self.lmbda * self.Q[item][k])
            self.alpha *= 0.1

    def predict(self, user, item):
        return sum(self.P[user][f] * self.Q[item][f] for f in range(0, self.F)) + self.bu[user] + self.bi[item] + self.mu


rating_data = loadData()
basicsvd = BiasSVD(rating_data, F=10)
basicsvd.train()
for item in ["E"]:
    print(item, basicsvd.predict(1, item))