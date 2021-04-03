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

        for item in self.sources:
            item.measure_slo()

    def load_members(self, journeys, squads, sources):
        temp = self.journeys
        self.journeys = list()
        for item in temp:          
            journey = next(x for x in journeys if x.journey == item)
            journey.features.append(self)
            self.journeys.append(journey)   

        temp = self.squads
        self.squads = list()
        for item in temp:            
            squad = next(x for x in squads if x.squad == item)
            squad.features.append(self)
            self.squads.append(squad)   
        
        temp = self.sources
        self.sources = list()
        for item in temp:       
            target = next(x for x in sources if x.source == item)             
            target.features.append(self)
            self.sources.append(target)   
        
        self.__measure_slo()
            
        


def features_to_indicators_dataframe(items: List[FeatureEntity]):
    feature_source = list()    
    for item in items:        
        for source in item.sources:
            feature_source.append([item.feature, item.avaSlo, item.expSlo, item.latSlo, source.source])
    
    feature_df = pd.DataFrame(feature_source, columns=['feature', 'avaSlo', 'expSlo', 'latSlo', 'source'])    
    return feature_df




    

  