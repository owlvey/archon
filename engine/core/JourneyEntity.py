from collections.abc import Sequence
from typing import List
import pandas as pd
from engine.core.StateUtil import StateUtil


class JourneyEntity: 

    def __init__(self) -> None:
        self.description = None
        self.journey = None
        self.family = None
        self.avaSlo = None
        self.expSlo = None
        self.latSlo = None
        self.avaSla = None
        self.latSla = None

        self.leaders = list()     
        self.features = list()

    @staticmethod
    def __measure_warning(slo, warning_zone):
        return slo + (1 - slo) * warning_zone

    def load_from_state(self, warning_zone: float, state):
        StateUtil.load_from_state(self, state)
        self.avaSlo = JourneyEntity.__measure_warning(self.avaSlo, warning_zone)
        self.expSlo = JourneyEntity.__measure_warning(self.expSlo, warning_zone)
        self.latSlo = self.latSlo - (self.latSlo * warning_zone)

    def load_members(self, items):
        temp = self.leaders
        self.leaders = list()
        for item in temp:            
            self.leaders.append(next(x for x in items if x.email == item))   
    

def journeys_to_dataframe(items: List[JourneyEntity]):
    data = list()
    for item in items:
        data.append([item.journey, item.family, item.avaSlo, item.expSlo, item.latSlo])
    return pd.DataFrame(data, columns=['journey', 'family', 'avaSlo', 'expSlo', 'latSlo'])


def journeys_to_features_dataframe(items: List[JourneyEntity]):
    data = list()    
    for item in items:        
        for feature in item.features:
            data.append([item.family, item.journey, item.avaSlo, item.expSlo, item.latSlo, feature.feature])
    
    df = pd.DataFrame(data, columns=['family', 'journey', 'avaSlo', 'expSlo', 'latSlo', 'feature'])    
    return df


def journeys_to_features_sources_dataframe(items: List[JourneyEntity]):
    data = list()
    for item in items:
        for feature in item.features:
            for source in feature.sources:
                data.append([item.family, item.journey, feature.feature, source.source, item.avaSlo, item.expSlo,
                             item.latSlo])

    df = pd.DataFrame(data, columns=['family', 'journey', 'feature', 'source', 'avaSlo', 'expSlo', 'latSlo'])

    return df

