# metro_map.py
#Comprobar , otra forma de hacer los transbordos que los heroes linea 1 conecta con heroes linea 2 con peso 1, y los heroes linea 2 conecta con santa ana linea 2 peso 1
metro_map = {
    'San Pablo linea 1': {'Neptuno': 1.4, 'San Pablo linea 5': 1},
    'Neptuno': {'San Pablo linea 1': 1.4, 'Pajaritos': 2.1},
    'Pajaritos': {'Neptuno': 2.1, 'Las Rejas': 1.8},
    'Las Rejas': {'Pajaritos': 1.8, 'Ecuador': 1.1},
    'Ecuador': {'Las Rejas': 1.1, 'San Alberto Hurtado': 1.4},
    'San Alberto Hurtado': {'Ecuador': 1.4, 'Universidad de Santiago': 1.1},
    'Universidad de Santiago': {'San Alberto Hurtado': 1.1, 'Estación Central': 1.5},
    'Estación Central': {'Universidad de Santiago': 1.5, 'U.L.A': 1.3},
    'U.L.A': {'Estación Central': 1.3, 'Republica': 1.2},
    'Republica': {'U.L.A': 1.2, 'Los Héroes linea 1': 1.2},
    'Los Héroes linea 1': {'Republica': 1.2, 'La Moneda': 0.9, 'Los Héroes linea 2': 1},
    'La Moneda': {'Los Héroes linea 1': 0.9, 'Universidad de Chile linea 1': 0.8},
    'Universidad de Chile linea 1': {'La Moneda': 0.8, 'Santa Lucía': 1, 'Universidad de Chile linea 3': 1},
    'Santa Lucía': {'Universidad de Chile linea 1': 1, 'Universidad Católica': 1.1},
    'Universidad Católica': {'Santa Lucía': 1.1, 'Baquedano linea 1': 1.4},
    'Baquedano linea 1': {'Universidad Católica': 1.4, 'Salvador': 1.8, 'Baquedano linea 5': 1},
    'Salvador': {'Baquedano linea 1': 1.8, 'Manuel Montt': 1.7},
    'Manuel Montt': {'Salvador': 1.7, 'Pedro de Valdivia': 1.4},
    'Pedro de Valdivia': {'Manuel Montt': 1.4, 'Los Leones linea 1': 1.1},
    'Los Leones linea 1': {'Pedro de Valdivia': 1.1, 'Tobalaba linea 1': 1.7, 'Los Leones linea 6': 1},
    'Tobalaba linea 1': {'Los Leones linea 1': 1.7, 'El Golf': 1.3, 'Tobalaba linea 4': 1},
    'El Golf': {'Tobalaba linea 1': 1.3, 'Alcántara': 1.3},
    'Alcántara': {'El Golf': 1.3, 'Escuela Militar': 1.2},
    'Escuela Militar': {'Alcántara': 1.2, 'Manquehue': 3.1},
    'Manquehue': {'Escuela Militar': 3.1, 'Hernando de Magallanes': 2.4},
    'Hernando de Magallanes': {'Manquehue': 2.4, 'Los Dominicos': 2.2},
    'Los Dominicos': {'Hernando de Magallanes': 2.2},

    # Línea 5
    'Plaza de Maipú': {'Santiago Bueras': 2.7},
    'Santiago Bueras': {'Plaza de Maipú': 2.7, 'Del Sol': 1.4},
    'Del Sol': {'Santiago Bueras': 1.4, 'Monte Tabor': 1.8},
    'Monte Tabor': {'Del Sol': 1.8, 'Las Parcelas': 1.6},
    'Las Parcelas': {'Monte Tabor': 1.6, 'Laguna Sur': 2.8},
    'Laguna Sur': {'Las Parcelas': 2.8, 'Barrancas': 2.1},
    'Barrancas': {'Laguna Sur': 2.1, 'Pudahuel': 1.7},
    'Pudahuel': {'Barrancas': 1.7, 'San Pablo linea 5': 2.8},
    'San Pablo linea 5': {'Pudahuel': 2.8, 'Lo Prado': 1, 'San Pablo linea 1': 1},
    'Lo Prado': {'San Pablo linea 5': 1, 'Blanqueado': 1.5},
    'Blanqueado': {'Lo Prado': 1.5, 'Gruta de Lourdes': 2.7},
    'Gruta de Lourdes': {'Blanqueado': 2.7, 'Quinta Normal': 1.9},
    'Quinta Normal': {'Gruta de Lourdes': 1.9, 'Cumming': 1.9},
    'Cumming': {'Quinta Normal': 1.9, 'Santa Ana linea 5': 1.4},
    'Santa Ana linea 5': {'Cumming': 1.4, 'Plaza de Armas linea 5': 1.5, 'Santa Ana linea 2': 1},
    'Plaza de Armas linea 5': {'Santa Ana linea 5': 1.5, 'Bellas Artes': 1.1, 'Plaza de Armas linea 3': 1},
    'Bellas Artes': {'Plaza de Armas linea 5': 1.1, 'Baquedano linea 5': 1.8},
    'Baquedano linea 5': {'Baquedano linea 1': 1, 'Bellas Artes': 1.8, 'Parque Bustamante': 1.1},
    'Parque Bustamante': {'Baquedano linea 5': 1.1, 'Santa Isabel': 0.9},
    'Santa Isabel': {'Parque Bustamante': 0.9, 'Irarrázaval linea 5': 1.3},
    'Irarrázaval linea 5': {'Santa Isabel': 1.3, 'Ñuble linea 5': 2.9, 'Irarrázaval linea 3': 1},
    'Ñuble linea 5': {'Irarrázaval linea 5': 2.9, 'Rodrigo de Araya': 2.2, 'Ñuble linea 6':1,},
    'Rodrigo de Araya': {'Ñuble linea 5': 2.2, 'Carlos Valdovinos': 1.9},
    'Carlos Valdovinos': {'Rodrigo de Araya': 1.9, 'Camino Agricola': 0.9},
    'Camino Agricola': {'Carlos Valdovinos': 0.9, 'San Joaquin': 1.4},
    'San Joaquin': {'Camino Agricola': 1.4, 'Pedredo': 1.9},
    'Pedredo': {'San Joaquin': 1.9, 'Mirador': 1.5},
    'Mirador': {'Pedredo': 1.5, 'Bellavista de la Florida': 1.6},
    'Bellavista de la Florida': {'Mirador': 1.6, 'Vicente Valdes linea 5': 1.3},
    'Vicente Valdes linea 5': {'Bellavista de la Florida': 1.3, 'Vicente Valdes linea 4': 1},
    

    # Línea 2
    'Vespucio Norte': {'Zapadores': 2.5},
    'Zapadores': {'Vespucio Norte': 2.5, 'Dorsal': 1.1},
    'Dorsal': {'Zapadores': 1.1, 'Einstein': 2.3},
    'Einstein': {'Dorsal': 2.3, 'Cementerios': 1.5},
    'Cementerios': {'Einstein': 1.5, 'Cerro Blanco': 1.6},
    'Cerro Blanco': {'Cementerios': 1.6, 'Patronato': 1.3},
    'Patronato': {'Cerro Blanco': 1.3, 'Cal y Canto linea 2': 1.3},
    'Cal y Canto linea 2': {'Patronato': 1.3, 'Santa Ana linea 2': 2.1, 'Cal y Canto linea 3': 1},
    'Santa Ana linea 2': {'Cal y Canto linea 2': 2.1, 'Los Héroes linea 2': 1.5, 'Santa Ana linea 5': 1},
    'Los Héroes linea 2': {'Santa Ana linea 2': 1.5, 'Toesca': 1.4, 'Los Héroes linea 1': 1},
    'Toesca': {'Los Héroes linea 2': 1.4, 'Parque OHiggins': 1.6},
    'Parque OHiggins': {'Toesca': 1.6, 'Rondizzoni': 1.6},
    'Rondizzoni': {'Parque OHiggins': 1.6, 'Franklin linea 2': 1.7},
    'Franklin linea 2': {'Rondizzoni': 1.7, 'El Llano': 1.2, 'Franklin linea 6': 1},
    'El Llano': {'Franklin linea 2': 1.2, 'San Miguel': 1.2},
    'San Miguel': {'El Llano': 1.2, 'Lo Vial': 1.4},
    'Lo Vial': {'San Miguel': 1.4, 'Departamental': 1.1},
    'Departamental': {'Lo Vial': 1.1, 'Ciudad del Niño': 1.3},
    'Ciudad del Niño': {'Departamental': 1.3, 'Lo Ovalle': 1.5},
    'Lo Ovalle': {'Ciudad del Niño': 1.5, 'El Parrón': 1.6},
    'El Parrón': {'Lo Ovalle': 1.6, 'La Cisterna linea 2': 2},
    'La Cisterna linea 2': {'El Parrón': 2, 'El Bosque': 1.5, 'La Cisterna linea 4A': 1},
    'El Bosque': {'La Cisterna linea 2': 1.5, 'Observatorio': 2.6},
    'Observatorio': {'El Bosque': 2.6, 'Copa lo Martinez': 2.1},
    'Copa lo Martinez': {'Observatorio': 2.1, 'Hospital el Pino': 2.2},
    'Hospital el Pino': {'Copa lo Martinez': 2.2},
    
    #Linea 3
    
    'Plaza Quilicura': {'Lo Cruzat': 1.9},
    'Lo Cruzat': {'Plaza Quilicura': 1.9, 'Ferrocaril': 2.9 },
    'Ferrocaril': {'Lo Cruzat': 2.9, 'Los Libertadores': 2.3 },
    'Los Libertadores': {'Ferrocaril': 2.3, 'Cardenal Caro': 2.1 },
    'Cardenal Caro': {'Los Libertadores': 2.1, 'Vivaceta': 3 },
    'Vivaceta': {'Cardenal Caro': 3, 'Conchali': 2.9 },
    'Conchali': {'Vivaceta': 2.9, 'Plaza Chacabuco': 2.5 },
    'Plaza Chacabuco': {'Conchali': 2.5, 'Hospitales': 2.3 },
    'Hospitales': {'Plaza Chacabuco': 2.3, 'Cal y Canto linea 3': 3.2 },
    'Cal y Canto linea 3': {'Hospitales': 3.2, 'Plaza de Armas linea 3': 1.1, 'Cal y Canto linea 2': 1},
    'Plaza de Armas linea 3': {'Cal y Canto linea 3': 1.1, 'Universidad de Chile linea 3': 1.4, 'Plaza de Armas linea 5': 1},
    'Universidad de Chile linea 3': {'Plaza de Armas linea 3': 1.4, 'Parque Almagro': 1.6, 'Universidad de Chile linea 1': 1},
    'Parque Almagro': {'Universidad de Chile linea 3': 1.6, 'Matta': 2.7 },
    'Matta': {'Parque Almagro': 2.7, 'Irarrázaval linea 3': 2.6 },
    'Irarrázaval linea 3': {'Matta': 2.6, 'Monseñor Eyzaguirre': 2.5, 'Irarrázaval linea 5': 1},
    'Monseñor Eyzaguirre': {'Irarrázaval linea 3': 2.5, 'Ñuñoa linea 3': 1.5 },
    'Ñuñoa linea 3': {'Monseñor Eyzaguirre': 1.5, 'Chile España': 1.4, 'Ñuñoa linea 6': 1},
    'Chile España': {'Ñuñoa linea 3': 1.4, 'Villa Frei': 2.9 },
    'Villa Frei': {'Chile España': 2.9, 'Plaza Egaña linea 3': 1.7 },
    'Plaza Egaña linea 3': {'Villa Frei': 1.7, 'Fernando Castillo Velasco': 2.5, 'Plaza Egaña linea 4': 1 },
    'Fernando Castillo Velasco': {'Plaza Egaña linea 3': 2.5},
    
    #Linea 6
    
    'Cerrillos': {'Lo Valledor': 2.7},
    'Lo Valledor': {'Cerrillos': 2.7, 'Pedro Aguirre Cerda': 2.6 },
    'Pedro Aguirre Cerda': {'Lo Valledor': 2.6, 'Franklin linea 6': 2.8 },
    'Franklin linea 6': {'Pedro Aguirre Cerda': 2.8, 'Bio Bio': 1.1, 'Franklin linea 2': 1 },
    'Bio Bio': {'Franklin linea 6': 1.1, 'Ñuble linea 6': 3.7 },
    'Ñuble linea 6': {'Bio Bio': 3.7, 'Estadio Nacional': 3.4, 'Ñuble linea 5': 1},
    'Estadio Nacional': {'Ñuble linea 6': 3.4, 'Ñuñoa linea 6': 1.6 },
    'Ñuñoa linea 6': {'Ñuñoa linea 3': 1, 'Ines de Suarez': 3.1, 'Estadio Nacional': 1.6},
    'Ines de Suarez': {'Ñuñoa linea 6': 3.1, 'Los Leones linea 6': 3.9 },
    'Los Leones linea 6': {'Los Leones linea 1': 1, 'Ines de Suarez': 3.9},
    
    #Linea 4
    
    'Tobalaba linea 4': {'Tobalaba linea 1': 1, 'Cristóbal Colón': 2.2},
    'Cristóbal Colón': {'Tobalaba linea 4': 2.2, 'Francisco Bilbao': 1.3 },
    'Francisco Bilbao': {'Cristóbal Colón': 1.3, 'Principe de Gales': 2.3 },
    'Principe de Gales': {'Francisco Bilbao': 2.3, 'Simon Bolivar': 1.3 },
    'Simon Bolivar': {'Principe de Gales': 1.3, 'Plaza Egaña linea 4': 1.4 },
    'Plaza Egaña linea 4': {'Plaza Egaña linea 3': 1, 'Simon Bolivar': 1.4, 'Los Orientales': 1.7 },
    'Los Orientales': {'Plaza Egaña linea 4': 1.7, 'Grecia': 1.4 },
    'Grecia': {'Los Orientales': 1.4, 'Los Presidentes': 2 },
    'Los Presidentes': {'Grecia': 2, 'Quilin': 1.5 },
    'Quilin': {'Los Presidentes': 1.5, 'Las Torres': 2.3 },
    'Las Torres': {'Quilin': 2.3, 'Macul': 2 },
    'Macul': {'Las Torres': 2, 'Vicuña Maquena Linea 4': 2.1 },
    'Vicuña Maquena Linea 4': {'Macul': 2.1, 'Vicente Valdes linea 4': 1.3, 'Vicuña Maquena Linea 4A': 1 },
    'Vicente Valdes linea 4': {'Vicente Valdes linea 5': 1, 'Vicuña Maquena Linea 4': 1.3, 'Rojas Magallanes': 2},
    'Rojas Magallanes': {'Vicente Valdes linea 4': 2, 'Trinidad': 1.9 },
    'Trinidad': {'Rojas Magallanes': 1.9, 'San Jose de la Estrella': 1.4 },
    'San Jose de la Estrella': {'Trinidad': 1.4, 'Los Quillayes': 1.5 },
    'Los Quillayes': {'San Jose de la Estrella': 1.5, 'Elisa Correa': 1.5 },
    'Elisa Correa': {'Los Quillayes': 1.5, 'Hospital Sotero del Rio': 1.3 },
    'Hospital Sotero del Rio': {'Elisa Correa': 1.3, 'Protectrora de la infancia': 2.4 },
    'Protectrora de la infancia': {'Hospital Sotero del Rio': 2.4, 'Las Mercedes': 2.1 },
    'Las Mercedes': {'Protectrora de la infancia': 2.1, 'Plaza de Puente Alto': 1.2 },
    'Plaza de Puente Alto': {'Las Mercedes': 1.2},
    
    #Linea 4A
    
    'La Cisterna linea 4A': {'La Cisterna linea 2': 1, 'San Ramon': 2.7},
    'San Ramon': {'La Cisterna linea 4A': 2.7, 'Santa Rosa': 1.1 },
    'Santa Rosa': {'San Ramon': 1.1, 'La Granja': 2.3 },
    'La Granja': {'Santa Rosa': 2.3, 'Santa Julia': 2.1 },
    'Santa Julia': {'La Granja': 2.1, 'Vicuña Maquena Linea 4A': 2.2 },
    'Vicuña Maquena Linea 4A': {'Vicuña Maquena Linea 4': 1, 'Santa Julia': 2.2 },
    
    
    
    
}