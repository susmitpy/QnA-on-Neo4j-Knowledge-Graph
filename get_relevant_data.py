import logging
from setup import search_nodes_rel
from models import Model, Person, Group, Company, Society, HasCommitteMember
from neo4j.graph import Node

node_type_mapping = {
    "Person": Person,
    "Group": Group,
    "Company": Company,
    "Society": Society,
    "HasCommitteeMember": HasCommitteMember,
}

#TODO: Handle both nodes and relationships
#TODO: Handle multiple labels for a node
def get_relevant_data(user_query: str) -> list[tuple[str, dict]]:
    """
    Returns the relevant nodes for the user query.
    """
    nodes: list[tuple[str,Node,float]] = search_nodes_rel(user_query)

    result = []
    for node_type, node, _ in nodes:
        node_obj:Model = node_type_mapping[node_type].inflate(node)
        node_info = node_obj.get_model_info()
        result.append((node_type, node_info))

    return result


user_query = "Which group is Jethalal's son a part of ?"
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = get_relevant_data(user_query)
    print(data)