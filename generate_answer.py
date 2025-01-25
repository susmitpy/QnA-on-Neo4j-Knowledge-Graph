import logging

from llm import llm
from prompts import GET_FINAL_ANSWER
from utils import get_bi_der_relationships, get_data_from_json, get_schema_text, prepare_info_str


def generate_answer(
    user_query: str,
    info: list[tuple[str, dict]],
    cypher: str,
    cypher_result: tuple[list[list], list],
) -> str:
    prompt = GET_FINAL_ANSWER.format(
        user_query=user_query,
        info=prepare_info_str(info=info),
        schema=get_schema_text(),
        cypher_query=cypher,
        cypher_query_result=cypher_result,
        bidir_rels=get_bi_der_relationships(),
    )

    logging.info(prompt)

    resp_text = llm.invoke(prompt)
    return resp_text


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    user_query, relevant_data, cypher, cypher_result = get_data_from_json(["user_query", "relevant_data", "cypher", "cypher_result"])
    resp = generate_answer(
        user_query=user_query,
        info=relevant_data,
        cypher=cypher,
        cypher_result=cypher_result,
    )
    logging.info("\n")
    logging.info(resp)
