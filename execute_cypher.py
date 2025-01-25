import logging
from typing import Union

from neo4j.graph import Node, Relationship

from utils import execute_cypher_query, get_data_from_json, update_json


def execute_cypher(cypher: str):
    data, columns = execute_cypher_query(cypher)
    data: list[list[Union[Node, Relationship, str, int, float]]]
    columns: list[str]

    parsed_data = []
    for record in data:
        parsed_record = []
        for item in record:
            if isinstance(item, Node):
                item: Node
                labels = str(list(item.labels))
                properties: dict = dict(item.items())
                del properties["embedding"]
                parsed_record.append(f"{labels} {properties}")
            elif isinstance(item, Relationship):
                item: Relationship
                rel_type = item.type
                properties: dict = dict(item.items())
                del properties["embedding"]
                parsed_record.append(f"{rel_type} {properties}")
            else:
                parsed_record.append(item)
        parsed_data.append(parsed_record)

    return parsed_data, columns


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    [cypher] = get_data_from_json(["cypher"])
    resp = execute_cypher(cypher=cypher)
    logging.info(resp)
    update_json("cypher_result", resp)
