import logging
from utils import execute_cypher_query

def execute_cypher(cypher:str):
    return execute_cypher_query(cypher)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    user_query = "Which group is Jethalal's son a part of ?"
    relevant_nodes = [('Person', {'element_id': '4:e739d468-094d-4147-891a-7dff70c687c6:2', 'first_name': 'Jethalal', 'surname': 'Gada', 'nick_name': 'Jethia', 'gender': 'M'})]
    cypher="""MATCH (p:Person {unique_id: '8f5ab237d5ff4b34a0409dd6c0dd0f6d'})-[:IS_PARENT_OF]-(c:Person)
OPTIONAL MATCH (c)-[:IS_PART_OF]->(g:Group)
WHERE p.gender = 'M'
RETURN g.name as group_name"""
    resp = execute_cypher(cypher=cypher)
    logging.debug(resp)