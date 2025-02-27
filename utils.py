import json
import logging
import os
import re
from typing import Any

from neomodel import config, db

# Configure the connection to Neo4j
config.DATABASE_URL = "bolt://neo4j:neotest123@localhost:7687"

def get_data_from_json(keys: list[str]) -> list[Any]:
    """
    Retrieves the values for the given keys from the JSON file.

    Args:
        keys (list[str]): A list of keys to retrieve the values for.

    Returns:
        [Any]: A list of values corresponding to the given keys.
    """
    with open("./data.json", "r") as f:
        data = json.load(f)
        return [data[key] for key in keys]

def update_json(key: str, value:Any):
    """
    Updates the JSON with the given key-value pair.
    """
    with open("./data.json", "r") as f:
        data = json.load(f)

    data[key] = value
    with open("./data.json", "w") as f:
        json.dump(data, f, indent=4)

def extract_cleaned_cypher(resp_content: str) -> str:
    """
    Extracts and returns a cleaned Cypher query from the given response content.

    Args:
        resp_content (str): The response content to search for a Cypher query.

    Returns:
        str: A string containing the extracted and formatted Cypher query, or an empty string if not found.
    """
    resp_content = resp_content.strip()
    logging.info(resp_content)

    # Check if the response content is a raw Cypher query
    if resp_content.lower().startswith("match"):
        return resp_content

    # Attempt to extract Cypher queries from the response content using regular expressions
    cypher_queries = [
        re.search(
            r"```cypher\n(.*?)\n```", resp_content, re.DOTALL
        ),  # multi-line syntax
        re.search(r"```sql\n(.*?)\n```", resp_content, re.DOTALL),  # multi-line syntax
        re.search(r"```(.*?)\n```", resp_content, re.DOTALL),  # multi-line syntax
        re.search(r"(?:\\n|^)(?:(?:MATCH) )?\((.*?)\)", resp_content, re.DOTALL),
    ]

    # Find the first matching Cypher query (if any) and return it
    for cypher in cypher_queries:
        if cypher:
            # Remove leading and trailing whitespace from the extracted query
            return cypher.group(1).strip()

    # If no Cypher queries are found, raise an exception
    raise Exception("Cypher Query Not Found")


def test_extract_cleaned_cypher():
    content = "```\nMATCH (jethalal:Person{unique_id:'8f5ab237d5ff4b34a0409dd6c0dd0f6d'}) \nOPTIONAL MATCH (jethalal)-[parent:IS_PARENT_OF]->(child:Person)\nRETURN child-->(group:Group)<-[part_of:IS_PART_OF] WHERE part_of IS NOT NULL\n```"
    print(extract_cleaned_cypher(content))


def prepare_info_str(info: list[tuple[set, dict]]) -> str:
    info_str = ""
    for labels, data in info:
        info_str += f"\nLabel: {labels}"
        info_str += f"\nInfo: {data}"

    return info_str


def execute_cypher_query(query, params=None):
    """
    Executes a Cypher query and returns the result.
    """
    try:
        return db.cypher_query(query, params)
    except Exception:
        logging.error(query)
        raise


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
- Society
  - unique_id
  - name
- Group
  - unique_id
  - name
- Company
  - unique_id
  - name

Relationships:
- IS_SPOUSE_OF: Person - Person
- IS_PARENT_OF: Person -> Person
- IS_PART_OF: Person -> Group
- IS_OWNER_OF: Person -> Company
- HAS_COMMITTEE_MEMBER (position: string): Society -> Person

Indexes:
  - unique_id: Person, Society, Group, Company, HAS_COMMITTEE_MEMBER
"""
    return schema.strip()


def get_bi_der_relationships() -> str:
    bider_rel = ["`IS_SPOUSE_OF`"]
    return ", ".join(bider_rel)


if __name__ == "__main__":
    logging.basicConfig(level=logging.info)
    test_extract_cleaned_cypher()
