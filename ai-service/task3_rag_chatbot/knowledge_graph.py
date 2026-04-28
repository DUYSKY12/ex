import networkx as nx
import matplotlib.pyplot as plt

def build_knowledge_graph():
    """ Xây dựng Knowledge Graph cho 10 sản phẩm mẫu """
    G = nx.DiGraph()

    # Thêm Node Category
    categories = ["Laptop", "Mobile", "Clothing", "Electronics"]
    for cat in categories:
        G.add_node(cat, type="Category")

    # Mocks 10 products
    products = [
        {"id": "P1", "name": "MacBook Pro M3", "category": "Laptop", "brand": "Apple", "price_range": "High"},
        {"id": "P2", "name": "Dell XPS 15", "category": "Laptop", "brand": "Dell", "price_range": "High"},
        {"id": "P3", "name": "ThinkPad X1", "category": "Laptop", "brand": "Lenovo", "price_range": "High"},
        {"id": "P4", "name": "iPhone 15 Pro Max", "category": "Mobile", "brand": "Apple", "price_range": "High"},
        {"id": "P5", "name": "Galaxy S24 Ultra", "category": "Mobile", "brand": "Samsung", "price_range": "High"},
        {"id": "P6", "name": "Pixel 8 Pro", "category": "Mobile", "brand": "Google", "price_range": "Medium"},
        {"id": "P7", "name": "Nike Running T-Shirt", "category": "Clothing", "brand": "Nike", "price_range": "Low"},
        {"id": "P8", "name": "Adidas Hoodie", "category": "Clothing", "brand": "Adidas", "price_range": "Low"},
        {"id": "P9", "name": "Levi's 501 Jeans", "category": "Clothing", "brand": "Levis", "price_range": "Medium"},
        {"id": "P10", "name": "Sony WH-1000XM5", "category": "Electronics", "brand": "Sony", "price_range": "Medium"},
    ]

    for p in products:
        # Node sản phẩm
        G.add_node(p["id"], name=p["name"], type="Product")
        
        # Node Brand (nếu chưa có tự động sinh)
        G.add_node(p["brand"], type="Brand")
        
        # Thêm Edge quan hệ
        G.add_edge(p["id"], p["category"], relation="BELONGS_TO_CATEGORY")
        G.add_edge(p["id"], p["brand"], relation="HAS_BRAND")
        G.add_edge(p["id"], p["price_range"], relation="HAS_PRICE_RANGE")

    print(f"Khởi tạo xong KG. Tổng số Node: {G.number_of_nodes()}, Tổng số cạnh: {G.number_of_edges()}")
    return G

def search_kg(graph, entity_name):
    """ Hàm truy xuất đồ thị đơn giản để bổ sung thông tin cho RAG """
    # Tìm node có name khớp
    node_id = None
    for n, data in graph.nodes(data=True):
        if data.get('name', '').lower() == entity_name.lower():
            node_id = n
            break
            
    if not node_id:
        return "Không tìm thấy thông tin trên Knowledge Graph."

    neighbors = list(graph.successors(node_id))
    relationships = []
    for neighbor in neighbors:
        edge_data = graph.get_edge_data(node_id, neighbor)
        relationships.append(f"{edge_data['relation']} {neighbor}")
        
    return f"Sản phẩm {entity_name} có quan hệ: " + ", ".join(relationships)

if __name__ == "__main__":
    kg = build_knowledge_graph()
    print(search_kg(kg, "Dell XPS 15"))
