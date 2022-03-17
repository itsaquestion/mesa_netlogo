import copy
import random
from dataclasses import dataclass, field
from collections import OrderedDict


@dataclass()
class Agent:
    """
    Agent类
    """
    uid: int = 0

    def init(self):
        pass

    def step(self):
        pass

    def __post_init__(self):
        self.init()


class AgentSet:
    """
    AgentSet类，本质上是Agent的一个List。
    自动管理uid，添加时会自增1；添加时deepcopy，因此和原对象无关联。
    """

    def __init__(self):
        self.agent_list: list = []

    def add(self, a: Agent):
        if len(self.agent_list) == 0:
            a.uid = 0
        else:
            a.uid = max([b.uid for b in self.agent_list]) + 1

        self.agent_list.append(copy.deepcopy(a))

    def shuffle(self):
        random.shuffle(self.agent_list)


class ABM:
    def __init__(self):
        self.tick_data: OrderedDict = OrderedDict()

    def get_max_tick(self):
        return max(self.tick_data.keys())

    def tick(self):
        """
        时间往前走一步。实质上是把最后一个tick的数据，复制到末尾，且使其tick+1，
        使用self.append，因此是deepcopy
        :return:
        """
        self.append(self.last())

    def append(self, agent_set: AgentSet):
        """
        在最后添加一个AgentSet：如果原来没有数据，则tick=0；如果有数据，则tick递增1。
        使用copy.deepcopy，因此添加后数据将和源数据没有关联
        可用于setup过程。
        :param agent_set:
        :return:
        """
        i: int = 0
        if len(self.tick_data) > 0:
            i = self.get_max_tick() + 1

        """
        deepcopy避免引入引用。
        每个tick的状态，应该相互独立；
        当一个tick完成，数据应该不再变更
        """
        self.tick_data[i] = copy.deepcopy(agent_set)

    def last(self) -> AgentSet:
        """
        获得最后时间截面的AgentSet
        :return: 最后时间截面的AgentSet
        """
        return self.tick_data[self.get_max_tick()]

    def get(self, tick: int) -> AgentSet:
        """
        按tick，获得时间截面的AgentSet
        :param tick: tick
        :return: tick时间的AgentSet
        """
        # if tick < 0 | tick > self.get_max_tick():
        #     raise ValueError("tick应该在[0,最大tick]之间")

        return self.tick_data[tick]
