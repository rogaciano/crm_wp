import urllib.request
import urllib.error
import json

print("=" * 60)
print("TESTE COMPLETO DE LOGIN + FETCH USER")
print("=" * 60)

# Passo 1: Login
print("\n[1] Fazendo login...")
url_login = "http://localhost:8000/api/auth/login/"
data = {
    "username": "admin",
    "password": "admin123"
}

try:
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(
        url_login,
        data=json_data,
        headers={'Content-Type': 'application/json'}
    )
    
    with urllib.request.urlopen(req, timeout=5) as response:
        login_data = json.loads(response.read().decode('utf-8'))
        access_token = login_data.get('access')
        
        print(f"✓ Login bem-sucedido!")
        print(f"  Access Token: {access_token[:50]}...")
        
        # Passo 2: Buscar dados do usuário
        print("\n[2] Buscando dados do usuário (/usuarios/me/)...")
        url_me = "http://localhost:8000/api/usuarios/me/"
        
        req_me = urllib.request.Request(
            url_me,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        try:
            with urllib.request.urlopen(req_me, timeout=5) as response_me:
                user_data = json.loads(response_me.read().decode('utf-8'))
                
                print(f"✓ Dados do usuário obtidos com sucesso!")
                print(f"\nDados do usuário:")
                print(json.dumps(user_data, indent=2, ensure_ascii=False))
                
        except urllib.error.HTTPError as e:
            print(f"✗ ERRO ao buscar dados do usuário!")
            print(f"Status Code: {e.code}")
            error_body = e.read().decode('utf-8')
            print(f"Response: {error_body}")
            
            if e.code == 404:
                print("\n⚠ PROBLEMA IDENTIFICADO:")
                print("  O endpoint /usuarios/me/ não existe ou não está configurado corretamente")
                print("  Verifique se a rota está registrada no router")
        
except urllib.error.HTTPError as e:
    print(f"✗ ERRO no login!")
    print(f"Status Code: {e.code}")
    print(f"Response: {e.read().decode('utf-8')}")
    
except urllib.error.URLError as e:
    print(f"✗ ERRO: Servidor não está respondendo!")
    print(f"  Erro: {e}")
    
except Exception as e:
    print(f"✗ ERRO: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
