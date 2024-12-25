GET_ADDITIONAL_INFO = """
The user asked the query
{user_query}
You have the information about the relevant nodes in the query
{info}

Write a Cypher query to answer the user's question from a large Neo4j knowledge graph. 
Make sure to properly use properties to only match relevant nodes and relationships to avoid ambiguity.
Use only the following schema:

{schema}

Only return the cypher query to retrieve data. Don't return anything else. Prefer unique_id to match the specific nodes
"""

GET_FINAL_ANSWER = """
The user asked the query
{user_query}
Given information about the relevant nodes
{info}
Cypher query used to fetch additional information
{cypher_query}
for the schema
{schema}

the query returned
{cypher_query_result}

Answer the user's query {user_query} in natural language based only on the above
"""