import urllib.request
import urllib.error
import json

print("=" * 60)
print("TESTE DE LOGIN VIA API")
print("=" * 60)

url = "http://localhost:8000/api/auth/login/"
data = {
    "username": "admin",
    "password": "admin123"
}

print(f"\nURL: {url}")
print(f"Dados: {json.dumps(data, indent=2)}")
print("\nEnviando requisição...")

try:
    # Preparar requisição
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={'Content-Type': 'application/json'}
    )
    
    # Enviar requisição
    with urllib.request.urlopen(req, timeout=5) as response:
        status_code = response.status
        response_data = json.loads(response.read().decode('utf-8'))
        
        print(f"\nStatus Code: {status_code}")
        
        if status_code == 200:
            print("\n✓ LOGIN BEM-SUCEDIDO!")
            print(f"\nTokens recebidos:")
            print(f"  Access Token: {response_data.get('access', 'N/A')[:50]}...")
            print(f"  Refresh Token: {response_data.get('refresh', 'N/A')[:50]}...")
        else:
            print(f"\n✗ LOGIN FALHOU!")
            print(f"Response: {response_data}")
        
except urllib.error.URLError as e:
    print("\n✗ ERRO: Não foi possível conectar ao servidor!")
    print("  O servidor Django está rodando em http://localhost:8000?")
    print("\n  Para iniciar o servidor, execute:")
    print("  cd backend")
    print("  .\\venv\\Scripts\\activate")
    print("  python manage.py runserver")
    print(f"\n  Erro: {e}")
    
except urllib.error.HTTPError as e:
    print(f"\n✗ LOGIN FALHOU!")
    print(f"Status Code: {e.code}")
    print(f"Response: {e.read().decode('utf-8')}")
    
except Exception as e:
    print(f"\n✗ ERRO: {e}")

print("=" * 60)
