from sentence_transformers import SentenceTransformer
from consts import STOP_WORDS
from models import Model, INDEXES
from utils import execute_cypher_query
from neo4j.graph import Node
import numpy as np

import logging

#TODO: use a better embedder which is apt for values or maybe key value pairs and/or find better strategy
# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

def prepare_values_for_embedding(values: list[str]) -> str:
    return " ".join(values)

def embed_text(text) -> np.ndarray[float]:
    return model.encode(text)


def search_nodes_rel(user_query: str, top_k: int = 10, score_thresh=0.5) -> list[tuple[str, Model, float]]:
    """
    Processes a user query, performs a vector search across Person, Group, and Company.
    Relationships HAS_COMMITTEE_MEMBER is also considered.
    
    Args:
        user_query (str): The user's search query.
        top_k (int): The number of top results to return from each index.
        score_thresh (float): threshold for score between 0 and 1
    """
    # Split the query into individual words
    words = user_query.split(" ")

    # Remove stop words
    words = [word for word in words if word.lower() not in STOP_WORDS]

    # Join back
    sentence = " ".join(words)

    # Generate embedding for each word in user's query
    # query_embeddings = [embed_text(word).tolist() for word in words]

    query_embeddings = [embed_text(sentence).tolist()]

    # Define Cypher queries for each index
    cypher_queries = {
        'Person': f"""
            MATCH (n:Person)
            WHERE n.embedding IS NOT NULL
            CALL db.index.vector.queryNodes('{INDEXES.PERSON_EMBEDDING}', $top_k, $query_embedding) YIELD node, score
            WHERE score > $score_thresh
            RETURN 'Person' AS type, node, score
        """,
        'Group': f"""
            MATCH (n:Group)
            WHERE n.embedding IS NOT NULL
            CALL db.index.vector.queryNodes('{INDEXES.GROUP_EMBEDDING}', $top_k, $query_embedding) YIELD node, score
            WHERE score > $score_thresh
            RETURN 'Group' AS type, node, score
        """,
        'Company': f"""
            MATCH (n:Company)
            WHERE n.embedding IS NOT NULL
            CALL db.index.vector.queryNodes('{INDEXES.COMPANY_EMBEDDING}', $top_k, $query_embedding) YIELD node, score
            WHERE score > $score_thresh
            RETURN 'Company' AS type, node, score
        """,
        'Society': f"""
            MATCH (n:Society)
            WHERE n.embedding IS NOT NULL
            CALL db.index.vector.queryNodes('{INDEXES.SOCIETY_EMBEDDING}', $top_k, $query_embedding) YIELD node, score
            WHERE score > $score_thresh
            RETURN 'Society' AS type, node, score
        """,
        'HasCommitteeMember': f"""
            MATCH () - [r:HAS_COMMITTEE_MEMBER] - ()
            WHERE r.embedding IS NOT NULL
            CALL db.index.vector.queryRelationships('{INDEXES.HAS_COMMITTEE_MEMBER_EMBEDDING}', $top_k, $query_embedding) YIELD relationship, score
            WHERE score > $score_thresh
            RETURN 'HasCommitteeMember' AS type, relationship, score
        """
    }

    combined_results = []
    node_ids = set()

    # Execute queries for each index
    for query_embedding in query_embeddings:
        for entity, cypher in cypher_queries.items():
            results: list[tuple[str, Node, float]]
            results, meta = execute_cypher_query(cypher, {
                'query_embedding': query_embedding,
                'top_k': top_k,
                "score_thresh": score_thresh
            })

            #TODO: Check why duplicate nodes are being returned
            logging.debug(cypher)
            logging.debug(len(results))
            logging.debug("\n")

            for record in results:
                node_type = record[0]
                node = record[1]
                score = record[2]

                if node.element_id not in node_ids:
                    combined_results.append((node_type, node, score))
                    node_ids.add(node.element_id)
    
    # Print combined results
    if not combined_results:
        logging.error("No matching nodes found.")
        return
    
    return combined_results

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)