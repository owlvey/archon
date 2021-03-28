class DockerContainerEntity:
    def __init__(self):
        self.image = None
        self.environment = dict()

    def set_environments(self, state: dict):
        for k, v in state.items():
            self.environment[k] = v


