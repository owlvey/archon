from sqlalchemy import MetaData, Table, String, Column, Text, DateTime, Boolean, Integer, create_engine, ForeignKey
from sqlalchemy.sql.sqltypes import Float


class ORMMetadata:
    metadata = MetaData()

    products_table = Table('Products', metadata,
                           Column('id', Integer(), primary_key=True),
                           Column('product', String(512), nullable=False),
                           Column('description', String(512), nullable=False),
                           Column('latency_percentile', Float(), nullable=False),
                           )

    members_table = Table('Members', metadata,
                          Column('id', Integer(), primary_key=True),
                          Column('name', String(512), nullable=False),
                          Column('email', String(512), nullable=False),
                          Column('nickname', String(512), nullable=False),
                          )

    sources_table = Table('Sources', metadata,
                          Column('id', Integer(), primary_key=True),
                          Column('source', String(1024), nullable=False),
                          Column('avaSlo', Float(), nullable=False),
                          Column('expSlo', Float(), nullable=False),
                          Column('latSlo', Float(), nullable=False)
                          )

    squads_table = Table('Squads', metadata,
                         Column('id', Integer(), primary_key=True),
                         Column('squad', String(512), nullable=False)
                         )
    journeys_table = Table('Journeys', metadata,
                           Column('id', Integer(), primary_key=True),
                           Column('journey', String(512), nullable=False),
                           Column('description', String(512), nullable=False),
                           Column('family', String(512), nullable=False),
                           Column('avaSlo', Float(), nullable=False),
                           Column('expSlo', Float(), nullable=False),
                           Column('latSlo', Float(), nullable=False),
                           Column('avaSla', Float(), nullable=False),
                           Column('latSla', Float(), nullable=False),
                           )

    product_members_table = Table('ProductLeaders', metadata,
                                  Column('productId', Integer(), ForeignKey("Products.id")),
                                  Column('memberId', Integer(), ForeignKey("Members.id"))
                                  )

    journey_members_table = Table('JourneyLeaders', metadata,
                                  Column('journeyId', Integer(), ForeignKey("Journeys.id")),
                                  Column('memberId', Integer(), ForeignKey("Members.id"))
                                  )

    journey_features_table = Table('JourneyFeatures', metadata,
                                  Column('journeyId', Integer(), ForeignKey("Journeys.id")),
                                  Column('featureId', Integer(), ForeignKey("Features.id"))
                                  )

    squads_members_table = Table('SquadMembers', metadata,
                                 Column('squadId', Integer(), ForeignKey("Squads.id")),
                                 Column('memberId', Integer(), ForeignKey("Members.id"))
                                 )

    features_table = Table('Features', metadata,
                           Column('id', Integer(), primary_key=True),
                           Column('feature', String(512), nullable=False),
                           Column('description', String(512), nullable=False),
                           Column('avaSlo', Float(), nullable=False),
                           Column('expSlo', Float(), nullable=False),
                           Column('latSlo', Float(), nullable=False)
                           )

    feature_squads_table = Table('FeatureSquads', metadata,
                                 Column('featureId', Integer(), ForeignKey("Features.id")),
                                 Column('squadId', Integer(), ForeignKey("Squads.id")),
                                 )

    feature_sources_table = Table('FeatureSources', metadata,
                                  Column('featureId', Integer(), ForeignKey("Features.id")),
                                  Column('sourceId', Integer(), ForeignKey("Sources.id")),
                                  )