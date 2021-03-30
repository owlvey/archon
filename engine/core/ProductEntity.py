class ProductEntity:

    def __init__(self):
        self.description = None
        self.product = None
        self.latency_percentile = None
        self.leaders = list()        
    
    def load_members(self, items):
        temp = self.leaders
        self.leaders = list()
        for item in temp:            
            self.leaders.append(next(x for x in items if x.email == item))
    
    
    
        
