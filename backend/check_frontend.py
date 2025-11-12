import urllib.request
import urllib.error

print("Verificando se o frontend está rodando...")

try:
    with urllib.request.urlopen('http://localhost:5173', timeout=2) as response:
        print(f"✅ Frontend está rodando em http://localhost:5173")
        print(f"Status: {response.status}")
except urllib.error.URLError as e:
    print(f"❌ Frontend NÃO está rodando em http://localhost:5173")
    print(f"Erro: {e}")
    print("\nPara iniciar o frontend:")
    print("  cd frontend")
    print("  npm run dev")
