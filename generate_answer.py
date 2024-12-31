import logging

from llm import llm
from prompts import GET_FINAL_ANSWER
from utils import get_bi_der_relationships, get_schema_text, prepare_info_str


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
    user_query = "Which group is Jethalal's son a part of ?"
    relevant_data = [
        (
            "['Person']",
            {
                "unique_id": "68caf0e03eb74f3b959ddb5f13811695",
                "first_name": "Jethalal",
                "surname": "Gada",
                "nick_name": "Jethia",
                "gender": "M",
            },
        ),
        (
            "HAS_COMMITTEE_MEMBER",
            {"unique_id": "6ebcc32e8daf4988973fda14d4dd8109", "position": "Member"},
        ),
        (
            "['Group']",
            {"unique_id": "8c7103cf3db94c9fba3a0a7dcebc3758", "name": "Mahila Mandal"},
        ),
        (
            "['Person']",
            {
                "unique_id": "dee49592d0dd47b3b71a16f8b3d2cc9b",
                "first_name": "Sonalika",
                "surname": "Bhide",
                "nick_name": "Sonu",
                "gender": "F",
            },
        ),
        (
            "['Person']",
            {
                "unique_id": "31d5992f8ff74bdfb70374b3d8c949a1",
                "first_name": "Gulabkumar",
                "surname": "Haathi",
                "nick_name": "Goli",
                "gender": "M",
            },
        ),
    ]
    cypher = """
MATCH (p1:Person {first_name: 'Jethalal', surname: 'Gada'})
      -[:IS_PARENT_OF*1]-(p2:Person)
      -[:IS_PART_OF]-(g:Group)
RETURN g.name"""
    cypher_result = ([["Tapu Sena"]], ["g.name"])

    resp = generate_answer(
        user_query=user_query,
        info=relevant_data,
        cypher=cypher,
        cypher_result=cypher_result,
    )
    logging.info("\n")
    logging.info(resp)
