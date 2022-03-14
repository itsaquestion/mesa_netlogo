"""
mesa的财富分配模型 + netlogo作为控制和绘图界面

"""
import time

# import numba
from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from NL import NL


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    return gini(agent_wealths)


def gini(agent_wealths):
    x = sorted(agent_wealths)
    N = len(agent_wealths)
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))

    return 1 + (1 / N) - 2 * B


class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        if self.wealth == 0:
            return
        other_agent = self.random.choice(self.model.schedule.agents)
        other_agent.wealth += 1
        self.wealth -= 1


class MoneyModel(Model):

    def __init__(self, n):
        self.num_agents = n

        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

        self.datacollector = DataCollector(
            model_reporters={"gini": compute_gini},
            agent_reporters={"Wealth": "wealth"}
        )

        nl.clear_reset()

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        # 要绘制的变量名，netlogo中要和DataCollector中相同
        var_list = ['gini']

        for var in var_list:
            nl.set(var, self.get_last_value(var))

        nl.tick()

    def get_last_value(self, var):
        return self.datacollector.model_vars[var][-1]


# %%
nl = NL()
nl.load_model('./money_model.nlogo')

# %%
num = int(nl.get("num"))
steps = int(nl.get("steps"))

t = time.time()
model: Model = MoneyModel(num)

for i in range(steps):
    # print(i)
    model.step()

elapsed = time.time() - t
print(round(elapsed, 2))


# %%
t = time.time()
nl.cmd('setup')
nl.cmd('repeat steps [go]')
elapsed = time.time() - t
print(round(elapsed, 2))

# %%
nl.close()
