from engine.core.DockerComponseEntity import DockerComposeEntity
from engine.core.ProductEntity import ProductEntity
from engine.core.MemberEntity import MemberEntity
from engine.core.InfrastructureEntity import InfrastructureEntity
from engine.core.DockerContainerEntity import DockerContainerEntity
from engine.core.StateUtil import StateUtil


class SystemEntity: 
    def __init__(self):
        self.infrastructure = InfrastructureEntity()
        self.product = ProductEntity()
        self.members = list()
        self.squads = list()
        self.compose = DockerComposeEntity()

    def load_state(self, infrastructure: dict,
                   product_state: dict,
                   members_state: list):
        self.infrastructure.load_state(infrastructure)
        StateUtil.load_from_state(self.product, product_state)

    def generate_sinks(self):
        for sink in self.infrastructure.sinks:
            if sink['type'] == "dynatrace":
                container = DockerContainerEntity()
                container.image = ""
                del sink['type']
                container.set_environments(sink)
                self.compose.sinks.append(container)

    def generate_app(self):
        self.generate_sinks()
        return self.compose.build_state()




