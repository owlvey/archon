from engine.core.DebtAnalysisAggregate import DebtAnalasysAggregate
from engine.gateways.GrafanaGateway import GrafanaGateway
from engine.gateways.MySqlGateway import MySqlGateway
from engine.gateways.FileGateway import FileGateway
from engine.core.SystemEntity import SystemEntity
import pandas as pd
import json


class ShellComponent:
    
    def __init__(self):
        self.system_entity = None
        self.states_gateways = list()
        self.grafana_gateway = None
        self.file_gateway = FileGateway()
    
    def __load_state(self):
        infrastructure, product, members, squads, journeys, features = self.file_gateway.read_metadata()
        self.system_entity = SystemEntity()
        self.system_entity.load_state(infrastructure, product, members, squads, journeys, features)        
    
    def __create_infrastructure(self):
        visual = self.system_entity.infrastructure.visualizations[0]
        self.grafana_gateway = GrafanaGateway(visual['host'], visual['user'], visual['password'])

        for item in self.system_entity.infrastructure.states:                        
            self.states_gateways.append(                              
                MySqlGateway(item['user'], item['password'], item['host'], item['port'], item['database'])
            )   
            self.grafana_gateway.create_datasource(item['user'], item['password'], item['host'], item['port'], item['database'], item['type'])
         
        
    def __save_metadata(self):        
        for gateway in self.states_gateways:
            # members first
            gateway.post_members(self.system_entity.members)
            gateway.post_product(self.system_entity.product)
            gateway.post_squads(self.system_entity.squads)
            gateway.post_journeys(self.system_entity.journeys)            
            gateway.post_sources(self.system_entity.sources)
            gateway.post_features(self.system_entity.features)

    def __generate_visualizations(self):
        self.grafana_gateway.create_folder('journeys')
        self.grafana_gateway.create_folder('features')
        self.grafana_gateway.create_folder('squads')
        self.grafana_gateway.create_folder('sources')

        folders = self.grafana_gateway.get_folders()
        for folder in folders:
            if folder['title']  == "sources":

                 with open('/Users/Gregory/owlvey/archon/engine/dashboards/sources/overview.json', 'r') as f:                    
                    dashboard = json.load(f)
                    del dashboard['uid']
                    del dashboard['version']
                    del dashboard['id']
                    self.grafana_gateway.create_dashboard(folder['id'],dashboard)
    
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
        report = agg.execute()

        for gateway in self.states_gateways:
            gateway.post_data(report, 'SourceDaily')

        self.__generate_visualizations()
        
        
        




