# Star Wars API Explorer

API FastAPI que consome a Star Wars API (SWAPI) e retorna dados customizados e enriquecidos.

## Sobre

Aplicação Python que funciona como intermediária para a [SWAPI](https://swapi.dev/). Transforma dados brutos em respostas estruturadas com informações enriquecidas sobre personagens, filmes, planetas, espécies, naves e veículos. Construída com foco em performance (requisições assíncronas e caching) e pronta para produção em Google Cloud Platform.

## Características

- Endpoints para todos os recursos da SWAPI (People, Films, Planets, Species, Starships, Vehicles)
- Dados enriquecidos consolidando informações relacionadas
- Cache inteligente (24h) e requisições assíncronas
- Documentação interativa (Swagger em `/docs`)
- Validação de dados com Pydantic
- Health check para monitoramento
- Deploy em Google Cloud Functions Gen2

## Tecnologias

- Python 3.12.5+, uv, FastAPI, Pydantic, aiohttp, Uvicorn, Google Cloud Functions

## Instalação e Execução

### 1. Clonar e instalar dependências
```bash
git clone https://github.com/kaelkkd/powerofdata-swapi.git
cd powerofdata-swapi
```
O uso do [uv](https://github.com/astral-sh/uv) é recomendado, porém, a aplicação pode ser executada sem o mesmo.
```bash
uv venv

#Ative o venv
source .venv/bin/activate    #Linux ou Mac
.venv\Scripts\activate       #Windows

uv sync
```


### 2. Executar localmente

```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Acessar

- API: http://localhost:8000/
- Documentação: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Exemplos de Uso

```bash
# Listar personagens
curl http://localhost:8000/people?page=1

# Buscar personagem por ID
curl http://localhost:8000/people/1

# Listar filmes
curl http://localhost:8000/films?page=1

# Buscar filme por ID
curl http://localhost:8000/films/1
```

Mesma estrutura para: `/planets/{id}`, `/species/{id}`, `/starships/{id}`, `/vehicles/{id}`

## Estrutura de Respostas

### Resposta de Personagem Enriquecida

```json
{
  "id": 1,
  "name": "Luke Skywalker",
  "height": 172,
  "mass": 77.0,
  "appearance": {
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color": "blue"
  },
  "birth_year": "19BBY",
  "gender": "male",
  "homeworld": {
    "id": 1,
    "name": "Tatooine",
    "climate": "arid",
    "terrain": "desert"
  },
  "films": [
    {
      "id": 1,
      "title": "A New Hope",
      "episode_id": 4,
      "release_date": "1977-05-25"
    }
  ],
  "statistics": {
    "films_count": 5,
    "species_count": 1,
    "starships_count": 2,
    "vehicles_count": 2
  }
}
```

## Endpoints

| Recurso | Listagem | Detalhe |
|---------|----------|---------|
| Personagens | GET `/people?page=1` | GET `/people/{id}` |
| Filmes | GET `/films?page=1` | GET `/films/{id}` |
| Planetas | GET `/planets?page=1` | GET `/planets/{id}` |
| Espécies | GET `/species?page=1` | GET `/species/{id}` |
| Naves | GET `/starships?page=1` | GET `/starships/{id}` |
| Veículos | GET `/vehicles?page=1` | GET `/vehicles/{id}` |
| Sistema | GET `/` | GET `/health` |

## Testes
O projeto contém casos de teste simples que podem ser executados da seguinte forma:
```bash
uv add pytest httpx
pytest src/tests/
```

## Deploy

Deploy automático em Google Cloud Functions:

```bash
gcloud functions deploy star-wars-api-prod \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=star_wars_api \
  --trigger-http \
  --allow-unauthenticated
```

CI/CD automático via GitHub Actions: `ci.yml` (testes), `deploy-dev.yml` (dev), `deploy-prod.yml` (produção)

## Pontos importantes

- **Cache**: 24 horas para otimizar performance
- **Rate limit**: A SWAPI possui limitações; o cache local mitiga isso
- **Timeout**: 5 segundos por requisição
- **Erros**: Códigos HTTP apropriados (200, 404, 500)
