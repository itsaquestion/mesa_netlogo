"""
使用原始python的opinions模型

"""
# %%
from dataclasses import dataclass
import random

from matplotlib import pyplot as plt
import seaborn as sns

import matplotlib as mpl

from TicToc import tic, toc
import pandas as pd

sns.set()
mpl.rcParams['figure.dpi'] = 300
# %%
num: int
steps: int
epsilon: float
trembling: float

agent_list = []
agent_list_steps = []
data = []


def collect_data(i: int):
    agent_list_steps.append(agent_list.copy())
    step_data = pd.DataFrame(agent_list)
    step_data['tick'] = i
    data.append(step_data)


def clear_all():
    global agent_list
    global agent_list_steps
    global data

    agent_list_steps = []
    agent_list = []
    data = []


@dataclass()
class Agent:
    id: int

    def init(self):
        pass

    def step(self):
        pass

    def __post_init__(self):
        self.init()


def one_of(x=None):
    if x is None:
        x = agent_list
    return random.choice(x)


@dataclass
class OpAgent(Agent):
    id: int
    opinion: float = 0

    def init(self):
        self.opinion = random.random()

    def step(self):
        if random.random() < trembling:
            self.opinion = random.random()
        else:
            other_op = one_of().opinion
            if abs(self.opinion - other_op) < epsilon:
                self.opinion = (self.opinion + other_op) / 2


def setup():
    clear_all()

    for i in range(num):
        agent = OpAgent(i)
        agent_list.append(agent)


def go(ticks):
    for i in range(ticks):
        random.shuffle(agent_list)
        # collect_data(i)

        for agent in agent_list:
            agent.step()


# %%
num = 500
steps = 500

epsilon = 0.1
trembling = 0.001

setup()

tic()
go(steps)
toc()


# %%
data_df = pd.concat(data)

y = data_df.query(f'tick == {max(data_df.tick)}').opinion
plt.hist(y, 100)
plt.show()
