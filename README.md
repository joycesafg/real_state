# property-friends-real-state

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

The goal of the project is to build a pipeline to train and deploy a ML Model ensuring reproducibility and scalability

## Project Organization

# FastAPI Model Deployment

This repository contains a FastAPI-based API to serve a trained machine learning model. The training and deployment process is automated using GitHub Actions and Docker.

## Repository Structure

```
/
├── property_friends_real_state/
│   ├── modeling/
│   │   ├── get_data.py  # Downloads data from S3
│   │   ├── train.py     # Trains the model
│   │   ├── predict.py   # Evaluates the model
│   ├── app/
│   │   ├── app.py      # FastAPI app
├── Dockerfile           # Dockerfile to build the API
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt  # Dependencies
├── .github/workflows/
│   ├── ci_cd.yml  # GitHub Actions workflow for training and deployment
├── README.md
```

## Running Locally

### 1. Clone the Repository

```bash
git https://github.com/joycesafg/property-friends-real-state-repo.git
cd property-friends-real-state-repo
```

### 2. Set Up and Run the API Locally

#### Using Python (Without Docker)

```bash
pip install -r requirements.txt
uvicorn property_friends_real_state.app.app:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

#### Using Docker Compose

```bash
docker-compose up
```

## Automated Training and Deployment Workflow (GitHub Actions)

### Overview

1. When pushing to the `main` branch, GitHub Actions executes the `ci_cd.yml` workflow.
2. The workflow:
   - Downloads data from S3
   - Trains the model
   - Saves the model as `model.pkl`
   - Packages the API into a Docker image
   - Pushes the image to GitHub Container Registry (GHCR)

### GitHub Actions Configuration

In the GitHub repository, add the following **secrets**:

- `AKI` (AWS Access Key ID)
- `SAK` (AWS Secret Access Key)
- `GHCR_PAT` (Personal Access Token for GHCR authentication)

The workflow (`.github/workflows/ci_cd.yml`) automates this process.

## Accessing API Logs in MongoDB

The API stores prediction logs in MongoDB. To run locally:

1. Start MongoDB with Docker:

   ```bash
   docker-compose up -d
   ```

2. Access the database:

   ```
    client = MongoClient("mongodb://localhost:27017")
    db = client["logs_db"]
    logs_collection = db.api_logs

    logs = logs_collection.find()
    for log in logs:
        print(log)
   ```

# Real Estate Prediction API

📍 Endpoint

```
 POST /predict/ 
```

Recebe dados de um imóvel e retorna um preço estimado baseado no modelo de Machine Learning.

🔒 Autenticação
A API requer uma API Key no cabeçalho da requisição:
```
x-api-key: your_api_key
```

📝 Request (Entrada)
Content-Type: application/json
```
Exemplo de Body:

{
  "type": "apartment",
  "sector": "downtown",
  "net_usable_area": 75.5,
  "net_area": 90.0,
  "n_rooms": 3,
  "n_bathroom": 2,
  "latitude": -23.55052,
  "longitude": -46.633308,
  "price": 500000
}
```
📌 Parâmetros da Entrada

| Campo              | Tipo   | Obrigatório  | Descrição |
|--------------------|--------|------------- |-----------|
| `type`             | string | ✅ Sim       | Tipo do imóvel (ex: `"apartment"`, `"house"`) |
| `sector`           | string | ✅ Sim       | Localização ou setor do imóvel |
| `net_usable_area`  | float  | ✅ Sim       | Área útil do imóvel (m²) |
| `net_area`         | float  | ✅ Sim       | Área total do imóvel (m²) |
| `n_rooms`          | float  | ✅ Sim	    | Número de quartos
| `n_bathroom`       | float  | ✅ Sim	    | Número de banheiros
| `latitude`         | float  | ✅ Sim	    | Latitude da localização do imóvel
| `longitude`        | float  | ✅ Sim	    | Longitude da localização do imóvel
| `price`            | float  | ✅ Sim	    | Preço de venda do imóvel


📤 Response (Saída)
✅ 200 OK (Sucesso)

Exemplo de Resposta:
```
{
  "prediction": 520000
}
```
📌 Descrição da Resposta
Campo	    | Tipo	| Descrição
prediction	| int	| Valor previsto do imóvel baseado no modelo

⚠️ Possíveis Erros

Código	| Mensagem	          | Causa
|-------|---------------------|-------------------------------------
|400     |Bad Request          | Input data error: {detalhe}	Algum dado enviado no |payload é inválido
|403     |Forbidden	          | Access denied: Invalid API Key	API Key ausente ou incorreta
|500     |Internal Server Error|	Internal server error: Erro inesperado no servidor

🚀 Como Testar a API usando python

```
import requests

url = "http://localhost:8000/predict/"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "your_api_key"
}
data = {
    "type": "apartment",
    "sector": "downtown",
    "net_usable_area": 75.5,
    "net_area": 90.0,
    "n_rooms": 3,
    "n_bathroom": 2,
    "latitude": -23.55052,
    "longitude": -46.633308,
    "price": 500000
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```
---

**Author:** Joyce Maria do Carmo de Sa
**Contact:** joycesafg@gmail.com

