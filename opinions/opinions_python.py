"""
使用原始python的opinions模型

"""
# %%
from dataclasses import dataclass
import random

from matplotlib import pyplot as plt
import seaborn as sns

from TicToc import tic, toc
import pandas as pd
import numpy as np

sns.set()

# %%
num = 500
steps = 500

epsilon: float = 0.1

agent_list = []

agent_list_steps = []

trembling = 0.001

data = []


@dataclass
class Agent:
    id: int
    opinion: float

    def step(self):
        if random.random() < trembling:
            self.opinion = random.random()
        else:
            other_op = one_of().opinion
            if abs(self.opinion - other_op) < epsilon:
                self.opinion = (self.opinion + other_op) / 2


def one_of(x=None) -> Agent:
    if x is None:
        x = agent_list
    return random.choice(x)


def setup():
    for i in range(num):
        a = Agent(i, round(random.random(), 2))
        agent_list.append(a)


def go():
    for i in range(steps):

        agent_list_steps.append(agent_list.copy())

        random.shuffle(agent_list)

        step_data = pd.DataFrame(agent_list)
        # step_data.sort_values('id', inplace=True)
        step_data['step'] = i
        data.append(step_data)

        for agent in agent_list:
            agent.step()


# %%
setup()

tic()
go()
toc()

# %%
data_df = pd.concat(data)
data_df.sort_values(['step', 'id'], inplace=True)
print(data_df)

# %%

y = data_df.query(f'step == {max(data_df.step)}').opinion

plt.hist(y, 100)

plt.show()
