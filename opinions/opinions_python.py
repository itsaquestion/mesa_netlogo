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

agents = []
agent_list_steps = []
data = []
ticks = 0


def collect_data(i: int):
    agent_list_steps.append(agents.copy())
    step_data = pd.DataFrame(agents)
    step_data['tick'] = i
    data.append(step_data)


def clear_all():
    global agents
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
        x = agents
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
        agents.append(agent)


def tick():
    global ticks
    ticks += 1


def go(steps):
    for i in range(steps):
        tick()

        random.shuffle(agents)
        for agent in agents:
            agent.step()

        collect_data(ticks)


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
