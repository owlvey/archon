from engine.core.DebtHourlyAnalysisAggregate import DebtHourlyAnalysisAggregate
from engine.core.MetadataAggregate import MetadataAggregate
from engine.core.graphs.DebtGraphAnalysisAggregate import DebtGraphAnalysisAggregate
from engine.core.DebtAnalysisAggregate import DebtAnalysisAggregate
from engine.gateways.FileStateGateway import FileStateGateway
from engine.gateways.MySqlGateway import MySqlGateway
from engine.gateways.FileGateway import FileGateway
from engine.core.SystemEntity import SystemEntity
import pandas as pd
import sys
import json


class ShellComponent:
    
    def __init__(self):
        self.system_entity = SystemEntity()
        self.states_gateways = list()        
        self.file_gateway = FileGateway()
    
    def __create_infrastructure(self):
        visual = self.system_entity.infrastructure.visualizations[0]        
        for item in self.system_entity.infrastructure.states:
            if item['type'] == 'mysql':
                self.states_gateways.append(
                    MySqlGateway(item['user'], item['password'], item['host'], item['port'], item['database'])
                )
            elif item['type'] == 'filestate':
                self.states_gateways.append(FileStateGateway())
            else:
                raise ValueError('state not found')

    def __load_state(self):
        infrastructure, product, members, squads, journeys, features = self.file_gateway.read_metadata()
        self.system_entity.load_state(infrastructure, product, members, squads, journeys, features)        
    
    
        
    def __save_metadata(self):        
        for gateway in self.states_gateways:
            # members first
            gateway.post_members(self.system_entity.members)
            gateway.post_product(self.system_entity.product)
            gateway.post_squads(self.system_entity.squads)
            gateway.post_sources(self.system_entity.sources)
            gateway.post_features(self.system_entity.features)
            gateway.post_journeys(self.system_entity.journeys)            
            
    
    def __load_data(self):
        dfs = list()
        for item in self.system_entity.infrastructure.sinks:
            
            nrows = sys.maxsize
            if 'nrows' in item:
                nrows = int(item['nrows'])
            df = self.file_gateway.read_data(item['target'], nrows)
            dfs.append(df)
        df = pd.concat(dfs)
        return df
            
    def run(self):
        self.__load_state()
        self.__create_infrastructure()       
        for gateway in self.states_gateways:
            gateway.create_metadata_storage()

        self.system_entity.measure_slo()

        self.__save_metadata()

        meta_agg = MetadataAggregate(self.system_entity)
        metadata_journey_features, metadata_feature_sources = meta_agg.execute()

        data = self.__load_data()
        # measure slo per period

        agg_slo = DebtAnalysisAggregate(data, self.system_entity)
        monthly_squads, monthly_journey, monthly_features, monthly_source = agg_slo.execute()

        for gateway in self.states_gateways:
            gateway.post_data(monthly_journey, 'MonthlyJourney', index_names=['journey', 'feature', 'source', 'start'])
            gateway.post_data(monthly_features, 'MonthlyFeature', index_names=['feature', 'source', 'start'])
            gateway.post_data(monthly_source, 'MonthlySource', index_names=['source', 'start'])
            gateway.post_data(monthly_squads, 'MonthlySquad', index_names=['squad', 'feature', 'source', 'start'])
            gateway.post_data(DebtAnalysisAggregate.generate_monthly_family_ava_pivot(monthly_journey),
                              'MonthlyAvaDebtGroupPivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_family_exp_pivot(monthly_journey),
                              'MonthlyExpDebtGroupPivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_family_lat_pivot(monthly_journey),
                              'MonthlyLatDebtGroupPivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_journey_ava_pivot(monthly_journey),
                              'MonthlyAvaDebtJourneyPivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_journey_exp_pivot(monthly_journey),
                              'MonthlyExpDebtJourneyPivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_journey_lat_pivot(monthly_journey),
                              'MonthlyLatDebtJourneyPivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_feature_ava_pivot(monthly_features),
                              'MonthlyAvaDebtFeaturePivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_feature_exp_pivot(monthly_features),
                              'MonthlyExpDebtFeaturePivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_feature_lat_pivot(monthly_features),
                              'MonthlyLatDebtFeaturePivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_squad_ava_pivot(monthly_squads),
                              'MonthlyAvaDebtSquadPivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_squad_exp_pivot(monthly_squads),
                              'MonthlyExpDebtSquadPivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_squad_lat_pivot(monthly_squads),
                              'MonthlyLatDebtSquadPivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_source_ava_pivot(monthly_source),
                              'MonthlyAvaDebtSourcePivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_source_exp_pivot(monthly_source),
                              'MonthlyExpDebtSourcePivot')

            gateway.post_data(DebtAnalysisAggregate.generate_monthly_source_lat_pivot(monthly_source),
                              'MonthlyLatDebtSourcePivot')

            gateway.post_data(metadata_feature_sources, 'FeatureSourcesMap')
            gateway.post_data(metadata_journey_features, 'JourneyFeaturesMap')

        # measure slo by hourly with warning zone enabled
        self.system_entity.apply_warning_zone()
        self.system_entity.measure_slo()
        agg = DebtHourlyAnalysisAggregate(data, self.system_entity)
        squad_hourly, journey_hourly, hourly_feature, hourly_source = agg.execute()

        graph = DebtGraphAnalysisAggregate(self.system_entity, hourly_source)
        feature_source_graph = graph.execute()

        for gateway in self.states_gateways:            
            gateway.post_data(journey_hourly, 'HourlyJourney', index_names=['journey', 'feature', 'source', 'start'])
            gateway.post_data(hourly_feature, 'HourlyFeature', index_names=['feature', 'source', 'start'])
            gateway.post_data(hourly_source, 'HourlySource', index_names=['source', 'start'])
            gateway.post_data(squad_hourly, 'HourlySquad',  index_names=['squad', 'feature', 'source', 'start'])
            gateway.post_data(metadata_feature_sources, 'FeatureSourcesMap')
            gateway.post_data(metadata_journey_features, 'JourneyFeaturesMap')
        

