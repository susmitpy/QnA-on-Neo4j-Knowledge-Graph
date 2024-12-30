from prompts import GET_FINAL_ANSWER
from utils import get_schema_text, prepare_info_str, get_bi_der_relationships
from llm import llm
import logging


def generate_answer(user_query: str, info: list[tuple[str, dict]], cypher:str, cypher_result:tuple[list[list], list]) -> str:
    prompt = GET_FINAL_ANSWER.format(
        user_query=user_query,
        info=prepare_info_str(info=info),
        schema=get_schema_text(),
        cypher_query=cypher,
        cypher_query_result=cypher_result,
        bidir_rels=get_bi_der_relationships()
    )

    logging.info(prompt)

    resp = llm.invoke(prompt)
    return resp.content

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
    cypher_result = ([['Tapu Sena']], ['group_name'])

    resp = generate_answer(user_query=user_query, info=relevant_nodes, cypher=cypher, cypher_result=cypher_result)
    logging.info("\n")
    logging.info(resp)