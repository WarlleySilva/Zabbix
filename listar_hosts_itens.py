import requests

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

# Função para obter os hosts desativados
def get_disabled_hosts(url, token):
    host_data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "host"],
            "filter": {
                "status": 1  # Filtragem para hosts desativados (0 para ativos)
            },
            "selectInterfaces": ["ip"],
            "auth": token,
            "id": 1
        },
        "auth": token,
        "id": 1
    }
    response = requests.post(url + 'api_jsonrpc.php', json=host_data)
    result = response.json()
    return result.get('result')

# Função para obter os itens não suportados e ativados de um host e escrever os IDs em um arquivo txt
def get_unsupported_and_enabled_items_and_write_ids(url, token, host_id, output_file):
    item_data = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["itemid"],
            "hostids": host_id,
            "filter": {
                "state": 1,  # Filtrar apenas itens com estado "not supported"
                "status": 0  # Filtrar apenas itens ativados (0 para ativado, 1 para desativado)
            },
            "auth": token,
            "id": 1
        },
        "auth": token,
        "id": 1
    }
    response = requests.post(url + 'api_jsonrpc.php', json=item_data)
    result = response.json().get('result')

    if result:
        with open(output_file, 'a') as file:
            for item in result:
                file.write(str(item['itemid']) + '\n')

# Função principal para executar o script
def main():
    # Informações de conexão com o Zabbix
    zabbix_url = "http://127.0.0.1/zabbix"
    username = "user"
    password = "password"

    # Autenticar na API do Zabbix
    token = authenticate_zabbix_api(zabbix_url, username, password)
    if token:
        # Obter os hosts desativados
        disabled_hosts = get_disabled_hosts(zabbix_url, token)

        # Iterar sobre os hosts desativados
        for host in disabled_hosts:
            host_id = host['hostid']
            #print(f"Nome: {host['host']}")
            # Obter itens não suportados e ativados e escrever os IDs em um arquivo txt
            output_file = f"/etc/zabbix/scripts/itens_not_suport/unsupported_items.txt"
            get_unsupported_and_enabled_items_and_write_ids(zabbix_url, token, host_id, output_file)
    else:
        print("Falha na autenticação. Verifique suas credenciais.")

if __name__ == "__main__":
    main()
