from prompts import GET_ADDITIONAL_INFO
from utils import extract_cleaned_cypher, get_schema_text, prepare_info_str, get_bi_der_relationships
from llm import llm
import logging

def generate_cypher(user_query: str, info: list[tuple[str, dict]]):
    prompt = GET_ADDITIONAL_INFO.format(
        user_query=user_query,
        info=prepare_info_str(info=info),
        schema=get_schema_text(),
        bidir_rels=get_bi_der_relationships()
    )

    logging.info(prompt)

    resp = llm.invoke(prompt)

    logging.info(resp)
    cypher = extract_cleaned_cypher(resp.content)

    return cypher


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    user_query = "Which group is Jethalal's son a part of ?"
    relevant_nodes = [('Person', {'unique_id': '8f5ab237d5ff4b34a0409dd6c0dd0f6d', 'first_name': 'Jethalal', 'surname': 'Gada', 'nick_name': 'Jethia', 'gender': 'M'})]
    cypher = generate_cypher(user_query=user_query, info=relevant_nodes)
    print("\n")
    print(cypher)