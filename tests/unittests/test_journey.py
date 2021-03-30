from engine.core.StateUtil import StateUtil
from engine.core.JourneyEntity import JourneyEntity, journeys_to_dataframe
import unittest


class JourneyUnitTest(unittest.TestCase):

    def test_dataframe(self):
        journey = JourneyEntity()
        journey.journey = 'test'
        journey.family = 'test'
        journey.avaSlo = 0.99
        journey.expSlo = 0.99
        journey.latSlo = 2000

        df = journeys_to_dataframe([journey])

        print(df.info())


