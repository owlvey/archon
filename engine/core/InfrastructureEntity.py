class InfrastructureEntity:

    def __init__(self):
        self.sinks = list()
        self.states = list()
        self.visualizations = list()
        self.hourly_days = None
        self.warning_zone = None

    def load_state(self, state: dict):
        self.sinks = state['sinks']
        self.states = state['states']
        self.visualizations = state['visualizations']
        self.hourly_days = state['hourly_days']
        
        self.warning_zone = state.get('warning_zone', 0)





