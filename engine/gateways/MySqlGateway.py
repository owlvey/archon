from datetime import datetime
from mysql.connector.cursor import MySQLCursorBufferedNamedTuple, RE_SQL_INSERT_STMT
from sqlalchemy import MetaData, Table, String, Column, Text, DateTime, Boolean, Integer, create_engine, ForeignKey
import mysql.connector
from sqlalchemy.sql.expression import insert, select
from sqlalchemy.sql.sqltypes import Float


class MySqlGateway:

    metadata = MetaData()

    members_table = Table('Members', metadata, 
        Column('id', Integer(), primary_key=True),
        Column('name', String(512), nullable=False),
        Column('email', String(512), nullable=False),    
    )

    sources_table = Table('Sources', metadata, 
        Column('id', Integer(), primary_key=True),
        Column('source', String(1024), nullable=False)        
    )

    squads_table = Table('Squads', metadata, 
        Column('id', Integer(), primary_key=True),
        Column('squad', String(512), nullable=False)        
    )
    journeys_table = Table('Journeys', metadata, 
        Column('id', Integer(), primary_key=True),
        Column('journey', String(512), nullable=False),
        Column('description', String(512), nullable=False),
        Column('group', String(512), nullable=False), 
        Column('avaSlo', Float(), nullable=False),
        Column('expSlo', Float(), nullable=False),
        Column('latSlo', Float(), nullable=False),
        Column('avaSla', Float(), nullable=False),
        Column('latSla', Float(), nullable=False),
    )
    
    journey_members_table = Table('JourneyMembers', metadata, 
        Column('journeyId', Integer(), ForeignKey("Journeys.id")),
        Column('memberId', Integer(),  ForeignKey("Members.id"))        
    )

    squads_members_table = Table('SquadMembers', metadata, 
        Column('squadId', Integer(), ForeignKey("Squads.id")),
        Column('memberId', Integer(),  ForeignKey("Members.id"))        
    )

    features_table = Table('Features', metadata, 
        Column('id', Integer(), primary_key=True),
        Column('feature', String(512), nullable=False),
        Column('description', String(512), nullable=False),        
    )

    feature_squads_table = Table('FeatureSquads', metadata, 
        Column('featureId', Integer(),  ForeignKey("Features.id")),        
        Column('squadId', Integer(), ForeignKey("Squads.id")),        
    )

    feature_sources_table = Table('FeatureSources', metadata, 
        Column('featureId', Integer(),  ForeignKey("Features.id")),        
        Column('sourceId', Integer(), ForeignKey("Sources.id")),        
    )

    def __init__(self, connection) -> None:        
        self.metadata_engine = create_engine(connection, 
            strategy='mock', executor = self.__metadata_dump)        
        self.engine = create_engine(connection)        

    def create_metadata_storage(self):        
        MySqlGateway.metadata.drop_all(self.engine)
        MySqlGateway.metadata.create_all(self.metadata_engine)        
        MySqlGateway.metadata.create_all(self.engine)        
    
    def __metadata_dump(self, sql, *multiparams, **params):
        print(sql.compile(dialect=self.metadata_engine.dialect))           
    
    def post_members(self, values: list):
        if values:            
            self.engine.execute(insert(MySqlGateway.members_table), [x.__dict__ for x in values])
    
    @staticmethod
    def __prepare_no_list(target):    
        temp = dict()
        for k, v in target.__dict__.items():
            if not type(v) is list : 
                temp[k] = v
        return temp
    
    def post_squads(self, values: list):
        if values:            
            members = list(self.engine.execute(MySqlGateway.members_table.select()).fetchall())
            for item in values:
                r = self.engine.execute(insert(MySqlGateway.squads_table), MySqlGateway.__prepare_no_list(item))
                for m in item.members:
                    member_id = next(x[0] for x in members if x[2] == m)         
                    ins = MySqlGateway.squads_members_table.insert().values(
                         squadId = r.inserted_primary_key, 
                         memberId = member_id)           
                    self.engine.execute(ins)                                
           
    
    def post_sources(self, values: list):
        if values:            
            self.engine.execute(insert(MySqlGateway.sources_table), [ { "source": x} for x in values])
    
    def post_journeys(self, values: list):
        if values:            
            members = list(self.engine.execute(MySqlGateway.members_table.select()).fetchall())
            for item in values:
                r = self.engine.execute(insert(MySqlGateway.journeys_table), MySqlGateway.__prepare_no_list(item))
                for m in item.leaders:
                    member_id = next(x[0] for x in members if x[2] == m)         
                    ins = MySqlGateway.journey_members_table.insert().values(
                         journeyId = r.inserted_primary_key, 
                         memberId = member_id)           
                    self.engine.execute(ins)             

            

    def post_features(self, values: list):
        if values:            
            sources = list(self.engine.execute(MySqlGateway.sources_table.select()).fetchall())
            squads = list(self.engine.execute(MySqlGateway.squads_table.select()).fetchall())
            for item in values:
                r = self.engine.execute(insert(MySqlGateway.features_table), 
                        MySqlGateway.__prepare_no_list(item))
                for m in item.squads:
                    squad_id = next(x[0] for x in squads if x[1] == m)         
                    ins = MySqlGateway.feature_squads_table.insert().values(
                         featureId = r.inserted_primary_key, 
                         squadId = squad_id)           
                    self.engine.execute(ins)         

                for m in item.sources:
                    source_id = next(x[0] for x in sources if x[1] == m)         
                    ins = MySqlGateway.feature_sources_table.insert().values(
                         featureId = r.inserted_primary_key, 
                         sourceId = source_id)           
                    self.engine.execute(ins)             

            

    def post_products(self, values: list):
        mydb = self.__create_connection()
        try:
            cursor = mydb.cursor()    
            sql = "INSERT INTO DynatraceEntries (source, start, end, total, availability, experience, latency) VALUES (%s, %s, %s, %s, %s, %s, %s)"            
            for val in values:
                cursor.execute(sql, val.to_tuple())  
            mydb.commit()
        finally:
            try:
                if cursor:
                    cursor.close()
            finally:
                pass
            mydb.close()
