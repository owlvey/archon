from engine.core.SystemEntity import SystemEntity
from engine.core.FeatureEntity import features_to_indicators_dataframe
from engine.core.JourneyEntity import journeys_to_features_dataframe


class MetadataAggregate:
    def __init__(self, system: SystemEntity) -> None:
        self.system = system

    def execute(self): 
        indicators = features_to_indicators_dataframe(self.system.features)
        journey_feature = journeys_to_features_dataframe(self.system.journeys)
        return journey_feature, indicators
        