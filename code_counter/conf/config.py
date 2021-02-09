
import json  
import pkg_resources

resource_package = __name__

def load():
    filename = pkg_resources.resource_filename(resource_package, 'config.json')
    with open(filename, 'rb') as config:
            config = json.load(config)
    return config