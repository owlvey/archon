
from engine.core.DebtAnalysisAggregate import DebtAnalysisAggregate
import unittest
import pandas as pd


class DebtAnalysisAggregateTest(unittest.TestCase):

    def test_generate_monthly_pivot(self):        
        r = DebtAnalysisAggregate.mean_x(pd.Series([0, 6, 4 , 0]))
        self.assertEquals(5, r)
        r = DebtAnalysisAggregate.mean_x(pd.Series([6, 4 ]))
        self.assertEquals(5, r)
        r = DebtAnalysisAggregate.mean_x(pd.Series([]))
        self.assertEquals(0, r)
        r = DebtAnalysisAggregate.mean_x(pd.Series([0]))
        self.assertEquals(0, r)
        r = DebtAnalysisAggregate.mean_x(pd.Series([1]))
        self.assertEquals(1, r)
        r = DebtAnalysisAggregate.mean_x(pd.Series([0.5, 0.5]))
        self.assertEquals(0.5, r)

