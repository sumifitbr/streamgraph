import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import random

# Inicializar st.session_state se necessário
if 'nodes' not in st.session_state:
    st.session_state['nodes'] = []
if 'edges' not in st.session_state:
    st.session_state['edges'] = []

# Função para adicionar um nó ao grafo
def add_node(node_id, node_label):
    st.session_state['nodes'].append(Node(id=node_id, label=node_label))

# Função para gerar uma cor aleatória
def random_color():
    r = lambda: random.randint(0,255)
    return f'#{r():02x}{r():02x}{r():02x}'

# Função para adicionar uma aresta ao grafo
def add_edge(source_id, target_id, label):
    color = random_color()
    st.session_state['edges'].append(Edge(source=source_id, target=target_id, label=label, color=color))

# Função para encontrar um nó pelo label
def find_node_by_label(label):
    for node in st.session_state['nodes']:
        if node.label == label:
            return node
    return None

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Inserção de Informação", "Visualização de Dados"])

if menu == "Inserção de Informação":
    st.title("Inserção de Informação")

    # Formulário para inserir nó
    with st.form(key='node_form'):
        node_id = st.text_input("ID do Nó")
        node_label = st.text_input("Label do Nó")
        submit_node = st.form_submit_button(label='Adicionar Nó')
        if submit_node:
            add_node(node_id, node_label)
            st.success(f"Nó {node_id} - {node_label} adicionado.")

    # Formulário para inserir aresta
    with st.form(key='edge_form'):
        source_label = st.text_input("Fonte da Aresta (Label do Nó)")
        target_label = st.text_input("Destino da Aresta (Label do Nó)")
        edge_label = st.text_input("Label da Aresta (Tecnologia)")
        submit_edge = st.form_submit_button(label='Adicionar Aresta')
        if submit_edge:
            source_node = find_node_by_label(source_label)
            target_node = find_node_by_label(target_label)
            if source_node and target_node:
                add_edge(source_node.id, target_node.id, edge_label)
                st.success(f"Aresta de {source_label} para {target_label} adicionada com label {edge_label}.")
            else:
                st.warning("Nó não encontrado. Verifique os labels dos nós.")

elif menu == "Visualização de Dados":
    st.title("Visualização de Dados")

    # Caixa de pesquisa para iniciar a visualização a partir de um nó específico
    start_node_label = st.sidebar.text_input("Iniciar visualização a partir do nó (label)")
    search_button = st.sidebar.button("Visualizar")

    if search_button:
        start_node = find_node_by_label(start_node_label)
        if start_node:
            # Configuração do grafo
            config = Config(width=800, height=600, directed=True, nodeHighlightBehavior=True, highlightColor="#F7A7A6",
                            collapsible=True, node={'color': 'lightblue', 'size': 400}, edge={'color': 'lightgray', 'width': 2},
                            heightMultiplier=2)

            # Filtrar nós e arestas para iniciar a visualização a partir do nó específico
            nodes_to_display = [start_node]
            edges_to_display = []
            for edge in st.session_state['edges']:
                if edge.source == start_node.id or edge.target == start_node.id:
                    edges_to_display.append(edge)
                    # Adicionar nós conectados às arestas encontradas
                    for node in st.session_state['nodes']:
                        if node.id == edge.source or node.id == edge.target:
                            if node not in nodes_to_display:
                                nodes_to_display.append(node)

            # Exibindo o grafo
            selected_node = agraph(nodes=nodes_to_display, edges=edges_to_display, config=config)

            # Manipular clique em um nó para exibir todas as arestas relacionadas
            if selected_node and 'event' in selected_node:
                clicked_node_id = selected_node['event']
                if clicked_node_id:
                    st.subheader(f"Arestas relacionadas ao nó {clicked_node_id}:")
                    related_edges = []
                    for edge in edges_to_display:
                        if edge.source == clicked_node_id or edge.target == clicked_node_id:
                            related_edges.append(edge)
                            st.write(f"- {edge.label} ({edge.source} -> {edge.target})")
                    if not related_edges:
                        st.write("Nenhuma aresta relacionada encontrada.")
            else:
                st.warning("Nenhum nó selecionado ou nenhum evento de clique encontrado.")
        else:
            st.warning("Nó não encontrado. Por favor, verifique o label do nó.")
