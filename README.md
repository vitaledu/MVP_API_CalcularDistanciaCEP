# Distância API

Este projeto é uma API para calcular a distância entre dois CEPs. Utiliza Flask, Flask-CORS e Flask-RESTX.

## Instalação

Para executar este projeto, siga os passos abaixo:

### Requisitos

- Docker instalado em sua máquina.

### Passos para execução

1. Clone este repositório:
    ```sh
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2. Construa a imagem Docker:
    ```sh
    docker build -t distancia-api .
    ```

3. Execute o container Docker:
    ```sh
    docker run -p 5001:5001 distancia-api
    ```

A API estará disponível em `http://localhost:5001`.

## Uso da API

A API possui um endpoint principal para calcular a distância entre dois CEPs.

### Endpoint: `/calcular_distancia`

- Método: GET
- Parâmetros:
  - `origem` (obrigatório): CEP de origem.
  - `destino` (obrigatório): CEP de destino.

#### Exemplo de requisição

```sh
curl -X GET "http://localhost:5001/calcular_distancia?origem=01001000&destino=20040030"
Exemplo de resposta
json
Copy code
{
  "origem": "01001000",
  "destino": "20040030",
  "distancia": 429.38
}
Estrutura do Projeto
app.py: Arquivo principal da aplicação Flask.
model/distancia_model.py: Contém as funções para obter endereço via CEP, coordenadas e calcular distância.
logger.py: Configurações de log.
Desenvolvimento
Executando localmente
Se preferir executar a aplicação localmente sem Docker, siga os passos abaixo:

Crie um ambiente virtual:

sh
Copy code
python -m venv venv
Ative o ambiente virtual:

No Windows:
sh
Copy code
venv\Scripts\activate
No Unix ou MacOS:
sh
Copy code
source venv/bin/activate
Instale as dependências:

sh
Copy code
pip install -r requirements.txt
Execute a aplicação:

sh
Copy code
python app.py
A aplicação estará disponível em http://localhost:5001.

Contribuição
Sinta-se à vontade para abrir issues e pull requests. Toda contribuição é bem-vinda!