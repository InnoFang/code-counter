#!/usr/bin/env python3
# coding:utf8
import json  
import pkg_resources

resource_package = __name__

def load():
    filename = pkg_resources.resource_filename(resource_package, 'config.json')
    with open(filename, 'rb') as config:
            conf = json.load(config)
    return conf