from flask import Flask, render_template, jsonify, send_file
from pymongo import MongoClient
import json
import plotly.express as px
import os
from bson import ObjectId

app = Flask(__name__)

# Conéctate a la base de datos
client = MongoClient('localhost', 27017)
db = client.lista1
collection = db['1']

# Variable global para contar las visitas
visit_count = 0

@app.route("/")
def index():
    # Incrementa el contador en cada visita
    global visit_count
    visit_count += 1

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

    return render_template("html/index.html", visit_count=visit_count, data_formatted=data_formatted)

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
    # Obtén los datos de la base de datos
    data_from_db = list(collection.find())

    # Convierte el objeto ObjectId a su representación de cadena
    for item in data_from_db:
        item['_id'] = str(item['_id'])

    # Gráfico de Tendencia
    fig_tendencia = px.line(
        data_from_db,
        x='name',  # Cambia aquí de '_id' a 'name'
        y='physical',
        title='Tendencia del parámetro Physical',
        labels={'name': 'Nombre', 'physical': 'Physical'},
    )

    # Modifica la ruta para guardar el gráfico en la carpeta 'static'
    graph_tendencia_filename = 'graph_tendencia.html'
    fig_tendencia.write_html(f'static/{graph_tendencia_filename}', full_html=False)

    # Gráfico de Barras - Poise por Nombre
    fig_barras_poise = px.bar(
        data_from_db,
        x='name',
        y='poise',
        title='Gráfico de Barras - Poise por Nombre',
        labels={'name': 'Nombre', 'poise': 'Poise'},
    )

    # Modifica la ruta para guardar el gráfico en la carpeta 'static'
    graph_barras_poise_filename = 'graph_barras_poise.html'
    fig_barras_poise.write_html(f'static/{graph_barras_poise_filename}', full_html=False)

    # Renderiza la página analisis.html con los gráficos
    return render_template(
        "html/analisis.html",
        graph_tendencia_filename=graph_tendencia_filename,
        graph_barras_poise_filename=graph_barras_poise_filename
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




