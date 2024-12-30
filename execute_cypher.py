import logging
from utils import execute_cypher_query
from neo4j.graph import Node, Relationship
from typing import Union

def execute_cypher(cypher:str):
    data, columns =  execute_cypher_query(cypher)
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
                del properties['embedding']
                parsed_record.append(f"{labels} {properties}")
            elif isinstance(item, Relationship):
                item: Relationship
                rel_type = item.type
                properties: dict = dict(item.items())
                del properties['embedding']
                parsed_record.append(f"{rel_type} {properties}")
            else:
                parsed_record.append(item)
        parsed_data.append(parsed_record)

    return parsed_data, columns

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    user_query = "Which group is Jethalal's son a part of ?"
    relevant_nodes = [("['Person']", {'unique_id': '71ab9b9354224045962ba3606e452729', 'first_name': 'Jethalal', 'surname': 'Gada', 'nick_name': 'Jethia', 'gender': 'M'}), ('HAS_COMMITTEE_MEMBER', {'unique_id': 'a9a73ec269664b59b4095a1cdc591ca5', 'position': 'Member'}), ("['Group']", {'unique_id': '46cc614dbc9c46978f504adc1dedd584', 'name': 'Mahila Mandal'}), ("['Person']", {'unique_id': '27f54f7cbba2475abc68dad230d91295', 'first_name': 'Sonalika', 'surname': 'Bhide', 'nick_name': 'Sonu', 'gender': 'F'}), ("['Person']", {'unique_id': 'b7ae43fa45f94f6090c2e8cab9d3344b', 'first_name': 'Gulabkumar', 'surname': 'Haathi', 'nick_name': 'Goli', 'gender': 'M'})]
    cypher="""
    MATCH (p:Person)-[:IS_PARENT_OF]->(c:Person)
WHERE p.unique_id = '71ab9b9354224045962ba3606e452729'
WITH c
OPTIONAL MATCH (c)-[:IS_PART_OF]->(g:Group)
RETURN g.name AS group_name
"""
    resp = execute_cypher(cypher=cypher)
    logging.info(resp)