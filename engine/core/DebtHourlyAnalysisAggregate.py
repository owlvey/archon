from numpy.lib.financial import nper
from pandas.core.frame import DataFrame
from engine.core.SystemEntity import SystemEntity
from engine.core.JourneyEntity import journeys_to_features_sources_dataframe
from engine.core.SourceEntity import sources_to_dataframe
from engine.core.SquadEntity import squads_to_features_dataframe
from engine.core.FeatureEntity import features_to_indicators_dataframe
import pandas as pd
import numpy as np
from datetime import  datetime, timedelta


class DebtHourlyAnalysisAggregate:
    def __init__(self, data: DataFrame, system: SystemEntity) -> None:
        self.system = system
        self.data = data

    @staticmethod
    def __measure_debt(output_hourly):
        output_hourly['ava_debt'] = 0
        output_hourly['exp_debt'] = 0
        output_hourly['lat_debt'] = 0
        if output_hourly.empty:
            return

        output_hourly['ava_debt'] = output_hourly.apply(
            lambda x: 0 if x['ava_prop'] >= x['avaSlo'] else x['avaSlo'] - x['ava_prop'], axis=1)
        output_hourly['exp_debt'] = output_hourly.apply(
            lambda x: 0 if x['exp_prop'] >= x['expSlo'] else x['expSlo'] - x['exp_prop'], axis=1)
        output_hourly['lat_debt'] = output_hourly.apply(
            lambda x: 0 if x['lat'] <= x['latSlo'] else x['lat'] - x['latSlo'], axis=1)

    def __build_source_hourly(self):
        anchor = self.data['start'].max() - timedelta(days=self.system.infrastructure.hourly_days)
        corpus = self.data[self.data['start'] >= anchor].copy()

        output_hourly = corpus.groupby(
            [pd.Grouper(key='start', freq='H'), 'source']).agg({
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

        base_source = self.__build_source_hourly()
        hourly_source = sources_df.merge(base_source, left_on='source', right_on='source', how='inner').copy()
        DebtHourlyAnalysisAggregate.__measure_debt(hourly_source)

        hourly_features = features_source_df.merge(base_source, left_on='source', right_on='source', how='inner').copy()
        DebtHourlyAnalysisAggregate.__measure_debt(hourly_features)

        hourly_squads = squads_features_df.merge(hourly_features, left_on='feature', right_on='feature', how='inner')

        hourly_journey = journeys_features_sources_df.merge(base_source,
                                                            left_on='source', right_on='source', how='inner').copy()
        DebtHourlyAnalysisAggregate.__measure_debt(hourly_journey)

        hourly_journey.fillna(0)
        hourly_squads.fillna(0)
        hourly_features.fillna(0)
        hourly_source.fillna(0)

        return hourly_squads, hourly_journey, hourly_features, hourly_source
