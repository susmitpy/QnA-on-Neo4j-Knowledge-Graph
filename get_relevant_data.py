import json
import logging
from sys import exit

from neo4j.graph import Node, Relationship

from models import Model, node_rel_type_mapping
from vector_utils import search_nodes_rel
from utils import update_json


def get_relevant_data(user_query: str, top_k: int = 5) -> list[tuple[set, dict]]:
    """
    Returns the relevant nodes, relationships for the user query.

    Returns:
    list[tuple[set, dict]]: A list of tuples containing the labels and the data info.
    """
    nodes_rel: list[tuple[str, Node, float]] = search_nodes_rel(user_query)
    # Sort the data by score, the sort in query will work only for each separate entity
    sorted_nodes_rels = sorted(nodes_rel, key=lambda x: x[2], reverse=True)
    top_k_sorted_nodes_rels = sorted_nodes_rels[:top_k]

    result = []
    for entity, node_rel, score in top_k_sorted_nodes_rels:
        data_obj: Model = node_rel_type_mapping[entity].inflate(node_rel)
        data_info = data_obj.get_model_info()
        labels_type: str
        if isinstance(node_rel, Node):
            labels_type = str(list(node_rel.labels))
        elif isinstance(node_rel, Relationship):
            node_rel: Relationship
            labels_type = node_rel.type
        result.append((labels_type, data_info))
        logging.info(entity)
        logging.info(labels_type)
        logging.info(data_info)
        logging.info(score)

    logging.info(result)

    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("To quit, press q")
    while True:
        user_query = input("Enter your query: ")
        if user_query == "q":
            print("Bye !")
            exit()

        with open("./data.json", "w") as f:
            json.dump({
                "user_query": user_query,
            }, f)
            
        op = get_relevant_data(user_query)
        update_json("relevant_data", op)
        
