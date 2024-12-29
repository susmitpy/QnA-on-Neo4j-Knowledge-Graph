import logging
from vector_utils import search_nodes_rel
from models import Model, Person, Group, Company, Society, HasCommitteeMember
from neo4j.graph import Node
from sys import exit

node_type_mapping = {
    "Person": Person,
    "Group": Group,
    "Company": Company,
    "Society": Society,
    "HasCommitteeMember": HasCommitteeMember,
}

#TODO: Handle both nodes and relationships
#TODO: Handle multiple labels for a node
def get_relevant_data(user_query: str) -> list[tuple[str, dict]]:
    """
    Returns the relevant nodes for the user query.
    """
    nodes: list[tuple[str,Node,float]] = search_nodes_rel(user_query)
    # Sort the data by score, the filter in query will work only for each separate entity
    sorted_nodes = sorted(nodes, key=lambda x: x[2], reverse=True)

    result = []
    for node_type, node, score in sorted_nodes:
        node_obj:Model = node_type_mapping[node_type].inflate(node)
        node_info = node_obj.get_model_info()
        result.append((node_type, node_info))
        logging.info(node_type)
        logging.info(node_info)
        logging.info(score)

    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("To quit, press q")
    while True:
        user_query = input("Enter your query: ")
        if user_query == "q":
            print("Bye !")
            exit()

        get_relevant_data(user_query)