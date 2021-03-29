from engine.gateways.MySqlGateway import MySqlGateway
from engine.gateways.FileGateway import FileGateway
from engine.core.SystemEntity import SystemEntity


class ShellComponent:
    
    def __init__(self):
        self.system_entity = None
        self.states_gateways = list()
        self.file_gateway = FileGateway()
    
    def __load_state(self):
        infrastructure, product, members, squads, journeys, features = self.file_gateway.read_data()
        self.system_entity = SystemEntity()
        self.system_entity.load_state(infrastructure, product, members, squads, journeys, features)        
    
    def __create_infrastructure(self):
        for item in self.system_entity.infrastructure.states:
            self.states_gateways.append(                
                MySqlGateway(item['connection'])
            )        
        
    def __save_metadata(self):        
        for gateway in self.states_gateways:
            gateway.post_members(self.system_entity.members)
            gateway.post_squads(self.system_entity.squads)
            gateway.post_journeys(self.system_entity.journeys)            
            gateway.post_sources(self.system_entity.get_sources())
            gateway.post_features(self.system_entity.features)
        
    def run(self):
        self.__load_state()
        self.__create_infrastructure()       
        for gateway in self.states_gateways:
            gateway.create_metadata_storage()
        
        self.__save_metadata()
        
        
        




