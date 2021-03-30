class SquadEntity:

    def __init__(self) -> None:
        self.squad = None
        self.description = None
        self.members = list()    
    
    def load_members(self, items):
        temp = self.members
        self.members = list()
        for item in temp:            
            self.members.append(next(x for x in items if x.email == item))

    


