from engine.core.MetadataAggregate import MetadataAggregate
from engine.core.graphs.DebtGraphAnalysisAggregate import DebtGraphAnalysisAggregate
from engine.core.DebtAnalysisAggregate import DebtAnalasysAggregate
from engine.gateways.MySqlGateway import MySqlGateway
from engine.gateways.FileGateway import FileGateway
from engine.core.SystemEntity import SystemEntity
import pandas as pd
import json


class ShellComponent:
    
    def __init__(self):
        self.system_entity = None
        self.states_gateways = list()        
        self.file_gateway = FileGateway()
    
    def __load_state(self):
        infrastructure, product, members, squads, journeys, features = self.file_gateway.read_metadata()
        self.system_entity = SystemEntity()
        self.system_entity.load_state(infrastructure, product, members, squads, journeys, features)        
    
    def __create_infrastructure(self):
        visual = self.system_entity.infrastructure.visualizations[0]        

        for item in self.system_entity.infrastructure.states:                        
            self.states_gateways.append(                              
                MySqlGateway(item['user'], item['password'], item['host'], item['port'], item['database'])
            )               
         
        
    def __save_metadata(self):        
        for gateway in self.states_gateways:
            # members first
            gateway.post_members(self.system_entity.members)
            gateway.post_product(self.system_entity.product)
            gateway.post_squads(self.system_entity.squads)
            gateway.post_journeys(self.system_entity.journeys)            
            gateway.post_sources(self.system_entity.sources)
            gateway.post_features(self.system_entity.features)

    
    def __save_data(self):        
        dfs = list()
        for item in self.system_entity.infrastructure.sinks:
            df = self.file_gateway.read_data(item['target'])
            dfs.append(df)
        df = pd.concat(dfs)
        for gateway in self.states_gateways:
            gateway.post_sourceItems(df)
        
        return df
            
    def run(self):
        self.__load_state()
        self.__create_infrastructure()       
        for gateway in self.states_gateways:
            gateway.create_metadata_storage()
        
        self.__save_metadata()

        data = self.__save_data()

        agg = DebtAnalasysAggregate(data, self.system_entity)
        groups_hourly, squad_hourly, journey_hourly, hourly_feature, hourly_source = agg.execute()

        meta_agg = MetadataAggregate(self.system_entity)
        metadata_journey_features, metadata_feature_sources = meta_agg.execute()

        graph =  DebtGraphAnalysisAggregate(self.system_entity, hourly_source)
        feature_source_graph = graph.execute()

        for gateway in self.states_gateways:            
            gateway.post_data(journey_hourly, 'HourlyJourney')
            gateway.post_data(hourly_feature, 'HourlyFeature')
            gateway.post_data(hourly_source, 'HourlySource')
            gateway.post_data(squad_hourly, 'HourlySquad')
            gateway.post_data(groups_hourly, 'HourlyGroup')           
            gateway.post_data(feature_source_graph, 'GraphFeatureSource')                       
            gateway.post_data(metadata_feature_sources, 'FeatureSourcesMap')
            gateway.post_data(metadata_journey_features, 'JourneyFeaturesMap')
        

