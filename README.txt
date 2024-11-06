**Guia de Uso dos Scripts para Gerenciamento de Itens do Zabbix**

Esses dois scripts Python foram projetados para interagir com a API do Zabbix, com o objetivo de identificar e gerenciar itens não suportados em hosts desativados. O primeiro script lista e grava IDs dos itens não suportados e ativados em um arquivo, enquanto o segundo script desativa esses itens utilizando os IDs listados. A seguir, vamos detalhar o funcionamento e a execução de cada script.

---

### Pré-requisitos

- Ter o Python instalado em sua máquina.
- Instalar a biblioteca `requests` para fazer as chamadas à API. Execute no terminal:
  ```bash
  pip install requests
  ```
- Ter acesso à API do Zabbix e permissão para realizar operações nos itens e hosts.

---

### Script 1: Listagem de Itens Não Suportados e Ativados em Hosts Desativados

Este script autentica na API do Zabbix, identifica hosts desativados, filtra itens ativados e não suportados, e grava seus IDs em um arquivo de texto.

#### Passo a Passo

1. **Autenticação**: A função `authenticate_zabbix_api` autentica na API do Zabbix e obtém o token necessário para as operações.

2. **Listagem de Hosts Desativados**: A função `get_disabled_hosts` faz uma solicitação para buscar hosts desativados (ou seja, aqueles com `status` definido como `1`).

3. **Filtragem e Gravação de Itens**: Para cada host desativado, o script busca itens ativados (`status: 0`) e não suportados (`state: 1`) através da função `get_unsupported_and_enabled_items_and_write_ids`. Os IDs desses itens são gravados em um arquivo no diretório `/etc/zabbix/scripts/itens_not_suport/unsupported_items.txt`.

4. **Execução**: O script executa essas etapas ao chamar a função `main`.

#### Execução do Script 1

Salve o script como `script_1.py` e execute-o:

```bash
python script_1.py
```

### Script 2: Desativação dos Itens Listados

Este script autentica na API do Zabbix, lê os IDs dos itens gravados pelo Script 1, e desativa esses itens.

#### Passo a Passo

1. **Autenticação**: A função `authenticate_zabbix_api` é chamada novamente para autenticar na API e obter o token.

2. **Leitura dos IDs de Itens**: O script lê o arquivo `/etc/zabbix/scripts/itens_not_suport/unsupported_items.txt` e carrega os IDs dos itens a serem desativados.

3. **Desativação dos Itens**: Para cada ID, a função `disable_item` altera o `status` do item para `1` (desativado).

4. **Execução**: A função `main` realiza a leitura e desativação dos itens listados.

#### Execução do Script 2

Salve o script como `script_2.py` e execute-o:

```bash
python script_2.py
```

---

### Observações Importantes

- **Ordem de Execução**: Execute o Script 1 antes do Script 2, pois o segundo script depende do arquivo de IDs gerado pelo primeiro.
- **Validação de Acesso**: Verifique se você possui acesso para autenticar e manipular itens e hosts pela API do Zabbix.
- **Caminho do Arquivo**: Certifique-se de que o diretório `/etc/zabbix/scripts/itens_not_suport/` exista e tenha permissões de escrita, pois é lá que o arquivo `unsupported_items.txt` será salvo.
- **Mensagens de Erro**: Caso ocorram erros de autenticação ou leitura, o script exibirá mensagens para facilitar a resolução de problemas.

Esses scripts fornecem uma solução automatizada para identificar e desativar itens problemáticos, ajudando a manter um ambiente de monitoramento mais eficiente e livre de alertas irrelevantes.