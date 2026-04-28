"""
TASK 4 & 5: FastAPI Endpoints for GraphRAG Chatbot
- POST /api/chat - Chat with AI
- POST /api/track - Track user actions in Neo4j
- GET /api/recommend - Get product recommendations
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Optional
from datetime import datetime
import json
import os
from rag_pipeline import GraphRAGPipeline
from neo4j import GraphDatabase

app = FastAPI(
    title="E-commerce AI Chatbot API",
    description="GraphRAG-powered AI Assistant for E-commerce",
    version="1.0.0"
)

# ==================== Configuration ====================
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-dummy")

# ==================== Initialize ====================
print("🚀 Initializing E-commerce AI Chatbot API...")

try:
    rag_pipeline = GraphRAGPipeline(
        neo4j_uri=NEO4J_URI,
        neo4j_user=NEO4J_USER,
        neo4j_password=NEO4J_PASSWORD,
        openai_api_key=OPENAI_API_KEY
    )
    print("✅ GraphRAG Pipeline initialized")
except Exception as e:
    print(f"❌ Error initializing GraphRAG: {e}")
    rag_pipeline = None

# ==================== Models ====================
class ChatRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    product_id: Optional[str] = None

class TrackActionRequest(BaseModel):
    user_id: str
    product_id: str
    action: str  # view, click, search, add_to_cart, review, wishlist, purchase, share
    timestamp: Optional[str] = None

class ChatResponse(BaseModel):
    status: str
    query: str
    answer: str
    cypher_query: Optional[str] = None
    confidence: Optional[float] = None
    processing_time_ms: Optional[float] = None

# ==================== Endpoints ====================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "E-commerce AI Chatbot",
        "version": "1.0.0"
    }

@app.post("/api/chat", response_model=dict)
async def chat_endpoint(req: ChatRequest):
    """
    Chat with AI Assistant
    
    Example:
    {
        "query": "Có bao nhiêu khách hàng mua sản phẩm P121?",
        "user_id": "U001",
        "product_id": "P121"
    }
    """
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="GraphRAG service unavailable")
    
    try:
        import time
        start_time = time.time()
        
        # Query GraphRAG
        response = rag_pipeline.query(req.query)
        
        processing_time = (time.time() - start_time) * 1000
        response['processing_time_ms'] = processing_time
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/track")
async def track_action(req: TrackActionRequest):
    """
    Track user action in Neo4j
    
    Example:
    {
        "user_id": "U001",
        "product_id": "P121",
        "action": "add_to_cart",
        "timestamp": "2026-04-21 10:30:45"
    }
    """
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="GraphRAG service unavailable")
    
    try:
        timestamp = req.timestamp or datetime.now().isoformat()
        
        # Execute Cypher to create relationship
        cypher_query = f"""
        MATCH (u:User {{user_id: '{req.user_id}'}})
        MATCH (a:Action {{action_type: '{req.action}'}})
        MATCH (p:Product {{product_id: '{req.product_id}'}})
        CREATE (u)-[:PERFORMED {{timestamp: '{timestamp}'}}]->(a)
        CREATE (a)-[:ON]->(p)
        """
        
        result = rag_pipeline.direct_cypher_query(cypher_query)
        
        return {
            "status": "success",
            "user_id": req.user_id,
            "product_id": req.product_id,
            "action": req.action,
            "timestamp": timestamp
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommend")
async def get_recommendations(
    category: Optional[str] = None,
    sort_by: str = "popularity",
    limit: int = 10
):
    """
    Get product recommendations from Neo4j
    
    Example: /api/recommend?category=Laptop&sort_by=popularity&limit=5
    """
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="GraphRAG service unavailable")
    
    try:
        if category:
            cypher_query = f"""
            MATCH (p:Product)-[:BELONGS_TO]->(c:Category {{category_name: '{category}'}})
            MATCH (u:User)-[:PERFORMED]->(a:Action {{action_type: 'purchase'}})-[:ON]->(p)
            RETURN p.product_id, p.name, p.price, COUNT(u) AS purchase_count
            ORDER BY purchase_count DESC
            LIMIT {limit}
            """
        else:
            cypher_query = f"""
            MATCH (u:User)-[:PERFORMED]->(a:Action {{action_type: 'purchase'}})-[:ON]->(p:Product)
            RETURN p.product_id, p.name, p.price, COUNT(u) AS purchase_count
            ORDER BY purchase_count DESC
            LIMIT {limit}
            """
        
        results = rag_pipeline.direct_cypher_query(cypher_query)
        
        return {
            "status": "success",
            "category": category,
            "sort_by": sort_by,
            "limit": limit,
            "products": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products/{product_id}")
async def get_product_detail(product_id: str):
    """Get product details from Neo4j"""
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="GraphRAG service unavailable")
    
    try:
        cypher_query = f"""
        MATCH (p:Product {{product_id: '{product_id}'}})
        OPTIONAL MATCH (p)-[:BELONGS_TO]->(c:Category)
        OPTIONAL MATCH (u:User)-[:PERFORMED]->(a:Action {{action_type: 'purchase'}})-[:ON]->(p)
        RETURN p.product_id, p.name, p.price, c.category_name AS category, COUNT(u) AS purchase_count
        """
        
        results = rag_pipeline.direct_cypher_query(cypher_query)
        
        if not results:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        
        return {
            "status": "success",
            "product": results[0]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_statistics():
    """Get graph statistics"""
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="GraphRAG service unavailable")
    
    try:
        queries = {
            "total_users": "MATCH (u:User) RETURN COUNT(u)",
            "total_products": "MATCH (p:Product) RETURN COUNT(p)",
            "total_interactions": "MATCH (u:User)-[:PERFORMED]->() RETURN COUNT(*)",
            "total_purchases": "MATCH (u:User)-[:PERFORMED]->(a:Action {action_type: 'purchase'}) RETURN COUNT(DISTINCT u)"
        }
        
        stats = {}
        for key, query in queries.items():
            result = rag_pipeline.direct_cypher_query(query)
            if result:
                stats[key] = list(result[0].values())[0]
        
        return {
            "status": "success",
            "statistics": stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/docs")
async def api_docs():
    """API Documentation"""
    return {
        "service": "E-commerce AI Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/chat": "Chat with AI (GraphRAG)",
            "POST /api/track": "Track user action",
            "GET /api/recommend": "Get recommendations",
            "GET /api/products/{id}": "Get product detail",
            "GET /api/stats": "Get statistics"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)

            "answer": answer
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chạy với lệnh: uvicorn task3_rag_chatbot.main_api:app --host 0.0.0.0 --port 8007 --reload
