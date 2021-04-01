from numpy.lib.financial import nper
from pandas.core.frame import DataFrame
from engine.core.SystemEntity import SystemEntity
from engine.core.JourneyEntity import journeys_to_features_dataframe, journeys_to_dataframe
from engine.core.SourceEntity import sources_to_dataframe
from engine.core.SquadEntity import squads_to_features_dataframe
from engine.core.FeatureEntity import features_to_indicators_dataframe
import pandas as pd
import numpy as np


class DebtAnalasysAggregate:
    def __init__(self, data: DataFrame, system: SystemEntity) -> None:
        self.system = system
        self.data = data

    
    def __build_source_hourly(self, sources_df):
        source_analysis = sources_df.merge(self.data, left_on='source', right_on='source', how='left')
        
        output_hourly = source_analysis.groupby(
            [pd.Grouper(key='start',freq='H'), 'source', 'avaSlo', 'expSlo', 'latSlo']).agg({
            'total': 'sum',
            'ava': 'sum',
            'exp': 'sum',
            'lat': 'mean'
        }).reset_index()        

        output_hourly['ava_prop'] = output_hourly['ava'].divide(output_hourly['total'])
        output_hourly['exp_prop'] = output_hourly['exp'].divide(output_hourly['total'])

        output_hourly['ava_debt'] = output_hourly.apply(lambda x: 0 if x['ava_prop'] >= x['avaSlo'] else x['avaSlo'] - x['ava_prop'], axis=1)
        output_hourly['exp_debt'] = output_hourly.apply(lambda x: 0 if x['exp_prop'] >= x['expSlo'] else x['expSlo'] - x['exp_prop'], axis=1)
        output_hourly['lat_debt'] = output_hourly.apply(lambda x: 0 if x['lat'] <= x['latSlo'] else x['lat'] - x['latSlo'], axis=1)       

        output_hourly['ava_budget'] = output_hourly.apply(lambda x: 0 if x['ava_prop'] < x['avaSlo'] else x['ava_prop'] - x['avaSlo'], axis=1)
        output_hourly['exp_budget'] = output_hourly.apply(lambda x: 0 if x['exp_prop'] < x['expSlo'] else x['exp_prop'] - x['expSlo'], axis=1)
        output_hourly['lat_budget'] = output_hourly.apply(lambda x: 0 if x['lat'] > x['latSlo'] else x['latSlo'] - x['lat'], axis=1)       

        output_hourly.replace([np.inf, -np.inf], 0)

        return output_hourly.reset_index()
    
    def __build_features_hourly(self, features_source_df, hourly_source):        
        hourly_source = hourly_source[['source', 'start', 'ava_prop', 'exp_prop', 'lat']].copy()
        merged = features_source_df.merge(hourly_source, left_on='source',  right_on='source', how='left')
        
        output_hourly = merged.groupby(['feature', 'start' ]).aggregate(
        {
                "avaSlo": 'max',                 
                'expSlo': 'max', 
                'latSlo': 'min',
                'ava_prop': 'min',
                'exp_prop': 'min',
                'lat': 'max'
        }).reset_index()

        output_hourly['ava_debt'] = output_hourly.apply(lambda x: 0 if x['ava_prop'] >= x['avaSlo'] else x['avaSlo'] - x['ava_prop'], axis=1)
        output_hourly['exp_debt'] = output_hourly.apply(lambda x: 0 if x['exp_prop'] >= x['expSlo'] else x['expSlo'] - x['exp_prop'], axis=1)
        output_hourly['lat_debt'] = output_hourly.apply(lambda x: 0 if x['lat'] <= x['latSlo'] else x['lat'] - x['latSlo'], axis=1)       

        output_hourly['ava_budget'] = output_hourly.apply(lambda x: 0 if x['ava_prop'] < x['avaSlo'] else x['ava_prop'] - x['avaSlo'], axis=1)
        output_hourly['exp_budget'] = output_hourly.apply(lambda x: 0 if x['exp_prop'] < x['expSlo'] else x['exp_prop'] - x['expSlo'], axis=1)
        output_hourly['lat_budget'] = output_hourly.apply(lambda x: 0 if x['lat'] > x['latSlo'] else x['latSlo'] - x['lat'], axis=1)       

        output_hourly.replace([np.inf, -np.inf], 0)

        return output_hourly
    
    def __build_journeys_hourly(self, journey_feature_df, hourly_feature):        
        hourly_feature = hourly_feature[['feature', 'start', 'ava_prop', 'exp_prop', 'lat']].copy()
        merged = journey_feature_df.merge(hourly_feature, left_on='feature',  right_on='feature', how='left')
        
        output_hourly = merged.groupby(['family', 'journey', 'start' ]).aggregate(
        {
                "avaSlo": 'max',                 
                'expSlo': 'max', 
                'latSlo': 'min',
                'ava_prop': 'min',
                'exp_prop': 'min',
                'lat': 'max'
        }).reset_index()

        output_hourly['ava_debt'] = output_hourly.apply(lambda x: 0 if x['ava_prop'] >= x['avaSlo'] else x['avaSlo'] - x['ava_prop'], axis=1)
        output_hourly['exp_debt'] = output_hourly.apply(lambda x: 0 if x['exp_prop'] >= x['expSlo'] else x['expSlo'] - x['exp_prop'], axis=1)
        output_hourly['lat_debt'] = output_hourly.apply(lambda x: 0 if x['lat'] <= x['latSlo'] else x['lat'] - x['latSlo'], axis=1)       

        output_hourly['ava_budget'] = output_hourly.apply(lambda x: 0 if x['ava_prop'] < x['avaSlo'] else x['ava_prop'] - x['avaSlo'], axis=1)
        output_hourly['exp_budget'] = output_hourly.apply(lambda x: 0 if x['exp_prop'] < x['expSlo'] else x['exp_prop'] - x['expSlo'], axis=1)
        output_hourly['lat_budget'] = output_hourly.apply(lambda x: 0 if x['lat'] > x['latSlo'] else x['latSlo'] - x['lat'], axis=1)       

        output_hourly.replace([np.inf, -np.inf], 0)

        return output_hourly
    
    def __build_squad_hourly(self, squad_feature_df, hourly_feature):        
        hourly_feature = hourly_feature[['feature', 'start', 'ava_prop', 'exp_prop', 'lat', 'ava_debt', 'exp_debt', 'lat_debt', 'ava_budget', 'exp_budget', 'lat_budget']].copy()
        merged = squad_feature_df.merge(hourly_feature, left_on='feature',  right_on='feature', how='left')
        
        output_hourly = merged.groupby(['squad', 'start' ]).aggregate(
        {
                "avaSlo": 'max',                 
                'expSlo': 'max', 
                'latSlo': 'min',
                'ava_prop': 'min',
                'exp_prop': 'min',
                'lat': 'max',
                'ava_debt': 'sum',
                'exp_debt': 'sum',
                'lat_debt': 'sum',
                'ava_budget': 'sum',
                'exp_budget': 'sum',
                'lat_budget': 'sum'
        }).reset_index()        

        output_hourly.replace([np.inf, -np.inf], 0)

        return output_hourly
    
    def __build_group_hourly(self, group_df, hourly_journey):        
        hourly_journey = hourly_journey[['journey', 'start', 'ava_debt', 'exp_debt', 'lat_debt']].copy()
        merged = group_df.merge(hourly_journey, left_on='journey',  right_on='journey', how='left')
        
        output_hourly = merged.groupby(['journey', 'start' ]).aggregate(
        {
                "avaSlo": 'mean',                 
                'expSlo': 'mean', 
                'latSlo': 'mean',
                'ava_debt': 'sum',
                'exp_debt': 'sum',
                'lat_debt': 'sum'
        }).reset_index()
                
        output_hourly.replace([np.inf, -np.inf], 0)

        return output_hourly   

    def execute(self):
        journeys_df =  journeys_to_dataframe(self.system.journeys)
        journeys_features_df = journeys_to_features_dataframe(self.system.journeys)
        features_source_df = features_to_indicators_dataframe(self.system.features)
        sources_df = sources_to_dataframe(self.system.sources)
        squads_df = squads_to_features_dataframe(self.system.squads)

        hourly_source  =self.__build_source_hourly(sources_df)
        hourly_features =  self.__build_features_hourly(features_source_df, hourly_source)
        hourly_journey = self.__build_journeys_hourly(journeys_features_df, hourly_features)
        hourly_groups = self.__build_group_hourly(journeys_df, hourly_journey)

        hourly_squads = self.__build_squad_hourly(squads_df, hourly_features)
        
        
        # __build_journeys_hourly
        return  hourly_groups, hourly_squads, hourly_journey, hourly_features, hourly_source

        

    
    
        
        
        