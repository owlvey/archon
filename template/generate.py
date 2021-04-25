from datetime import datetime, timedelta
from engine.core.SystemEntity import SystemEntity
import yaml
import pandas as pd
from random import gauss, randint



if __name__ == "__main__":
    
    members = list()
    with open('./template/members.yaml', 'r') as f:
        data = yaml.load(f, yaml.FullLoader)
        members = list(data)
    
    with open('./template/product.yaml', 'r') as f:
        data = yaml.load_all(f, yaml.FullLoader)
        data = list(data)            
        product = data[0][0]                        
        journeys = data[1]
        features = data[2]
    
    squads = list()
    with open('./template/squads.yaml', 'r') as f:
        data = yaml.load(f, yaml.FullLoader)
        squads = list(data)                         

    system = SystemEntity() 
    system.load_state(
        {
            "sinks": list(),
            "states": list(),
            "visualizations": list(), 
            "hourly_days": 7
        },
        product, members, squads, journeys, features)

    system.measure_slo()

    data = list()
    sources = list()
    for j in system.journeys:        
        for f in j.features:
            for s in f.sources:
                sources.append(s)

    start =  datetime(datetime.now().year, 1, 1) - timedelta(days=365)
    end = start + timedelta( minutes=59, seconds=59)    
    while end < datetime.now():    
        for s in sources:            
            total = randint(10, 100000)
            ava = round(total * gauss(s.avaSlo + (1 - s.avaSlo) * 0.1, 0.01))            
            exp = round(total * gauss(s.expSlo + (1 - s.expSlo) * 0.1, 0.01))            
            lat = round(gauss(s.latSlo, 100), 0)            
            data.append([s.source, 
                start.strftime("%Y-%m-%d %H:%M:%S"),
                end.strftime("%Y-%m-%d %H:%M:%S"), total, ava, exp, lat])
        start = start + timedelta(hours=1)        
        end = end + timedelta(hours=1)        

    df = pd.DataFrame(data, columns=['source', 'start','end', 'total', 'ava', 'exp', 'lat'] )
    df.to_csv('./template/generate_data.csv', header=False, index=False, sep=";")