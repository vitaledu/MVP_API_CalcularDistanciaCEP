# schemas/distancia_schema.py

from marshmallow import Schema, fields

class DistanciaSchema(Schema):
    origem = fields.Str(required=True)
    destino = fields.Str(required=True)
    distancia = fields.Float(required=True)
