from engine.gateways.FileGateway import FileGateway
from engine.core.SystemEntity import SystemEntity


class ShellComponent:
    
    def __init__(self):
        self.file_gateway = FileGateway()
    
    def __load_state(self):
        infrastructure, product, members = self.file_gateway.read_data()
        system = SystemEntity()
        system.load_state(infrastructure, product, members)
        return system    
        
    def run(self):
        system = self.__load_state()
        result = system.generate_app()
        self.file_gateway.write_app(result)




