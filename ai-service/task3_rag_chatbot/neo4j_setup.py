"""
TASK 3: Xây dựng Knowledge Base Graph (KB_Graph) với Neo4j
- Create 500 User Nodes
- Create 150 Product Nodes  
- Create 8 Action Nodes
- Create Relationships: PERFORMED, ON
"""

import pandas as pd
import json
from neo4j import GraphDatabase
from datetime import datetime

class Neo4jKnowledgeGraph:
    def __init__(self, uri, user, password):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print(f"✅ Connected to Neo4j: {uri}")
    
    def close(self):
        """Close connection"""
        self.driver.close()
    
    def clear_database(self):
        """Clear all data from database"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("🗑️  Database cleared")
    
    def create_nodes(self):
        """Create all nodes (Users, Products, Actions)"""
        with self.driver.session() as session:
            # Create Users (500)
            print("\n📝 Creating User Nodes...")
            session.run("""
                UNWIND range(1, 500) AS i
                CREATE (:User {
                    user_id: 'U' + apoc.text.lpad(toString(i), 3, '0'),
                    created_at: datetime()
                })
            """)
            print("   ✓ 500 User nodes created")
            
            # Create Products (150)
            print("📝 Creating Product Nodes...")
            session.run("""
                UNWIND range(1, 150) AS i
                CREATE (:Product {
                    product_id: 'P' + apoc.text.lpad(toString(i), 3, '0'),
                    name: 'Product P' + apoc.text.lpad(toString(i), 3, '0'),
                    price: toFloat(apoc.number.parseInt(toString(i % 100)) + 50),
                    category: CASE i % 5 WHEN 0 THEN 'Laptop' WHEN 1 THEN 'Mobile' WHEN 2 THEN 'Clothing' WHEN 3 THEN 'Electronics' ELSE 'Accessories' END,
                    created_at: datetime()
                })
            """)
            print("   ✓ 150 Product nodes created")
            
            # Create Action nodes (8)
            print("📝 Creating Action Nodes...")
            actions = ["view", "click", "search", "share", "review", "wishlist", "add_to_cart", "purchase"]
            for action in actions:
                session.run(f"""
                    CREATE (:Action {{
                        action_type: '{action}',
                        label: '{action.upper()}'
                    }})
                """)
            print(f"   ✓ {len(actions)} Action nodes created")
            
            # Create Category nodes
            print("📝 Creating Category Nodes...")
            categories = ["Laptop", "Mobile", "Clothing", "Electronics", "Accessories"]
            for cat in categories:
                session.run(f"""
                    CREATE (:Category {{
                        category_name: '{cat}'
                    }})
                """)
            print(f"   ✓ {len(categories)} Category nodes created")
    
    def create_relationships(self, data_file="data/data_user500.csv"):
        """Create relationships from data"""
        print("\n🔗 Creating Relationships...")
        
        # Load data
        df = pd.read_csv(data_file)
        df = df.sort_values('timestamp')
        
        with self.driver.session() as session:
            # Create PERFORMED relationships
            print("   - Creating PERFORMED relationships...")
            for idx, row in df.iterrows():
                session.run("""
                    MATCH (u:User {user_id: $user_id})
                    MATCH (a:Action {action_type: $action})
                    CREATE (u)-[:PERFORMED {
                        timestamp: datetime($timestamp),
                        sequence_order: $order
                    }]->(a)
                """, {
                    "user_id": row['user_id'],
                    "action": row['action'],
                    "timestamp": row['timestamp'],
                    "order": idx
                })
            print(f"   ✓ {len(df)} PERFORMED relationships created")
            
            # Create ON relationships
            print("   - Creating ON relationships...")
            for idx, row in df.iterrows():
                session.run("""
                    MATCH (a:Action {action_type: $action})
                    MATCH (p:Product {product_id: $product_id})
                    CREATE (a)-[:ON]->(p)
                """, {
                    "action": row['action'],
                    "product_id": row['product_id']
                })
            print(f"   ✓ {len(df)} ON relationships created")
        
        # Create BELONGS_TO relationships
        print("   - Creating BELONGS_TO relationships...")
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Product)
                MATCH (c:Category {category_name: p.category})
                CREATE (p)-[:BELONGS_TO]->(c)
            """)
        print("   ✓ BELONGS_TO relationships created")
    
    def create_sample_queries_file(self):
        """Create sample Cypher queries"""
        queries = {
            "query_1": {
                "description": "Tìm khách hàng mua sản phẩm P121",
                "cypher": """
                MATCH (u:User)-[:PERFORMED]->(a:Action {action_type: 'purchase'})-[:ON]->(p:Product {product_id: 'P121'})
                RETURN u.user_id, u.created_at
                """
            },
            "query_2": {
                "description": "Tính số lượt view cho sản phẩm P115",
                "cypher": """
                MATCH (u:User)-[:PERFORMED]->(a:Action {action_type: 'view'})-[:ON]->(p:Product {product_id: 'P115'})
                RETURN COUNT(u) AS view_count
                """
            },
            "query_3": {
                "description": "Tìm các sản phẩm được mua nhiều nhất",
                "cypher": """
                MATCH (u:User)-[:PERFORMED]->(a:Action {action_type: 'purchase'})-[:ON]->(p:Product)
                RETURN p.product_id, p.name, COUNT(u) AS purchase_count
                ORDER BY purchase_count DESC
                LIMIT 10
                """
            },
            "query_4": {
                "description": "Tính user engagement score",
                "cypher": """
                MATCH (u:User)-[:PERFORMED]->(a:Action)-[:ON]->(p:Product)
                RETURN u.user_id, COUNT(a) AS action_count, COUNT(DISTINCT p) AS unique_products
                ORDER BY action_count DESC
                """
            },
            "query_5": {
                "description": "Phân tích hành vi phễu chuyển đổi",
                "cypher": """
                MATCH (u:User)-[:PERFORMED]->(a:Action)
                RETURN a.action_type, COUNT(DISTINCT u) AS user_count
                ORDER BY user_count DESC
                """
            }
        }
        
        with open("sample_queries.json", 'w', encoding='utf-8') as f:
            json.dump(queries, f, indent=2, ensure_ascii=False)
        print("✓ Sample queries saved: sample_queries.json")
    
    def get_statistics(self):
        """Get graph statistics"""
        with self.driver.session() as session:
            # Count nodes
            result = session.run("MATCH (n) RETURN labels(n)[0] AS label, COUNT(*) AS count")
            print("\n📊 Graph Statistics:")
            print("   Nodes:")
            total_nodes = 0
            for record in result:
                print(f"     - {record['label']}: {record['count']}")
                total_nodes += record['count']
            print(f"     - TOTAL: {total_nodes}")
            
            # Count relationships
            result = session.run("MATCH ()-[r]->() RETURN type(r) AS rel_type, COUNT(*) AS count")
            print("   Relationships:")
            total_rels = 0
            for record in result:
                print(f"     - {record['rel_type']}: {record['count']}")
                total_rels += record['count']
            print(f"     - TOTAL: {total_rels}")

def main():
    """Main setup"""
    print("=" * 70)
    print("🚀 TASK 3: Setup Neo4j Knowledge Base Graph")
    print("=" * 70)
    
    # Neo4j connection (local)
    URI = "bolt://localhost:7687"  # Default Neo4j port
    USER = "neo4j"
    PASSWORD = "password"
    
    try:
        kg = Neo4jKnowledgeGraph(URI, USER, PASSWORD)
        
        # Clear and create
        kg.clear_database()
        kg.create_nodes()
        kg.create_relationships(data_file="data/data_user500.csv")
        
        # Generate sample queries
        kg.create_sample_queries_file()
        
        # Get statistics
        kg.get_statistics()
        
        kg.close()
        
        print("\n" + "=" * 70)
        print("✅ TASK 3 COMPLETED - Knowledge Graph Created!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: Make sure Neo4j is running on localhost:7687")

if __name__ == "__main__":
    main()
