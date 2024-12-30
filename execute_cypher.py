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
    relevant_data = [("['Person']", {'unique_id': '68caf0e03eb74f3b959ddb5f13811695', 'first_name': 'Jethalal', 'surname': 'Gada', 'nick_name': 'Jethia', 'gender': 'M'}), ('HAS_COMMITTEE_MEMBER', {'unique_id': '6ebcc32e8daf4988973fda14d4dd8109', 'position': 'Member'}), ("['Group']", {'unique_id': '8c7103cf3db94c9fba3a0a7dcebc3758', 'name': 'Mahila Mandal'}), ("['Person']", {'unique_id': 'dee49592d0dd47b3b71a16f8b3d2cc9b', 'first_name': 'Sonalika', 'surname': 'Bhide', 'nick_name': 'Sonu', 'gender': 'F'}), ("['Person']", {'unique_id': '31d5992f8ff74bdfb70374b3d8c949a1', 'first_name': 'Gulabkumar', 'surname': 'Haathi', 'nick_name': 'Goli', 'gender': 'M'})]
    cypher="""
MATCH (p1:Person {first_name: 'Jethalal', surname: 'Gada'})
      -[:IS_PARENT_OF*1]-(p2:Person)
      -[:IS_PART_OF]-(g:Group)
RETURN g.name
"""
    resp = execute_cypher(cypher=cypher)
    logging.info(resp)