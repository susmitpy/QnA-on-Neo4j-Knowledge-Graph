from sys import exit
from get_relevant_nodes import get_relevant_nodes
from generate_cypher import generate_cypher
from execute_cypher import execute_cypher
from generate_answer import generate_answer

import logging
logging.basicConfig(level=logging.ERROR)

logging.info("Welcome to TMKOC QnA")
logging.info("To quit, press q")
 
while True:
    user_query = input("Enter your query: ")
    if user_query == "q":
        print("Bye !")
        exit()

    relevant_nodes = get_relevant_nodes(user_query=user_query)
    cypher_to_fetch_additional_info = generate_cypher(user_query=user_query, info=relevant_nodes)
    cypher_result = execute_cypher(cypher=cypher_to_fetch_additional_info)
    final_answer = generate_answer(user_query=user_query, info=relevant_nodes, cypher=cypher_to_fetch_additional_info, cypher_result=cypher_result)

    print(final_answer)

    