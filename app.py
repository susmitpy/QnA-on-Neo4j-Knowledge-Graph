import json
import logging
from sys import exit

from execute_cypher import execute_cypher
from generate_answer import generate_answer
from generate_cypher import generate_cypher
from get_relevant_data import get_relevant_data

logging.basicConfig(level=logging.WARNING)

print("Welcome to TMKOC QnA")
print("To quit, press q")

while True:
    user_query = input("\nEnter your query: ")
    if user_query == "q":
        print("Bye !")
        exit()

    try:
        relevant_nodes = get_relevant_data(user_query=user_query)
        cypher_to_fetch_additional_info = generate_cypher(
            user_query=user_query, info=relevant_nodes
        )
        cypher_result = execute_cypher(cypher=cypher_to_fetch_additional_info)
        final_answer = generate_answer(
            user_query=user_query,
            info=relevant_nodes,
            cypher=cypher_to_fetch_additional_info,
            cypher_result=cypher_result,
        )

        with open("./data.json", "w") as f:
            json.dump({"user_query": user_query, "relevant_data": relevant_nodes, "cypher": cypher_to_fetch_additional_info, "cypher_result": cypher_result}, f)

        print(final_answer)
    except Exception as e:
        logging.error(e)
