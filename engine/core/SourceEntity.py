from typing import List
import pandas as pd

class SourceEntity: 
    def __init__(self) -> None:
        self.source = None
        self.features = list()
        self.avaSlo = 0
        self.expSlo = 0
        self.latSlo = 0
        self.avaSla = 0
        self.latSla = 0

    def measure_slo(self):
        if not self.features:
            raise ValueError('Source without feature: {}'.format(self.source))
        self.avaSlo = max([x.avaSlo for x in self.features])
        self.latSlo = min([x.latSlo for x in self.features])
        self.expSlo = max([x.expSlo for x in self.features])
        self.avaSla = max([x.avaSla for x in self.features])
        self.latSla = min([x.latSla for x in self.features])


def sources_to_dataframe(items: List[SourceEntity]):
    data = list()
    for item in items:
        data.append([item.source, item.avaSlo, item.expSlo, item.latSlo])
    return pd.DataFrame(data, columns=['source', 'avaSlo', 'expSlo', 'latSlo'])
