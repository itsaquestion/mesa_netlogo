"""
使用mesa的opinions模型

"""
# %%
import time

# import numba
from dataclasses import dataclass

import numpy as np
from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import random

from TicToc import tic, toc

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


# %%

def one_of(model: Model):
    return random.choice(model.schedule.agents)


def stdlize(x):
    if x > 1:
        return 1
    if x < 0:
        return 0
    return x


@dataclass()
class OpAgent(Agent):
    unique_id: int
    model: Model
    opinion: float

    # def __post_init__(self):
    #     super().__init__(self.unique_id, self.model)
    #
    #     self.opinion = stdlize(self.opinion)

    def step(self):

        if random.random() < self.model.trembling:
            self.opinion = random.random()
        else:
            other_agent = one_of(self.model)

            diff = self.opinion - other_agent.opinion
            # 如果观点足够接近，则相互吸引
            if abs(diff) < self.model.epsilon:
                self.opinion = (self.opinion + other_agent.opinion) / 2

        # self.opinion = stdlize(self.opinion)


@dataclass
class OpModel(Model):
    num_agents: int
    epsilon: float
    trembling: float = 0.001

    def __post_init__(self):
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            a = OpAgent(i, self, opinion=round(random.random(), 2))

            self.schedule.add(a)

        self.datacollector = DataCollector(
            # model_reporters={"gini": compute_gini},
            agent_reporters={"opinion": "opinion"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


# %%
num = 500
steps = 500

model = OpModel(num, epsilon=0.1, trembling=0.01)

tic()
for i in range(steps):
    # print(i)
    model.step()
toc()

# x = model.datacollector.get_agent_vars_dataframe()
# print(x.head())

# %%

# df = x.reset_index()
# y = df[df['Step'] == max(df['Step'])]
#
# y.opinion.plot.hist(bins=100)
# plt.show()
#
# print(np.unique(round(y.opinion, 2)))
