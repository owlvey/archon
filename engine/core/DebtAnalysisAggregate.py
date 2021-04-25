from numpy.lib.financial import nper
from pandas.core.frame import DataFrame
from engine.core.SystemEntity import SystemEntity
from engine.core.JourneyEntity import journeys_to_features_sources_dataframe
from engine.core.SourceEntity import sources_to_dataframe
from engine.core.SquadEntity import squads_to_features_dataframe
from engine.core.FeatureEntity import features_to_indicators_dataframe
import pandas as pd
import numpy as np
import statistics
from datetime import  datetime, timedelta


class DebtAnalysisAggregate:
    def __init__(self, data: DataFrame, system: SystemEntity) -> None:
        self.system = system
        self.data = data

    @staticmethod
    def __measure_debt(output_hourly):
        output_hourly['ava_debt'] = output_hourly.apply(
            lambda x: 0 if x['ava_prop'] >= x['avaSlo'] else x['avaSlo'] - x['ava_prop'], axis=1)
        output_hourly['exp_debt'] = output_hourly.apply(
            lambda x: 0 if x['exp_prop'] >= x['expSlo'] else x['expSlo'] - x['exp_prop'], axis=1)
        output_hourly['lat_debt'] = output_hourly.apply(
            lambda x: 0 if x['lat'] <= x['latSlo'] else x['lat'] - x['latSlo'], axis=1)

    def __build_source_monthly(self):
        anchor = datetime.now() - timedelta(days=self.system.infrastructure.hourly_days)
        corpus = self.data

        output_hourly = corpus.groupby(
            [pd.Grouper(key='start', freq='M'), 'source']).agg({
                'total': 'sum',
                'ava': 'sum',
                'exp': 'sum',
                'lat': 'mean'}).reset_index()

        output_hourly['ava_prop'] = output_hourly['ava'].divide(output_hourly['total'])
        output_hourly['exp_prop'] = output_hourly['exp'].divide(output_hourly['total'])

        output_hourly.replace([np.inf, -np.inf], 0)

        return output_hourly.reset_index()

    def execute(self):
        journeys_features_sources_df = journeys_to_features_sources_dataframe(self.system.journeys)
        features_source_df = features_to_indicators_dataframe(self.system.features)
        sources_df = sources_to_dataframe(self.system.sources)
        squads_features_df = squads_to_features_dataframe(self.system.squads)

        base_source = self.__build_source_monthly()
        monthly_source = sources_df.merge(base_source, left_on='source', right_on='source', how='inner').copy()
        DebtAnalysisAggregate.__measure_debt(monthly_source)

        monthly_features = features_source_df.merge(base_source, left_on='source', right_on='source', how='inner').copy()
        DebtAnalysisAggregate.__measure_debt(monthly_features)

        monthly_squads = squads_features_df.merge(monthly_features, left_on='feature', right_on='feature', how='inner')

        monthly_journey = journeys_features_sources_df.merge(base_source,
                                                             left_on='source', right_on='source', how='inner').copy()
        DebtAnalysisAggregate.__measure_debt(monthly_journey)

        monthly_journey.fillna(0)
        monthly_squads.fillna(0)
        monthly_features.fillna(0)
        monthly_source.fillna(0)

        return monthly_squads, monthly_journey, monthly_features, monthly_source

    @staticmethod
    def mean_x(values):
        if values is None or len(values) == 0:
            return 0        
        temp = [y for y in values if y > 0]
        if not temp: 
            return 0
        return statistics.mean(temp)
        

    @staticmethod
    def generate_monthly_pivot(key_column, metric, monthly_data: pd.DataFrame):
        target = monthly_data.copy()
        target['start'] = target['start'].dt.strftime('%Y-%m')
        # use only debt values 
        monthly_pivot = target.groupby([key_column, 'start']).agg(
            { metric: DebtAnalysisAggregate.mean_x } ).reset_index().pivot(
            index=key_column, columns='start', values=metric
        ).reset_index().fillna(0).reset_index()
        names = list(monthly_pivot.columns)
        names.remove(key_column)
        names.remove('index')
        names = [key_column] + sorted(list(names))[-12:]
        return monthly_pivot[names]

    @staticmethod
    def generate_monthly_family_ava_pivot(monthly_journey: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('family', 'ava_debt', monthly_journey)

    @staticmethod
    def generate_monthly_family_exp_pivot(monthly_journey: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('family', 'exp_debt', monthly_journey)

    @staticmethod
    def generate_monthly_family_lat_pivot(monthly_journey: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('family', 'lat_debt', monthly_journey)

    @staticmethod
    def generate_monthly_journey_ava_pivot(monthly_journey: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('journey', 'ava_debt', monthly_journey)

    @staticmethod
    def generate_monthly_journey_exp_pivot(monthly_journey: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('journey', 'exp_debt', monthly_journey)

    @staticmethod
    def generate_monthly_journey_lat_pivot(monthly_journey: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('journey', 'lat_debt', monthly_journey)

    @staticmethod
    def generate_monthly_feature_ava_pivot(monthly_feature: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('feature', 'ava_debt', monthly_feature)

    @staticmethod
    def generate_monthly_feature_exp_pivot(monthly_feature: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('feature', 'exp_debt', monthly_feature)

    @staticmethod
    def generate_monthly_feature_lat_pivot(monthly_feature: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('feature', 'lat_debt', monthly_feature)

    @staticmethod
    def generate_monthly_squad_ava_pivot(monthly_squad: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('squad', 'ava_debt', monthly_squad)

    @staticmethod
    def generate_monthly_squad_exp_pivot(monthly_squad: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('squad', 'exp_debt', monthly_squad)

    @staticmethod
    def generate_monthly_squad_lat_pivot(monthly_squad: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('squad', 'lat_debt', monthly_squad)

    @staticmethod
    def generate_monthly_source_ava_pivot(monthly_source: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('source', 'ava_debt', monthly_source)

    @staticmethod
    def generate_monthly_source_exp_pivot(monthly_source: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('source', 'exp_debt', monthly_source)

    @staticmethod
    def generate_monthly_source_lat_pivot(monthly_source: pd.DataFrame):
        return DebtAnalysisAggregate.generate_monthly_pivot('source', 'lat_debt', monthly_source)

