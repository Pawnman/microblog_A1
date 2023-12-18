import json


class JsonSerializer(object):
    def serialize(self, key, value):
        if isinstance(value, str):
            return value, 1
        if isinstance(value, list):         # Если присутствует список подписчиков
            tmp = []
            for element in value:
                tmp.append(self.serialize(key, element))
            value = tmp
        if type(value).__module__ != "__builtin__":
            value = dict(value)
        return json.dumps(value), 2
    
    def deserialize(self, key, value, flags):
        if flags == 1:
            return value
        if flags == 2:
            return json.loads(value)
        raise Exception("Unknown serialization format")
        