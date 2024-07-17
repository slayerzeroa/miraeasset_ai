from streamlit_agraph import agraph, Node, Edge, Config

def draw_graph_streamlit(customer_ids, pb_ids, connections):
    nodes = []

    # Customer 노드 추가
    for cid in customer_ids:
        nodes.append(Node(id=f"Customer_{cid}", label=f"Customer {cid}", size=25))

    # PB 노드 추가
    for pid in pb_ids:
        nodes.append(Node(id=f"PB_{pid}", label=f"PB {pid}", size=25))

    # Matching 결과로 연결 추가
    edges = []

    for connection in connections:
        customer, pb = connection
        edges.append(Edge(source=f"Customer_{customer}", target=f"PB_{pb}", label="assigned_to"))

    # 그래프 설정
    config = Config(width=750, height=950, directed=True, physics=True, hierarchical=True)

    # 그래프 생성
    return agraph(nodes=nodes, edges=edges, config=config)