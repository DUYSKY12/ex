import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

SERVICES = {
    'customer': 'http://customer-service:8001',
    'staff': 'http://staff-service:8002',
    'laptop': 'http://laptop-service:8003',
    'mobile': 'http://mobile-service:8004',
    'clothes': 'http://clothes-service:8005',
    'product': 'http://product-service:8006',
    'ai': 'http://ai-service:8007',
}

def homepage(request):
    return render(request, 'homepage.html')

def login_page(request, role):
    return render(request, 'login.html', {'role': role})

def register_page(request):
    return render(request, 'register.html')

def customer_home(request):
    return render(request, 'customer/index.html')

def customer_profile(request):
    return render(request, 'customer/profile.html')

def customer_checkout(request):
    return render(request, 'customer/checkout.html')

def staff_dashboard(request):
    return render(request, 'staff/dashboard.html')

def api_products(request):
    try:
        laptops_resp = requests.get(f"{SERVICES['laptop']}/api/laptops", timeout=5)
        mobiles_resp = requests.get(f"{SERVICES['mobile']}/api/mobiles", timeout=5)
        clothes_resp = requests.get(f"{SERVICES['clothes']}/api/clothes", timeout=5)
        other_resp = requests.get(f"{SERVICES['product']}/api/v1/products", timeout=5)
        
        laptops = laptops_resp.json() if laptops_resp.status_code == 200 else []
        mobiles = mobiles_resp.json() if mobiles_resp.status_code == 200 else []
        clothes = clothes_resp.json() if clothes_resp.status_code == 200 else []
        other_data = other_resp.json().get('data', []) if other_resp.status_code == 200 else []
        
        return JsonResponse({'laptops': laptops, 'mobiles': mobiles, 'clothes': clothes, 'other': other_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ==================== TASK 5: Chat & Product Integration ====================

@csrf_exempt
def products_list(request):
    """
    TASK 5: Display all products with filter & search
    """
    if request.method == 'GET':
        category = request.GET.get('category')
        sort_by = request.GET.get('sort_by', 'popularity')
        
        try:
            # Get recommendations from AI Service
            ai_url = f"{SERVICES['ai']}/api/recommend"
            params = {'sort_by': sort_by, 'limit': 50}
            if category:
                params['category'] = category
            
            resp = requests.get(ai_url, params=params, timeout=5)
            
            if resp.status_code == 200:
                data = resp.json()
                products = data.get('products', [])
            else:
                products = []
            
            return render(request, 'products.html', {
                'products': products,
                'category': category,
                'sort_by': sort_by
            })
        
        except Exception as e:
            return render(request, 'products.html', {
                'error': f"Error loading products: {str(e)}",
                'products': []
            })

@csrf_exempt
def product_detail(request, product_id):
    """
    TASK 5: Get product details from Neo4j
    """
    try:
        resp = requests.get(
            f"{SERVICES['ai']}/api/products/{product_id}",
            timeout=5
        )
        
        if resp.status_code == 200:
            product = resp.json().get('product')
        else:
            product = None
        
        return render(request, 'product_detail.html', {'product': product})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def chat_interface(request):
    """
    TASK 5: Render chat interface page
    """
    return render(request, 'chat.html')

@csrf_exempt
def api_chat(request):
    """
    TASK 4 & 5: Chat endpoint (forward to AI Service)
    
    Request:
    {
        "query": "Có bao nhiêu khách hàng mua sản phẩm P121?",
        "user_id": "U001",
        "product_id": "P121"
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        body = json.loads(request.body)
        query = body.get('query')
        
        if not query:
            return JsonResponse({'error': 'query parameter required'}, status=400)
        
        # Forward to AI Service
        resp = requests.post(
            f"{SERVICES['ai']}/api/chat",
            json=body,
            timeout=10
        )
        
        if resp.status_code == 200:
            return JsonResponse(resp.json())
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'AI Service error',
                'details': resp.text
            }, status=resp.status_code)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_track_action(request):
    """
    TASK 5: Track user action (view, click, add_to_cart, etc.)
    
    Request:
    {
        "user_id": "U001",
        "product_id": "P121",
        "action": "add_to_cart",
        "timestamp": "2026-04-21 10:30:45"
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        body = json.loads(request.body)
        
        required_fields = ['user_id', 'product_id', 'action']
        if not all(field in body for field in required_fields):
            return JsonResponse({'error': f'Missing required fields: {required_fields}'}, status=400)
        
        # Forward to AI Service
        resp = requests.post(
            f"{SERVICES['ai']}/api/track",
            json=body,
            timeout=5
        )
        
        if resp.status_code == 200:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Tracking failed'
            }, status=500)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_get_recommendations(request):
    """
    TASK 5: Get product recommendations
    
    Query params:
    - category: str (optional)
    - sort_by: str (default: 'popularity')
    - limit: int (default: 10)
    """
    try:
        category = request.GET.get('category')
        sort_by = request.GET.get('sort_by', 'popularity')
        limit = request.GET.get('limit', 10)
        
        params = {'sort_by': sort_by, 'limit': limit}
        if category:
            params['category'] = category
        
        resp = requests.get(
            f"{SERVICES['ai']}/api/recommend",
            params=params,
            timeout=5
        )
        
        if resp.status_code == 200:
            return JsonResponse(resp.json())
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to get recommendations'
            }, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_get_statistics(request):
    """
    TASK 5: Get system statistics from Neo4j
    """
    try:
        resp = requests.get(
            f"{SERVICES['ai']}/api/stats",
            timeout=5
        )
        
        if resp.status_code == 200:
            return JsonResponse(resp.json())
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to get statistics'
            }, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def api_search(request):
    query = request.GET.get('q', '')
    try:
        laptops_resp = requests.get(f"{SERVICES['laptop']}/api/laptops?q={query}", timeout=5)
        mobiles_resp = requests.get(f"{SERVICES['mobile']}/api/mobiles?q={query}", timeout=5)
        clothes_resp = requests.get(f"{SERVICES['clothes']}/api/clothes?q={query}", timeout=5)
        
        laptops = laptops_resp.json() if laptops_resp.status_code == 200 else []
        mobiles = mobiles_resp.json() if mobiles_resp.status_code == 200 else []
        clothes = clothes_resp.json() if clothes_resp.status_code == 200 else []
        
        return JsonResponse({'laptops': laptops, 'mobiles': mobiles, 'clothes': clothes, 'other': []})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def proxy_view(request, service, endpoint):
    if service not in SERVICES:
        return JsonResponse({'error': 'Service not found'}, status=404)

    url = f"{SERVICES[service]}/{endpoint}"
    method = request.method
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ['host', 'content-length', 'content-type']
    }

    try:
        if method == 'GET':
            resp = requests.get(url, params=request.GET, headers=headers, timeout=10)
        elif method == 'POST':
            body = json.loads(request.body) if request.body else {}
            resp = requests.post(url, json=body, headers=headers, timeout=10)
        elif method == 'PUT':
            body = json.loads(request.body) if request.body else {}
            resp = requests.put(url, json=body, headers=headers, timeout=10)
        elif method == 'DELETE':
            resp = requests.delete(url, headers=headers, timeout=10)
        else:
            return JsonResponse({'error': 'Method not supported'}, status=405)

        # Use HttpResponse with json.dumps to support both lists AND dicts
        response_data = resp.json()
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json',
            status=resp.status_code
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
