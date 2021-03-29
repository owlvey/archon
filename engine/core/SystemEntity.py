from engine.core.FeatureEntity import FeatureEntity
from engine.core.JourneyEntity import JourneyEntity
from engine.core.SquadEntity import SquadEntity
from engine.core.DockerComponseEntity import DockerComposeEntity
from engine.core.ProductEntity import ProductEntity
from engine.core.MemberEntity import MemberEntity
from engine.core.InfrastructureEntity import InfrastructureEntity
from engine.core.DockerContainerEntity import DockerContainerEntity
from engine.core.StateUtil import StateUtil
import itertools

class SystemEntity: 
    def __init__(self):
        self.infrastructure = InfrastructureEntity()
        self.product = ProductEntity()
        self.members = list()
        self.squads = list()
        self.journeys = list()
        self.features = list()
        self.compose = DockerComposeEntity()

    def load_state(self, infrastructure: dict,
                   product_state: dict,
                   members_states: list,
                   squads_states: list,
                   journey_states: list,
                   features_states: list):
        self.infrastructure.load_state(infrastructure)
        StateUtil.load_from_state(self.product, product_state)
        for state in members_states:
            item = MemberEntity()
            StateUtil.load_from_state(item, state)
            self.members.append(item)
        for state in squads_states:
            item = SquadEntity()
            StateUtil.load_from_state(item, state)
            self.squads.append(item)
        for state in journey_states:
            item = JourneyEntity()
            StateUtil.load_from_state(item, state)
            self.journeys.append(item)
        for state in features_states:
            item = FeatureEntity()
            StateUtil.load_from_state(item, state)
            self.features.append(item)

    def get_sources(self):
        sources = set(itertools.chain(*[x.sources for x in self.features]))
        return sources
    
    def __str__(self) -> str:
        return self.__dict__.__str__()




