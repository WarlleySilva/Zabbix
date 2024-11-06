import requests
import json

# Função para autenticar e obter o token de autenticação
def authenticate_zabbix_api(url, user, passwd):
    auth_data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": user,
            "password": passwd
        },
        "id": 1,
        "auth": None
    }
    response = requests.post(url + 'api_jsonrpc.php', json=auth_data)
    result = response.json()
    return result.get('result')

# Função para desativar um item pelo ID
def disable_item(url, token, item_id):
    item_data = {
        "jsonrpc": "2.0",
        "method": "item.update",
        "params": {
            "itemid": item_id,
            "status": 1  # 1 para desativar o item
        },
        "auth": token,
        "id": 1
    }
    response = requests.post(url + 'api_jsonrpc.php', json=item_data)
    result = response.json()
    return result.get('result')

# Função principal para executar o script
def main():
    # Informações de conexão com o Zabbix
    zabbix_url = "http://127.0.0.1/zabbix"
    username = "user"
    password = "password"

    # Autenticar na API do Zabbix
    token = authenticate_zabbix_api(zabbix_url, username, password)
    if token:
        # Ler os IDs dos itens a serem desativados do arquivo
        try:
            with open('/etc/zabbix/scripts/itens_not_suport/unsupported_items.txt', 'r') as file:
                item_ids = [line.strip() for line in file if line.strip()]
        except IOError:
            print("Falha ao ler o arquivo de itens não suportados.")
            return

        # Desativar cada item
        for item_id in item_ids:
            result = disable_item(zabbix_url, token, item_id)
            if result:
                print(f"Item {item_id} desativado com sucesso.")
            else:
                print(f"Falha ao desativar o item {item_id}.")

    else:
        print("Falha na autenticação. Verifique suas credenciais.")

if __name__ == "__main__":
    main()
