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
        
    @staticmethod
    def seek_squad(squads, target):
        for squad in squads:
            if squad.squad == target:
                return squad
        else:
            raise ValueError(f"squad not found {target}")


def squads_to_features_dataframe(items: List[SquadEntity]):
    data = list()    
    for item in items:        
        for feature in item.features:
            data.append([item.squad, feature.feature])
    
    df = pd.DataFrame(data, columns=['squad', 'feature'])
    return df


