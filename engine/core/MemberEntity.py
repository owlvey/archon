class MemberEntity:
    
    def __init__(self): 
        self.email = None
        self.name = None    
        self.nickname = None
    
    

    @staticmethod
    def find_member(items, target):
        for x in items:
            if x.email == target:
                return x
        else:
            raise ValueError(f"not found {target}")
        
    