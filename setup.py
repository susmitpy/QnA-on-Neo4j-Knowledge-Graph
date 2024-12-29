from models import Person, Group, Company, Society, HasCommitteeMember, INDEXES
from utils import execute_cypher_query
from vector_utils import prepare_values_for_embedding, embed_text

def update_embeddings():
    # Update embeddings for Person
    persons: list[Person] = Person.nodes.all()
    for person in persons:
        values = person.get_values_for_embedding()
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
        values = society.get_values_for_embedding()
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
        values = group.get_values_for_embedding()
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
        values = company.get_values_for_embedding()
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
        rel_model: HasCommitteeMember = HasCommitteeMember.inflate(rel[0])
        values = rel_model.get_values_for_embedding()
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
    query = f"""
    CREATE VECTOR INDEX `{INDEXES.PERSON_EMBEDDING}`
    FOR (n:Person) ON (n.embedding)
    """
    execute_cypher_query(query)

    # Create vector index for Group
    query = f"""
    CREATE VECTOR INDEX `{INDEXES.GROUP_EMBEDDING}`
    FOR (n:Group) ON (n.embedding)
    """
    execute_cypher_query(query)

    # Create vector index for Company
    query = f"""
    CREATE VECTOR INDEX `{INDEXES.COMPANY_EMBEDDING}`
    FOR (n:Company) ON (n.embedding)
    """
    execute_cypher_query(query)

    # Create vector index for Society
    query = f"""
    CREATE VECTOR INDEX `{INDEXES.SOCIETY_EMBEDDING}`
    FOR (n:Society) ON (n.embedding)
    """
    execute_cypher_query(query)

    # Create vector index for HasCommitteeMember relationship
    query = f"""
    CREATE VECTOR INDEX `{INDEXES.HAS_COMMITTEE_MEMBER_EMBEDDING}`
    FOR () - [r:HAS_COMMITTEE_MEMBER] - () ON (r.embedding)
    """
    execute_cypher_query(query)

def setup():
    update_embeddings()
    create_vector_index()
    create_index_on_unique_id()

if __name__ == "__main__":
    setup()