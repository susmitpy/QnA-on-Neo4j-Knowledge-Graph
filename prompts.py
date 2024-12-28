GET_ADDITIONAL_INFO = """
The user asked the query:
{user_query}

You have the information about the relevant nodes in the query:
{info}

Write a Cypher query to answer the user's question from a large Neo4j knowledge graph.

Use the following schema:
{schema}

Make sure to:
- Match nodes and relationships precisely using their properties and the schema.
- For relationships like {bidir_rels}, which are inherently bidirectional, ensure your query accounts for both directions by using an undirected relationship pattern (`-[:REL]-`) to avoid missing data.
- Avoid unnecessary or ambiguous matches. Use properties such as `unique_id` to target specific nodes and ensure accuracy.
- Use only the Labels and relationships specified in the schema. Do not include any additional or unsupported labels or relationships.
- Only return the Cypher query to retrieve the data, and do not include explanations or any additional output.

"""

GET_FINAL_ANSWER = """
The user asked the query:
{user_query}

Given information about the relevant nodes:
{info}

Cypher query used to fetch additional information:
{cypher_query}

For the schema:
{schema}

The query returned:
{cypher_query_result}

Answer the user's query:

- Provide a concise, human-friendly response based only on the query result.
- For relationships like {bidir_rels}, which are inherently bidirectional, ensure you use the data as undirected and account for both directions in the context of the result.
- Base your answer strictly on the provided schema, query result, and context. Avoid adding assumptions or external information.
"""