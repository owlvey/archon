class StateUtil:

    @staticmethod
    def load_from_state(target, state:dict):
        for ok, ov in target.__dict__.items():
            if ok in state:
                target.__dict__[ok] = state[ok]
    
    @staticmethod
    def print_entity(target):
        print(target.__dict__.__str__())
            