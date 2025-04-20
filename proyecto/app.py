from flask import Flask, render_template, jsonify, send_file
from pymongo import MongoClient
import json

app = Flask(__name__)

# Conéctate a la base de datos
client = MongoClient('localhost', 27017)
db = client.lista1
collection = db['1']

@app.route("/")
def index():
    return render_template("html/index.html")

@app.route("/tabladatos")
def tabladatos():
    # Obtén los datos de la base de datos
    data_from_db = list(collection.find())

    # Modifica la consulta para adaptarse a la nueva estructura de la base de datos
    data_formatted = [
        {
            '_id': str(item['_id']),
            'name': item.get('name', ''),
            'position': item.get('position', ''),
            'poise': item.get('poise', ''),
            'physical': item.get('physical', ''),
            'magic': item.get('magic', ''),
            'fire': item.get('fire', ''),
            'lightning': item.get('lightning', ''),
        }
        for item in data_from_db
    ]

    return render_template("html/tabladatos.html", data=data_formatted)

@app.route("/descargar_datos")
def descargar_datos():
    # Obtén los datos de la base de datos
    data_from_db = list(collection.find())

    # Formatea los datos para la descarga
    data_formatted = [
        {
            '_id': str(item['_id']),
            'name': item.get('name', ''),
            'position': item.get('position', ''),
            'poise': item.get('poise', ''),
            'physical': item.get('physical', ''),
            'magic': item.get('magic', ''),
            'fire': item.get('fire', ''),
            'lightning': item.get('lightning', ''),
        }
        for item in data_from_db
    ]

    # Crea un archivo JSON temporal
    json_filename = "data.json"
    with open(json_filename, 'w') as json_file:
        json.dump(data_formatted, json_file)

    # Envía el archivo para descargar
    return send_file(json_filename, as_attachment=True, download_name="data.json")

@app.route("/analisis")
def analisis():
    return render_template("html/analisis.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

