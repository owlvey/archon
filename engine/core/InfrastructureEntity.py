class InfrastructureEntity:

    def __init__(self):
        self.sinks = list()
        self.states = list()
        self.visualizations = list()

    def load_state(self, state: dict):
        self.sinks = state['sinks']
        self.states = state['states']
        self.visualizations = state['visualizations']




