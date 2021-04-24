from datetime import datetime
from mysql.connector.cursor import MySQLCursorBufferedNamedTuple, RE_SQL_INSERT_STMT
from pandas.core.frame import DataFrame
from sqlalchemy import MetaData, Table, String, Column, Text, DateTime, Boolean, Integer, create_engine, ForeignKey
from sqlalchemy.sql.expression import insert, select
import sqlalchemy
import pandas as pd

from engine.gateways.ORMMetadata import ORMMetadata


class MySqlGateway:

    def __init__(self, user, password, host, port, database) -> None:
        connection = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        self.metadata_engine = create_engine(connection,
                                             strategy='mock', executor=self.__metadata_dump)
        self.engine = create_engine(connection)

    def create_metadata_storage(self):
        ORMMetadata.metadata.drop_all(self.engine)
        ORMMetadata.metadata.create_all(self.metadata_engine)
        ORMMetadata.metadata.create_all(self.engine)

    def health(self):         
         with self.engine.connect() as c:
             c.close()
       

    def __metadata_dump(self, sql, *multiparams, **params):
        pass
        # print(sql.compile(dialect=self.metadata_engine.dialect))

    def post_members(self, values: list):
        if values:
            self.engine.execute(insert(ORMMetadata.members_table), [x.__dict__ for x in values])

    @staticmethod
    def __prepare_no_list(target):
        temp = dict()
        for k, v in target.__dict__.items():
            if not type(v) is list:
                temp[k] = v
        return temp

    def post_squads(self, values: list):
        if values:
            members = list(self.engine.execute(ORMMetadata.members_table.select()).fetchall())
            for item in values:
                r = self.engine.execute(insert(ORMMetadata.squads_table), MySqlGateway.__prepare_no_list(item))
                for m in item.members:
                    member_id = self.__get_member(members, m)
                    ins = ORMMetadata.squads_members_table.insert().values(
                        squadId=r.inserted_primary_key,
                        memberId=member_id)
                    self.engine.execute(ins)

    def post_sources(self, values: list):
        if values:
            for item in values:
                self.engine.execute(insert(ORMMetadata.sources_table), MySqlGateway.__prepare_no_list(item))

    def __get_member(self, members, target):
        try:
            return next(x[0] for x in members if x[2] == target.email)
        except Exception as e:
            raise ValueError(f'member not found {target}') from e

    def post_product(self, value):        
        members = list(self.engine.execute(ORMMetadata.members_table.select()).fetchall())
        r = self.engine.execute(insert(ORMMetadata.products_table), MySqlGateway.__prepare_no_list(value))
        for m in value.leaders:
            member_id = self.__get_member(members, m)
            ins = ORMMetadata.product_members_table.insert().values(
                productId=r.inserted_primary_key,
                memberId=member_id)
            self.engine.execute(ins)

    def post_journeys(self, values: list):
        if values:
            members = list(self.engine.execute(ORMMetadata.members_table.select()).fetchall())
            features = list(self.engine.execute(ORMMetadata.features_table.select()).fetchall())
            
            for item in values:
                r = self.engine.execute(insert(ORMMetadata.journeys_table), MySqlGateway.__prepare_no_list(item))
                for m in item.leaders:
                    member_id = self.__get_member(members, m)
                    ins = ORMMetadata.journey_members_table.insert().values(
                        journeyId=r.inserted_primary_key,
                        memberId=member_id)
                    self.engine.execute(ins)
                for m in item.features:
                    feature_id = next(x[0] for x in features if x[1] == m.feature)
                    ins = ORMMetadata.journey_features_table.insert().values(
                        journeyId=r.inserted_primary_key,
                        featureId=feature_id)
                    self.engine.execute(ins)

    def post_features(self, values: list):
        if values:
            sources = list(self.engine.execute(ORMMetadata.sources_table.select()).fetchall())
            squads = list(self.engine.execute(ORMMetadata.squads_table.select()).fetchall())
            for item in values:
                r = self.engine.execute(insert(ORMMetadata.features_table),
                                        MySqlGateway.__prepare_no_list(item))
                for m in item.squads:
                    squad_id = next(x[0] for x in squads if x[1] == m.squad)
                    ins = ORMMetadata.feature_squads_table.insert().values(
                        featureId=r.inserted_primary_key,
                        squadId=squad_id)
                    self.engine.execute(ins)

                for m in item.sources:
                    source_id = next(x[0] for x in sources if x[1] == m.source)
                    ins = ORMMetadata.feature_sources_table.insert().values(
                        featureId=r.inserted_primary_key,
                        sourceId=source_id)
                    self.engine.execute(ins)

    def post_sourceItems(self, df: DataFrame):
        df.to_sql(name='SourceItems', con=self.engine, if_exists='replace', index=False,
                  dtype={'source': sqlalchemy.types.VARCHAR(length=512)}
                  )

    def post_data(self, df: DataFrame, name, index_names=list()):
        dtype = dict()
        if 'squad' in df.columns:
            dtype['squad'] = sqlalchemy.types.VARCHAR(length=512)
        if 'source' in df.columns:
            dtype['source'] = sqlalchemy.types.VARCHAR(length=512)
        if 'feature' in df.columns:
            dtype['feature'] = sqlalchemy.types.VARCHAR(length=512)
        if 'journey' in df.columns:
            dtype['journey'] = sqlalchemy.types.VARCHAR(length=512)
        df.to_sql(name=name, con=self.engine, if_exists='replace', dtype=dtype, index=False)

        if index_names:
            with self.engine.connect() as con:
                for index in index_names:
                    con.execute(f'CREATE INDEX idx_{name}_{index} ON {name} ({index});')
