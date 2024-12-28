from prompts import GET_FINAL_ANSWER
from utils import get_schema_text, prepare_info_str
from llm import llm
import logging


def generate_answer(user_query: str, info: list[tuple[str, dict]], cypher:str, cypher_result:tuple[list[list], list]) -> str:
    prompt = GET_FINAL_ANSWER.format(
        user_query=user_query,
        info=prepare_info_str(info=info),
        schema=get_schema_text(),
        cypher_query=cypher,
        cypher_query_result=cypher_result
    )

    logging.info(prompt)

    resp = llm.invoke(prompt)
    return resp.content

if __name__ == "__main__":
    logging.basicConfig(level=logging.info)
    user_query = "Which group is Jethalal's son a part of ?"
    relevant_nodes = [('Person', {'element_id': '4:e739d468-094d-4147-891a-7dff70c687c6:2', 'first_name': 'Jethalal', 'surname': 'Gada', 'nick_name': 'Jethia', 'gender': 'M'})]
    cypher="""MATCH (jethalal:Person {unique_id:'8f5ab237d5ff4b34a0409dd6c0dd0f6d'})-[parent_is_parent_of:IS_PARENT_OF]->(child)
OPTIONAL MATCH (child)-[part_in_group:IS_PART_OF]->(group)
RETURN group.name AS name"""
    cypher_result = ([['Tapu Sena']], ['group_name'])

    resp = generate_answer(user_query=user_query, info=relevant_nodes, cypher=cypher, cypher_result=cypher_result)
    logging.info("\n")
    logging.info(resp)