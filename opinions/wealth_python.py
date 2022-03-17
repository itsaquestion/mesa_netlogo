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
# epsilon: float
# trembling: float

agent_list = []
agent_list_steps = []
data = []
ticks = 0


def collect_data():
    agent_list_steps.append(agent_list.copy())
    step_data = pd.DataFrame(agent_list)
    step_data['tick'] = ticks
    data.append(step_data)


def clear_all():
    global agent_list
    global agent_list_steps
    global data
    global ticks

    agent_list_steps = []
    agent_list = []
    data = []
    ticks = 0


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
class WeAgent(Agent):
    id: int
    wealth: int = 1

    def init(self):
        pass

    def step(self):
        if self.wealth >= 1:
            other_agent = one_of()
            other_agent.wealth += 1
            self.wealth -= 1


def setup():
    clear_all()

    for i in range(num):
        agent = WeAgent(i)
        agent_list.append(agent)

    collect_data()


def tick():
    global ticks
    ticks += 1


def go(steps):
    for i in range(steps):
        tick()

        random.shuffle(agent_list)
        for agent in agent_list:
            agent.step()

        collect_data()


# %%
num = 500
steps = 500

# epsilon = 0.1
# trembling = 0.001

setup()

tic()
go(steps)
toc()

# %%
data_df = pd.concat(data)

y = data_df.query(f'tick == {max(data_df.tick)}').wealth
plt.hist(y, 7)
plt.show()

# %%
data_df
