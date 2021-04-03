import yaml
import pathlib
import os
import pandas as pd


class FileGateway:
    def __init__(self):
        self.dir = pathlib.Path(__file__).parent.absolute()

    def read_data(self, target, nrows=None, hourly_days=None):
        headers = ['source', 'start', 'end', 'total', 'ava', 'exp', 'lat']
        dtype = {
            'total': int,
            'ava': int,
            'exp': int,
            'lat': float
        }
        if nrows:
            df = pd.read_csv(target, sep=";",  names=headers, parse_dates=['start', 'end'], low_memory=False,
                             nrows=nrows, dtype=dtype)
        else:
            df = pd.read_csv(target, sep=";", names=headers,
                             parse_dates=['start', 'end'], low_memory=False, dtype=dtype)

        if df.isnull().values.any():
            raise ValueError('nan in data frame')

        return df

    def read_metadata_v2(self): 
        member_yaml = pathlib.Path(os.path.join(self.dir, './../../data/members.yaml')).absolute()
        members = list()
        with open(member_yaml, 'r') as f:
            data = yaml.load(f, yaml.FullLoader)            
            for item in list(data):
                members.append(item['email'], item['name'], item['nickname'])
        
        return pd.DataFrame(members, columns=['email', 'name', 'nickname'])
        

    def read_metadata(self):
        member_yaml = pathlib.Path(os.path.join(self.dir, './../../data/members.yaml')).absolute()
        members = list()
        with open(member_yaml, 'r') as f:
            data = yaml.load(f, yaml.FullLoader)
            members = list(data)            
             

        squad_yaml = pathlib.Path(os.path.join(self.dir, './../../data/squads.yaml')).absolute()
        squads = list()
        with open(squad_yaml, 'r') as f:
            data = yaml.load(f, yaml.FullLoader)
            squads = list(data)                         

        system_yaml = pathlib.Path(os.path.join(self.dir, './../../data/system.yaml')).absolute()        
        with open(system_yaml, 'r') as f:
            data = yaml.load(f, yaml.FullLoader)    
            data = list(data)                       
            infra = data[0]

        target = pathlib.Path(os.path.join(self.dir, './../../data/product.yaml')).absolute()
        with open(target, 'r') as f:
            data = yaml.load_all(f, yaml.FullLoader)
            data = list(data)            
            product = data[0][0]                        
            journeys = data[1]
            features = data[2]
            return infra, product, members, squads, journeys, features

    def write_app(self, state):
        target = os.path.join(self.dir, './../../wip/docker-compose.yaml')
        with open(target, 'w') as f:
            yaml.dump(state, f)
