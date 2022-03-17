from dataclasses import dataclass

import pytest

from ABM.Agents import AgentSet, Agent, ABM

agents = AgentSet()


@dataclass
class TheAgent(Agent):
    x: int = 0  # 继承后，新添加的变量（如x），在__init__的参数里位于后面，因此必须有初始值


def setup_module():
    # print('\n====初始化模块====')

    for i in range(10):
        a_agent = TheAgent()
        agents.add(a_agent)


def teardown_module():
    # print('\n====清除模块====')
    pass


class TestAgent:

    def test_uid(self):
        uid_list = [a.uid for a in agents.agent_list]

        # uid唯一
        assert len(uid_list) == len(set(uid_list))

        # 最大值正确
        assert max(uid_list) == 9

    def test_shuffle(self):
        a = [a.uid for a in agents.agent_list]
        agents.shuffle()
        b = [a.uid for a in agents.agent_list]

        assert a != b


class TestTickData:

    def test_add(self):
        model = ABM()

        aset = AgentSet()

        for i in range(3):
            a = TheAgent()
            aset.add(a)

        model.append(aset)

        assert model.get_max_tick() == 0

        model.append(aset)

        assert model.get_max_tick() == 1

        """
        采用deepcopy，避免导入引用
        """
        aset.agent_list[0].x = 2
        model.tick_data[0].agent_list[0].x = 3
        model.tick_data[1].agent_list[0].x = 4

        assert model.tick_data[0].agent_list[0].x == 3
        assert model.tick_data[1].agent_list[0].x == 4

        a = model.get(0)
        assert a.agent_list[0].x == 3

        b = model.get(1)
        assert b.agent_list[0].x == 4

        c = model.last()
        assert c.agent_list[0].x == 4

        model.tick()

        assert model.get_max_tick() == 2
        d = model.last()
        d.agent_list[0].x = 5
        assert c.agent_list[0].x == 4
