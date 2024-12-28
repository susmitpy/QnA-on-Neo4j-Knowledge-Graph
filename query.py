from neomodel import db
from neomodel import config

# Configure the connection to Neo4j
config.DATABASE_URL = 'bolt://neo4j:neotest123@localhost:7687'

def execute_cypher_query(query, params=None):
    """
    Executes a Cypher query and returns the result.
    """
    return db.cypher_query(query, params)

def get_schema_text():
    """
    Retrieves the schema from models in text form for LLM input.
    """
    schema = """
Nodes:
- Person
  - unique_id
  - first_name
  - surname
  - nick_name
  - gender (M,F)
- Group
  - unique_id

- Company
  - unique_id
  - name

Relationships:
- IS_SPOUSE_OF: Person - Person
- IS_PARENT_OF: Person -> Person
- IS_PART_OF: Person -> Group
- IS_OWNER_OF: Person -> Company
"""
    return schema.strip()