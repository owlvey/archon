import pandas as pd
class StateUtil:

    @staticmethod
    def load_from_state(target, state:dict):
        for ok, ov in target.__dict__.items():
            if ok in state:
                target.__dict__[ok] = state[ok]        
                if target.__dict__[ok] is None:
                    raise ValueError('member is none ' + str(state))
    
    @staticmethod
    def print_entity(target):
        print(target.__dict__.__str__())
    
    @staticmethod
    def to_dataframe(items):
        if not items:
            return None
        
        metadata = dict()        
        data = list()
        for item in items:
            for k, v in item.__dict__.items():
                target_type = type(v)
                if not target_type is list:
                    if not k in metadata:
                        if target_type is float:
                            metadata[k] = 'float'
                        if target_type is int:
                            metadata[k] = 'int'
                        if target_type is int:
                            metadata[k] = 'datetime'
                    data.append(v)
        return pd.DataFrame(data, columns=[x for x in metadata.keys()])

                    
                    



            