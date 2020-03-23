class BaseMember(object):
    def __init__(self, ID, preference, endowment):
        self.ID = ID
        self.preference = preference
        self.endowment = endowment


class PrimitiveMember(BaseMember):
    def __init__(self, ID, preference, endowment, effector, decider, executor, monitor, connector):
        super().__init__(ID, preference, endowment)
        self.effector = effector
        self.decider = decider
        self.executor = executor
        self.monitor = monitor
        self.connector = connector


class CollectiveMember(BaseMember):
    def __init__(self, ID, preference, endowment, decomposer, executor, converger):
        super().__init__(ID, preference, endowment)
        self.decomposer = decomposer
        self.executor = executor
        self.converger = converger


class AdviserMember(BaseMember):
    def __init__(self, ID, preference, endowment, the_conn_primitive):
        super().__init__(ID, preference, endowment)
        self.the_conn_primitive = the_conn_primitive


class MonitorMember(BaseMember):
    def __init__(self, ID, preference, endowment):
        super().__init__(ID, preference, endowment)
