# WVR API

API hub para ferramentas de OSINT e Cybersecurity utilizando FastAPI. Atualmente suporta execuções do Nmap, busca de subdomínios com Sublist3r e permite gerenciar chaves de acesso por meio de API keys.

## Executando com Docker

```bash
# build da imagem
docker build -t wvr-api .

# executa container
docker run -p 8000:8000 -e ADMIN_TOKEN=meutoken wvr-api
```

A API estará disponível em `http://localhost:8000`. Utilize o token definido em
`ADMIN_TOKEN` para gerar chaves via endpoint `/api/v1/apikeys`.

### Variáveis de ambiente

- `ADMIN_TOKEN`: token administrativo necessário para criar novas API keys.
- `DATABASE_URL`: URL de conexão com o banco (padrão `sqlite:///./app.db`).

## Endpoints Principais

### POST `/api/v1/apikeys`

Gera uma nova API key. Requer que o parâmetro `admin_token` seja igual ao
valor definido na variável de ambiente `ADMIN_TOKEN`.

Parâmetros (query):

- `owner` (**obrigatório**) &mdash; identificação de quem está criando a chave.
- `admin_token` (**obrigatório**) &mdash; token administrativo.

Exemplo:

```bash
curl -X POST "http://localhost:8000/api/v1/apikeys?owner=teste&admin_token=meutoken"
```

Resposta:

```json
{"api_key": "<nova-chave>"}
```

### POST `/api/v1/nmap/scan`

Executa um scan Nmap. É necessário enviar a API key no cabeçalho
`Authorization: Bearer <API_KEY>`.

Parâmetros (query):

- `target` (**obrigatório**) &mdash; IP ou host a ser escaneado.
- `options` (opcional) &mdash; opções da linha de comando do Nmap.

Exemplo:

```bash
curl -X POST "http://localhost:8000/api/v1/nmap/scan?target=scanme.nmap.org&options=-sV" \
  -H "Authorization: Bearer <API_KEY>"
```

Resposta:

```json
{"scan_id": 1, "result": "...saída do nmap..."}
```

### GET `/api/v1/nmap/scan/{scan_id}`

Retorna o resultado de um scan previamente executado. Também requer a API key
no cabeçalho `Authorization`.

Parâmetros:

- `scan_id` (path) &mdash; identificador numérico do scan.

Exemplo:

```bash
curl "http://localhost:8000/api/v1/nmap/scan/1" \
  -H "Authorization: Bearer <API_KEY>"
```

Resposta:

```json
{
  "scan_id": 1,
  "target": "scanme.nmap.org",
  "options": "-sV",
  "result": "...saída do nmap..."
}
```


### POST `/api/v1/subdomains/scan`

Executa uma enumeração de subdomínios utilizando o Sublist3r. É necessário enviar a API key no cabeçalho `Authorization: Bearer <API_KEY>`.

Parâmetros (query):

- `domain` (**obrigatório**) &mdash; domínio a ser pesquisado.

Exemplo:

```bash
curl -X POST "http://localhost:8000/api/v1/subdomains/scan?domain=example.com" \
  -H "Authorization: Bearer <API_KEY>"
```

Resposta:

```json
{
  "domain": "example.com",
  "subdomains": ["www.example.com", "blog.example.com"]
}
```
