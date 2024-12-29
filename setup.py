from sentence_transformers import SentenceTransformer
from models import Person, Group, Company, Society, Model, HasCommitteMember
from utils import execute_cypher_query
from neo4j.graph import Node

import logging

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

def prepare_values_for_embedding(values: list[str]) -> str:
    # Prepare the values for embedding
    return ", ".join(values)

def embed_text(text) -> list[float]:
    # Embed the text
    return model.encode(text)

def update_embeddings():
    # Update embeddings for Person
    persons: list[Person] = Person.nodes.all()
    for person in persons:
        values = person.get_values()
        text = prepare_values_for_embedding(values)
        embedding = embed_text(text).tolist()
        query = """
        MATCH (a:Person)
        WHERE elementId(a) = $elementId
        CALL db.create.setNodeVectorProperty(a, 'embedding', $embedding);
        """
        execute_cypher_query(query, {
            'elementId': person.element_id,
            'embedding': embedding
        })

    # Update embeddings for Society
    societies: list[Society] = Society.nodes.all()
    for society in societies:
        values = society.get_values()
        text = prepare_values_for_embedding(values)
        embedding = embed_text(text).tolist()
        query = """
        MATCH (a:Society)
        WHERE elementId(a) = $elementId
        CALL db.create.setNodeVectorProperty(a, 'embedding', $embedding);
        """
        execute_cypher_query(query, {
            'elementId': society.element_id,
            'embedding': embedding
        })
    
    # Update embeddings for Group
    groups: list[Group] = Group.nodes.all()
    for group in groups:
        values = group.get_values()
        text = prepare_values_for_embedding(values)
        embedding = embed_text(text).tolist()
        query = """
        MATCH (a:Group)
        WHERE elementId(a) = $elementId
        CALL db.create.setNodeVectorProperty(a, 'embedding', $embedding);
        """
        execute_cypher_query(query, {
            'elementId': group.element_id,
            'embedding': embedding
        })
    
    # Update embeddings for Company
    companies: list[Company] = Company.nodes.all()
    for company in companies:
        values = company.get_values()
        text = prepare_values_for_embedding(values)
        embedding = embed_text(text).tolist()
        query = """
        MATCH (a:Company)
        WHERE elementId(a) = $elementId
        CALL db.create.setNodeVectorProperty(a, 'embedding', $embedding);
        """
        execute_cypher_query(query, {
            'elementId': company.element_id,
            'embedding': embedding
        })

    # Update embeddings for HasCommitteeMember relationship
    has_committee_members_rels = execute_cypher_query(
    """
    MATCH (:Society) - [r:HAS_COMMITTEE_MEMBER] - (:Person)
    RETURN r    
    """
    )
    for rel in has_committee_members_rels[0]:
        logging.debug(rel)
        rel_model: HasCommitteMember = HasCommitteMember.inflate(rel[0])
        values = rel_model.get_values()
        text = prepare_values_for_embedding(values)
        embedding = embed_text(text).tolist()
        query = """
        MATCH () - [r:HAS_COMMITTEE_MEMBER] - ()
        WHERE elementId(r) = $elementId
        CALL db.create.setRelationshipVectorProperty(r, 'embedding', $embedding);
        """
        execute_cypher_query(query, {
            'elementId': rel_model.element_id,
            'embedding': embedding
        })

def create_index_on_unique_id():
    # Create index on unique_id for Person
    query = """
    CREATE INDEX FOR (n:Person) ON (n.unique_id)
    """
    execute_cypher_query(query)

    # Create index on unique_id for Group
    query = """
    CREATE INDEX FOR (n:Group) ON (n.unique_id)
    """
    execute_cypher_query(query)

    # Create index on unique_id for Company
    query = """
    CREATE INDEX FOR (n:Company) ON (n.unique_id)
    """
    execute_cypher_query(query)

    # Create index on unique_id for Society
    query = """
    CREATE INDEX FOR (n:Society) ON (n.unique_id)
    """
    execute_cypher_query(query)

    # Create index on unique_id for HasCommitteeMember relationship
    query = """
    CREATE INDEX FOR () - [r:HAS_COMMITTEE_MEMBER] - () ON (r.unique_id)
    """
    execute_cypher_query(query)


def create_vector_index():
    # Create vector index for Person
    query = """
    CREATE VECTOR INDEX `person-embeddings`
    FOR (n:Person) ON (n.embedding)
    """
    execute_cypher_query(query)

    # Create vector index for Group
    query = """
    CREATE VECTOR INDEX `group-embeddings`
    FOR (n:Group) ON (n.embedding)
    """
    execute_cypher_query(query)

    # Create vector index for Company
    query = """
    CREATE VECTOR INDEX `company-embeddings`
    FOR (n:Company) ON (n.embedding)
    """
    execute_cypher_query(query)

    # Create vector index for HasCommitteeMember relationship
    query = """
    CREATE VECTOR INDEX `has-committee-member-embeddings`
    FOR () - [r:HAS_COMMITTEE_MEMBER] - () ON (r.embedding)
    """
    execute_cypher_query(query)

STOP_WORDS = {'i',
 'me',
 'my',
 'myself',
 'we',
 'our',
 'ours',
 'ourselves',
 'you',
 'your',
 'yours',
 'yourself',
 'yourselves',
 'he',
 'him',
 'his',
 'himself',
 'she',
 'her',
 'hers',
 'herself',
 'it',
 'its',
 'itself',
 'they',
 'them',
 'their',
 'theirs',
 'themselves',
 'what',
 'which',
 'who',
 'whom',
 'this',
 'that',
 'these',
 'those',
 'am',
 'is',
 'are',
 'was',
 'were',
 'be',
 'been',
 'being',
 'have',
 'has',
 'had',
 'having',
 'do',
 'does',
 'did',
 'doing',
 'a',
 'an',
 'the',
 'and',
 'but',
 'if',
 'or',
 'because',
 'as',
 'until',
 'while',
 'of',
 'at',
 'by',
 'for',
 'with',
 'about',
 'against',
 'between',
 'into',
 'through',
 'during',
 'before',
 'after',
 'above',
 'below',
 'to',
 'from',
 'up',
 'down',
 'in',
 'out',
 'on',
 'off',
 'over',
 'under',
 'again',
 'further',
 'then',
 'once',
 'here',
 'there',
 'when',
 'where',
 'why',
 'how',
 'all',
 'any',
 'both',
 'each',
 'few',
 'more',
 'most',
 'other',
 'some',
 'such',
 'no',
 'nor',
 'not',
 'only',
 'own',
 'same',
 'so',
 'than',
 'too',
 'very',
 's',
 't',
 'can',
 'will',
 'just',
 'don',
 'should',
 'now'}

def search_nodes_rel(user_query: str, top_k: int = 10) -> list[tuple[str, Model, float]]:
    """
    Processes a user query, performs a vector search across Person, Group, and Company.
    Relationships HAS_COMMITTEE_MEMBER is also considered.
    and prints the matching nodes with similarity scores greater than 0.8.
    
    Args:
        user_query (str): The user's search query.
        top_k (int): The number of top results to return from each index.
    """
    # Split the query into individual words
    words = user_query.split(" ")

    # Remove stop words
    words = [word for word in words if word not in STOP_WORDS]

    # Generate embedding for each word in user's query
    query_embeddings = [embed_text(word).tolist() for word in words]

    # Define Cypher queries for each index

    cypher_queries = {
        'Person': """
            MATCH (n:Person)
            WHERE n.embedding IS NOT NULL
            CALL db.index.vector.queryNodes('person-embeddings', $top_k, $query_embedding) YIELD node, score
            WHERE score > 0.8
            RETURN 'Person' AS type, node, score
        """,
        'Group': """
            MATCH (n:Group)
            WHERE n.embedding IS NOT NULL
            CALL db.index.vector.queryNodes('group-embeddings', $top_k, $query_embedding) YIELD node, score
            WHERE score > 0.8
            RETURN 'Group' AS type, node, score
        """,
        'Company': """
            MATCH (n:Company)
            WHERE n.embedding IS NOT NULL
            CALL db.index.vector.queryNodes('company-embeddings', $top_k, $query_embedding) YIELD node, score
            WHERE score > 0.8
            RETURN 'Company' AS type, node, score
        """,
        'HasCommitteeMember': """
            MATCH () - [r:HAS_COMMITTEE_MEMBER] - ()
            WHERE r.embedding IS NOT NULL
            CALL db.index.vector.queryRelationships('has-committee-member-embeddings', $top_k, $query_embedding) YIELD relationship, score
            WHERE score > 0.8
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
                'top_k': top_k
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

def setup():
    update_embeddings()
    create_vector_index()
    create_index_on_unique_id()

if __name__ == "__main__":
    setup()