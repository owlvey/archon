import yaml
import pathlib
import os
import pandas as pd



class FileStateGateway:
    def __init__(self):
        self.dir = pathlib.Path(__file__).parent.absolute()

    def create_metadata_storage(self):
        pass

    def __metadata_dump(self, sql, *multiparams, **params):
        pass
        # print(sql.compile(dialect=self.metadata_engine.dialect))

    def post_members(self, values: list):
        pass

    def post_squads(self, values: list):
        pass

    def post_sources(self, values: list):
        pass

    def post_product(self, value):
        pass

    def post_journeys(self, values: list):
        pass

    def post_features(self, values: list):
        pass

    def post_sourceItems(self, df: pd.DataFrame):
        pass

    def post_data(self, df: pd.DataFrame, name, index_names=list()):
        target = os.path.join(self.dir, f'./../../wip/{name}.yaml')
        df.to_csv(target, index=False)



    
    