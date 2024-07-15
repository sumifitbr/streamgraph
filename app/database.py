from neo4j import GraphDatabase

class Neo4jDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def search_node(self, search_type, search_value):
        query = f"MATCH (n {{{search_type}: '{search_value}'}}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            return [record["n"] for record in result]

    def explore_node(self, node_id):
        query = f"MATCH (n)-[r]-(m) WHERE ID(n) = {node_id} RETURN n, r, m"
        with self.driver.session() as session:
            result = session.run(query)
            return [(record["n"], record["r"], record["m"]) for record in result]
