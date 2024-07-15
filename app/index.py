import streamlit as st
from streamlit_agraph import agraph, Config, Node, Edge
from database import Neo4jDatabase
import os

# Variaveis
NEO4J_USERNAME='neo4j'
NEO4J_PASSWORD='7R6dC5XNfYjKOJVAy1zdk_I5nlFqZ4qHKFbiihykq3I'
AURA_INSTANCEID='f9d70cee'

# Carregar configurações do Neo4j AuraDB a partir de variáveis de ambiente
neo4j_url = os.getenv(f"NEO4J_URL", "neo4j+s://{AURA_INSTANCEID}.databases.neo4j.io")
neo4j_user = os.getenv(f"NEO4J_USER", "{NEO4J_USERNAME}")
neo4j_password = os.getenv(f"NEO4J_PASSWORD", "{NEO4J_PASSWORD}")

# Inicializar a conexão com o banco de dados
db = Neo4jDatabase(neo4j_url, neo4j_user, neo4j_password)

# Interface do Streamlit
st.set_page_config(layout="wide")

st.title("Explorador de Nodes Neo4j")

# Campo de pesquisa central
search_type = st.selectbox("Escolha o tipo de pesquisa", ["CNPJ", "CPF"])
search_value = st.text_input("Digite o valor de pesquisa")

if st.button("Pesquisar"):
    nodes = db.search_node(search_type, search_value)
    if nodes:
        st.write(f"Foram encontrados {len(nodes)} nodes")
        for node in nodes:
            st.write(node)
    else:
        st.write("Nenhum node encontrado.")

# Função para desenhar o grafo
def draw_graph(nodes, edges):
    config = Config(width=800, height=600, directed=True, physics=True, hierarchical=False)
    return_value = agraph(nodes=nodes, edges=edges, config=config)
    return return_value

# Exibir o grafo
if 'nodes' in locals() and nodes:
    st.write("Explorando o node:")
    node_id = st.selectbox("Escolha o node para explorar", [node.id for node in nodes])
    if st.button("Explorar"):
        relationships = db.explore_node(node_id)
        graph_nodes = [Node(id=str(node.id), label=node["name"]) for node, _, _ in relationships]
        graph_edges = [Edge(source=str(node.id), target=str(m.id), label=r.type) for node, r, m in relationships]
        draw_graph(graph_nodes, graph_edges)

# Mudança de background
bg_color = st.color_picker("Escolha a cor de fundo")
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: {bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)
