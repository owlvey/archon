import yaml
import pathlib
import os


class FileGateway:
    def __init__(self):
        self.dir = pathlib.Path(__file__).parent.absolute()

    def read_data(self):
        target = pathlib.Path(os.path.join(self.dir, './../../data/template.yaml')).absolute()
        with open(target, 'r') as f:
            data = yaml.load_all(f, yaml.FullLoader)
            data = list(data)
            infra = data[0][0]
            product = data[1][0]
            members = data[2]
            return infra, product, members

    def write_app(self, state):
        target = os.path.join(self.dir, './../../wip/docker-compose.yaml')
        with open(target, 'w') as f:
            yaml.dump(state, f)
