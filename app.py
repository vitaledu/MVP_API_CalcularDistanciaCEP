from flask_cors import CORS
from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource
from model.distancia_model import obter_endereco_via_cep, obter_coordenadas, calcular_distancia
import logger
import requests

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Distância API', description='API para calcular distância entre CEPs')

# Logger
logger.setup_logger()
log = logger.get_logger(__name__)

@api.route('/calcular_distancia')
class CalcularDistancia(Resource):
    @api.param('origem', 'CEP de origem', required=True)
    @api.param('destino', 'CEP de destino', required=True)
    def get(self):
        origem_cep = request.args.get('origem')
        destino_cep = request.args.get('destino')
        
        if not origem_cep or not destino_cep:
            log.error("CEPs de origem e destino são obrigatórios")
            return make_response(jsonify({"error": "CEPs de origem e destino são obrigatórios"}), 400)
        
        try:
            log.info(f"Obtendo endereço de origem para CEP: {origem_cep}")
            origem_endereco = obter_endereco_via_cep(origem_cep)
            log.info(f"Endereço de origem: {origem_endereco}")

            log.info(f"Obtendo endereço de destino para CEP: {destino_cep}")
            destino_endereco = obter_endereco_via_cep(destino_cep)
            log.info(f"Endereço de destino: {destino_endereco}")

            if not origem_endereco or not destino_endereco:
                raise ValueError("CEP de origem ou destino inválido")

            log.info(f"Obtendo coordenadas de origem para o endereço: {origem_endereco}")
            origem_coords = obter_coordenadas(origem_endereco)
            log.info(f"Coordenadas de origem: {origem_coords}")

            log.info(f"Obtendo coordenadas de destino para o endereço: {destino_endereco}")
            destino_coords = obter_coordenadas(destino_endereco)
            log.info(f"Coordenadas de destino: {destino_coords}")

            if not origem_coords or not destino_coords:
                raise ValueError("Não foi possível obter as coordenadas de origem ou destino")
            
            log.info(f"Calculando distância entre {origem_coords} e {destino_coords}")
            distancia = calcular_distancia(origem_coords, destino_coords)
            log.info(f"Distância calculada: {distancia} km")
            return make_response(jsonify({"origem": origem_cep, "destino": destino_cep, "distancia": distancia}), 200)
        except ValueError as ve:
            log.error(f"Erro de validação: {ve}")
            return make_response(jsonify({"error": str(ve)}), 400)
        except requests.RequestException as re:
            log.error(f"Erro de solicitação: {re}")
            if re.response.status_code == 403:
                return make_response(jsonify({"error": "Acesso negado à API externa. Verifique se o serviço está disponível ou se você atingiu o limite de requisições."}), 500)
            return make_response(jsonify({"error": "Erro ao tentar obter dados de um serviço externo"}), 500)
        except Exception as e:
            log.error(f"Erro ao calcular distância: {e}")
            return make_response(jsonify({"error": "Erro interno ao calcular distância"}), 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
