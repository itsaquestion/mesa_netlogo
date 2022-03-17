"""
使用原始python的opinions模型

"""
# %%

from matplotlib import pyplot as plt
import seaborn as sns

import matplotlib as mpl

from TicToc import tic, toc


from ABM.Agents import *

sns.set()
mpl.rcParams['figure.dpi'] = 300
# %%
model = ABM()


def clear_all():
    global model
    model = ABM()


def one_of(x=None):
    if x is None:
        x = model.last().agent_list
    return random.choice(x)


@dataclass
class WeAgent(Agent):
    wealth: int = 1

    def init(self):
        pass

    def step(self):
        if self.wealth >= 1:
            other_agent = one_of()
            other_agent.wealth += 1
            self.wealth -= 1


def setup(num_agents: int):
    clear_all()

    agents = AgentSet()

    for i in range(num_agents):
        agent = WeAgent()
        agents.add(agent)

    model.append(agents)


def go(steps: int = 1):
    for i in range(steps):

        model.tick()

        agents = model.last()

        agents.shuffle()
        for agent in agents.agent_list:
            agent.step()

        # if model.get_max_tick() % 1 == 0:
        #
        #     y = [a.wealth for a in model.last().agent_list]
        #     plt.hist(y, 7)
        #     plt.show()


# %%
num = 500
steps = 500

# epsilon = 0.1
# trembling = 0.001

setup(num)

tic()
go(steps)
toc()

# # %%
#
# x = model.last()
#
# y = [a.wealth for a in x.agent_list]
# plt.hist(y, 7)
# plt.show()
