from engine.core.SystemEntity import SystemEntity
from engine.core.FeatureEntity import features_to_indicators_dataframe
import pandas as pd

class DebtGraphAnalysisAggregate:

    def __init__(self, system: SystemEntity, hourly_source: pd.DataFrame) -> None:        
        self.system = system
        self.hourly_source = hourly_source
    
    def execute(self): 
        features_source_df = features_to_indicators_dataframe(self.system.features)[['feature', 'source']].copy()
        feature_source_graph = features_source_df.merge(self.hourly_source, left_on='source',  right_on='source', how='inner')
        return feature_source_graph
        

