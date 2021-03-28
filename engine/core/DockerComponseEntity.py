class DockerComposeEntity:
    def __init__(self):
        self.sinks = list()

    def build_state(self):
        result = dict()

        services = dict()
        sink_count = 0
        for sink in self.sinks:
            services[f"sink_{sink_count}"] = sink.__dict__
            sink_count += 1

        result["version"] = "3"
        result["services"] = services
        result["networks"] = {
            "owlvey-net": {
                "external": False
            }
        }
        return result




