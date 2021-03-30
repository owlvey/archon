from numpy.lib.financial import nper
from pandas.core.frame import DataFrame
from engine.core.SystemEntity import SystemEntity
from engine.core.JourneyEntity import journeys_to_dataframe
from engine.core.SourceEntity import sources_to_dataframe
import pandas as pd
import numpy as np


class DebtAnalasysAggregate:
    def __init__(self, data: DataFrame, system: SystemEntity) -> None:
        self.system = system
        self.data = data

    
    def __build_source_daily(self, sources_df):
        source_analysis = sources_df.merge(self.data, left_on='source', right_on='source', how='left')
        
        output_daily = source_analysis.groupby(
            [pd.Grouper(key='start',freq='D'), 'source', 'avaSlo', 'expSlo', 'latSlo']).agg({
            'total': 'sum',
            'ava': 'sum',
            'exp': 'sum',
            'lat': 'mean'
        }).reset_index()        
        output_daily['ava_prop'] = output_daily['ava'].divide(output_daily['total'])
        output_daily['exp_prop'] = output_daily['exp'].divide(output_daily['total'])
        output_daily.replace([np.inf, -np.inf], 0)
        return output_daily.reset_index()


    def execute(self):
        journeys_df = journeys_to_dataframe(self.system.journeys)
        sources_df = sources_to_dataframe(self.system.sources)
        return self.__build_source_daily(sources_df)

        

    
    
        
        
        