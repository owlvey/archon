import yaml
import pathlib
import os
import pandas as pd
from os import listdir
from os.path import isfile, join
import  sys


class FileGateway:
    def __init__(self):        
        self.system_yaml = self.__get_system()

    # read from env or system.yaml or fail
    def __get_system(self):
        system_path = os.environ.get('OWLVEY_CONFIG', None)
        if system_path:
            return system_path            
        else:   
            return pathlib.Path(os.path.join(pathlib.Path(__file__).parent.absolute(), './../../system.yaml')).absolute()

    def read_data(self, target, nrows=None, hourly_days=None):
        headers = ['source', 'start', 'end', 'total', 'ava', 'exp', 'lat']
        dtype = dict(total=int, ava=int, exp=int, lat=float)

        onlyfiles = [f for f in listdir(target) if isfile(join(target, f))]
        temp = list()
        for file in onlyfiles:
            nrows = sys.maxsize
            df = pd.read_csv(join(target, file), sep=";",
                             names=headers, parse_dates=['start', 'end'],
                             low_memory=False,
                             nrows=nrows, dtype=dtype)
            temp.append(df)
        df = pd.concat(temp)

        if df.isnull().values.any():
            raise ValueError('nan in data frame')

        return df

    def read_metadata(self):
        with open(self.system_yaml, 'r') as f:
            data = yaml.load(f, yaml.FullLoader)    
            data = list(data)                       
            infra = data[0]
            metadata_dir = infra['metadata']['target']

        member_yaml = pathlib.Path(os.path.join(metadata_dir, 'members.yaml')).absolute()
        members = list()
        with open(member_yaml, 'r') as f:
            data = yaml.load(f, yaml.FullLoader)
            members = list(data)

        squad_yaml = pathlib.Path(os.path.join(metadata_dir, 'squads.yaml')).absolute()
        squads = list()
        with open(squad_yaml, 'r') as f:
            data = yaml.load(f, yaml.FullLoader)
            squads = list(data)                         

        target = pathlib.Path(os.path.join(metadata_dir, 'product.yaml')).absolute()
        with open(target, 'r') as f:
            data = yaml.load_all(f, yaml.FullLoader)
            data = list(data)            
            product = data[0][0]                        
            journeys = data[1]
            features = data[2]
            return infra, product, members, squads, journeys, features   
