from engine.core.SourceEntity import SourceEntity
from engine.core.FeatureEntity import FeatureEntity, features_to_dataframe
from engine.core.JourneyEntity import JourneyEntity, journeys_to_dataframe
from engine.core.SquadEntity import SquadEntity
from engine.core.DockerComponseEntity import DockerComposeEntity
from engine.core.ProductEntity import ProductEntity
from engine.core.MemberEntity import MemberEntity
from engine.core.InfrastructureEntity import InfrastructureEntity
from engine.core.StateUtil import StateUtil
import pandas
from typing import List
import itertools

class SystemEntity: 
    def __init__(self):
        self.infrastructure = InfrastructureEntity()
        self.product = ProductEntity()
        self.members = list()
        self.squads = list()
        self.journeys = list()
        self.features = list() # List[JourneyEntity]
        self.sources = list()
        self.compose = DockerComposeEntity()

    def load_state(self, infrastructure: dict,
                   product_state: dict,
                   members_states: list,
                   squads_states: list,
                   journey_states: list,
                   features_states: list):
        self.infrastructure.load_state(infrastructure)
        

        for state in members_states:
            item = MemberEntity()
            StateUtil.load_from_state(item, state)
            self.members.append(item)            
        
        StateUtil.load_from_state(self.product, product_state)
        self.product.load_members(self.members)

        for state in squads_states:
            item = SquadEntity()
            StateUtil.load_from_state(item, state)
            item.load_members(self.members)
            self.squads.append(item)
            
        for state in journey_states:
            item = JourneyEntity()
            StateUtil.load_from_state(item, state)
            item.load_members(self.members)
            self.journeys.append(item)
            
        for state in features_states:
            item = FeatureEntity()            
            StateUtil.load_from_state(item, state)                        
            self.features.append(item)
        
        for source in set(itertools.chain(*[x.sources for x in self.features])):
            item = SourceEntity()
            item.source = source
            self.sources.append(item)
        
        for state in self.features:            
            state.load_members(self.journeys, self.squads, self.sources)
    
    def __str__(self) -> str:
        return self.__dict__.__str__()

    def build_metadata_frame(self):
        journeys_df = journeys_to_dataframe(self.journeys)
        features, squads_df = features_to_dataframe(self.features)
        all = journeys_df.merge(features, left_on='Journey', right_on='Journey', how='inner')
        return all, squads_df





        




