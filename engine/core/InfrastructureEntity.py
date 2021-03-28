class InfrastructureEntity:

    def __init__(self):
        self.sinks = list()

    def load_state(self, state: dict):
        self.sinks = state['sinks']



