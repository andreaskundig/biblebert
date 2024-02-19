from dataclasses import dataclass
from pathlib import Path
import json
import msgpack

@dataclass
class Data:
    ids: list[str]
    #TODO use type from model (numpy stuff?)
    embeddings: list[list[float]]



def data_from_file(path: Path) -> Data:
    with open(path) as f:
        #TODO use msgpack
        data = json.load(f)
        return Data(data['ids'], data['embeddings'])

def save_data(data:Data, path: Path):
    #TODO save with msgpack
    pass
