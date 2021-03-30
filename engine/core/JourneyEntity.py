from collections.abc import Sequence
from typing import List
import pandas as pd
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