import logging

from llm import llm
from prompts import GET_ADDITIONAL_INFO
from utils import (
    extract_cleaned_cypher,
    get_bi_der_relationships,
    get_schema_text,
    prepare_info_str,
    update_json,
    get_data_from_json
)


def generate_cypher(user_query: str, info: list[tuple[str, dict]]):
    prompt = GET_ADDITIONAL_INFO.format(
        user_query=user_query,
        info=prepare_info_str(info=info),
        schema=get_schema_text(),
        bidir_rels=get_bi_der_relationships(),
    )

    logging.info(prompt)

    resp_text = llm.invoke(prompt)

    logging.info(resp_text)
    cypher = extract_cleaned_cypher(resp_text)

    return cypher


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    user_query, relevant_data = get_data_from_json(["user_query", "relevant_data"])
    cypher = generate_cypher(user_query=user_query, info=relevant_data)
    print("\n")
    print(cypher)

    update_json("cypher", cypher)
