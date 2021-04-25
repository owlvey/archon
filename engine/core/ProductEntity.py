from engine.core.MemberEntity import MemberEntity


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
            self.leaders.append( MemberEntity.find_member(items, item) )        
    
    def __str__(self) -> str:
        return "Product Entity {} {} {}".format(self.product, self.description, self.leaders)

