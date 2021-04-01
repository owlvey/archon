from typing import List
import pandas as pd

class SquadEntity:

    def __init__(self) -> None:
        self.squad = None
        self.description = None
        self.members = list()    
        self.features = list()
    
    def load_members(self, items):
        temp = self.members
        self.members = list()
        for item in temp:            
            self.members.append(next(x for x in items if x.email == item))

def squads_to_features_dataframe(items: List[SquadEntity]):
    data = list()    
    for item in items:        
        for feature in item.features:
            data.append([item.squad, feature.avaSlo, feature.expSlo, feature.latSlo, feature.feature])
    
    df = pd.DataFrame(data, columns=['squad', 'avaSlo', 'expSlo', 'latSlo', 'feature'])    
    return df


