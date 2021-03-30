from engine.core.SourceEntity import SourceEntity
from typing import Collection, List
from numpy.lib.utils import source
import pandas as pd
class FeatureEntity:

    def __init__(self) -> None:
        self.description = None
        self.feature = None
        self.journeys = list()
        self.squads = list()
        self.sources = list() 
        self.avaSlo = 0
        self.expSlo = 0
        self.latSlo = 0
        self.avaSla = 0
        self.latSla = 0

    def __measure_slo(self):
        if not self.journeys:
            raise ValueError('Feature without journeys: {}'.format(self.feature))
        self.avaSlo = max([x.avaSlo for x in self.journeys])
        self.latSlo = max([x.latSlo for x in self.journeys])
        self.expSlo = max([x.expSlo for x in self.journeys])
        self.avaSla = max([x.avaSla for x in self.journeys])
        self.latSla = max([x.latSla for x in self.journeys])

        for source in self.sources:
            source.measure_slo()


    def load_members(self, journeys, squads, sources):
        temp = self.journeys
        self.journeys = list()
        for item in temp:            
            self.journeys.append(next(x for x in journeys if x.journey == item))   

        temp = self.squads
        self.squads = list()
        for item in temp:            
            self.squads.append(next(x for x in squads if x.squad == item))   
        
        temp = self.sources
        self.sources = list()
        for item in temp:       
            target = next(x for x in sources if x.source == item)             
            target.features.append(self)
            self.sources.append(target)   
        
        self.__measure_slo()
            
        

        


def features_to_dataframe(items: List[FeatureEntity]):
    journey_feature = list()
    feature_squad = list()
    feature_source = list()
    data = list()
    for item in items:
        for journey in item.journeys:
            journey_feature.append([journey, item.feature])
        for squad in item.squads:
            feature_squad.append(item.feature, squad)
        for source in item.sources:
            feature_source.append([item.feature, source])

    journey_df = pd.DataFrame(journey_feature, columns=['journey', 'feature'])
    squad_df = pd.DataFrame(journey_feature, columns=['feature', 'squad'])
    feature_df = pd.DataFrame(journey_feature, columns=['feature', 'source'])
    features_all = journey_df.merge(feature_df, left_on='feature', right_on='feature', how='inner')
    return features_all


    

  