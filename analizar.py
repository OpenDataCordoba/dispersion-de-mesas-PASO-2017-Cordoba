#!/usr/bin/python3

'''
    Analizar los datos provisorios de las Elecciones PASO 2017 Legilativas en la Provincia 
    de Córdoba.

    Muestra de los datos

    sub_proCodigoProvincia,sub_depCodigoDepartamento,sub_munCodigoMunicipio,sub_mesCodigoCircuito,
        sub_mesCodigoMesa,sub_mesCodSexo,sub_votparCodigo,sub_parCodigo,ordenPartidos,subVotosPartido
    "04","001","666","0001 ","0001","X","0022","3017",1,0
    "04","001","666","0001 ","0001","X","0069","3037",1,3

    tomar los resultados de cada mesa a los fines de hacer un gráfico de dispersión
    con el % de electores vs % de votos de cada agrupación. 
'''
import csv
import sys

data_file = 'datos/circuitos-cordoba.csv'
campos = ['Seccion ID', 'Seccion Nombre', 'Circuito ID', 'Circuito Nombre']

circuitos = {}
with open(data_file) as csvfile:
    reader = csv.DictReader(csvfile)
    # headers = next(reader)
    for row in reader:
        departamento_id = row['Seccion ID'].strip().lstrip('0')
        departamento = row['Seccion Nombre'].strip().lstrip('0')
        circuito_id = row['Circuito ID'].strip().lstrip('0')
        circuito = row['Circuito Nombre'].strip().lstrip('0')

        nice = '{} ({} en {})'.format(circuito, circuito_id, departamento)
        circuitos[circuito_id] = {'nombre': circuito, 'departamento_id': departamento_id,
                                    'departamento': departamento, 'nice': nice }
        

# alianzas en córdoba
agrupaciones = {'22': 'HUMANISTA',
                    '69': 'GEN',
                    '201': 'PRIMERO LA GENTE',
                    '217': 'ENCUENTRO VECINAL',
                    '231': 'PAIS',
                    '502': 'CAMBIEMOS',
                    '503': 'FIT',
                    '543': 'CORDOBA CIUDADANA',
                    '567': 'IZQUIERDA AL FRENTE',
                    '570': 'SOMOS',
                    '578': 'UNION POR CORDOBA'}


campos = ['sub_proCodigoProvincia','sub_depCodigoDepartamento',
            'sub_munCodigoMunicipio','sub_mesCodigoCircuito',
            'sub_mesCodigoMesa','sub_mesCodSexo','sub_votparCodigo',
            'sub_parCodigo','ordenPartidos','subVotosPartido']

# archivo con los datos de los votantes de cada mesa a agrupaciones
data_file = 'datos/MesasSublemasCordobaProvincia.csv'

mesas = {}

with open(data_file) as csvfile:
    reader = csv.DictReader(csvfile)
    # headers = next(reader)

    for row in reader:
        departamento = row['sub_depCodigoDepartamento'].strip().lstrip('0')
        circuito = row['sub_mesCodigoCircuito'].strip().lstrip('0')
        votos = int(row['subVotosPartido'].strip())
        mesa = int(row['sub_mesCodigoMesa'].strip())
        
        agrupacion = row['sub_votparCodigo'].strip().lstrip('0')
        if agrupacion not in agrupaciones.keys():
            print('Error, agrupación inexistente')
            sys.exit(1)
        
        if mesa not in mesas.keys():
            if circuito in circuitos.keys():
                circuito_nice = circuitos[circuito]['nice']
            else:
                circuito_nice = '{} ????'.format(circuito)
                print('No existe el circuito {}'.format(circuito))

            mesas[mesa] = {'departamento': departamento, 'circuito': circuito,
                                'agrupaciones': {}, 'porcentajes': {},
                                'circuito': circuito_nice}
            
        if agrupacion not in mesas[mesa]['agrupaciones'].keys():
            mesas[mesa]['agrupaciones'][agrupacion] = 0
        
        mesas[mesa]['agrupaciones'][agrupacion] += votos


# archivo con los datos de los votantes de cada mesa generales (positivos, blancos, etc)
data_file = 'datos/MesasDNacionales.csv'

campos = ['mes_proCodigoProvincia', 'mes_depCodigoDepartamento',
            'mes_munCodigoMunicipio', 'mesCodigoCircuito',
            'mesCodigoMesa', 'mesCodSexo', 'mesEstado',
            'mesVotosValidos', 'mesVotosPositivos', 'mesVotosEnBlanco',
            'mesVotosNulos', 'mesVotosRecurridos', 'mesVotosImpugnados',
            'mesVotosComando', 'mesElectores', 'mesTotalVotantes',
            'mesVotosWarning_XP', 'mesVotosWarning_M3']


with open(data_file) as csvfile:
    reader = csv.DictReader(csvfile)
    # headers = next(reader)

    for row in reader:

        provincia = int(row['mes_proCodigoProvincia'].strip().lstrip('0'))
        if provincia != 4:
            continue

        departamento = row['mes_depCodigoDepartamento'].strip().lstrip('0')
        circuito = row['mesCodigoCircuito'].strip().lstrip('0')

        mesa = int(row['mesCodigoMesa'].strip())

        if mesa not in mesas.keys():
            print('Error, la mesa {} debería existir'.format(mesa))
            sys.exit(1)

        # solo debo pasar una vez por cada mesa
        if 'validos' in mesas[mesa].keys():
            print('Error, la mesa {} ya fue procesada'.format(mesa))
            sys.exit(1)

        validos = int(row['mesVotosValidos'].strip())
        positivos = int(row['mesVotosPositivos'].strip())
        blanco = int(row['mesVotosEnBlanco'].strip())
        nulos = int(row['mesVotosNulos'].strip())
        recurridos = int(row['mesVotosRecurridos'].strip())
        impugnados = int(row['mesVotosImpugnados'].strip())
        elecores_habilitados = int(row['mesElectores'].strip())
        electores_asistieron = int(row['mesTotalVotantes'].strip())

        mesas[mesa]['validos'] = validos
        mesas[mesa]['positivos'] = positivos
        mesas[mesa]['blanco'] = blanco
        mesas[mesa]['nulos'] = nulos
        mesas[mesa]['recurridos'] = recurridos
        mesas[mesa]['impugnados'] = impugnados
        mesas[mesa]['elecores_habilitados'] = elecores_habilitados
        mesas[mesa]['electores_asistieron'] = electores_asistieron
        
        participacion = round(100.0 * electores_asistieron / elecores_habilitados, 2)
        mesas[mesa]['participacion'] = participacion

        for agrupacion in mesas[mesa]['agrupaciones'].keys():
            votos = mesas[mesa]['agrupaciones'][agrupacion]
            if positivos > 0:
                porc = round(100.0 * votos / positivos, 2)
            else:
                porc = 0.0
            mesas[mesa]['porcentajes'][agrupacion] = porc
            

file_dest = 'datos/resultados-por-mesas-por-agrupacion.csv'
agrupaciones_headers = ['{} {}'.format(a, agrupaciones[a]) for a in agrupaciones.keys()]
agrupaciones_porc_headers = ['% {} {}'.format(a, agrupaciones[a]) for a in agrupaciones.keys()]

headers = ['departamento', 'circuito', 'mesa', 'habilitados', 'votaron', 'positivos', 'participacion'] + agrupaciones_headers + agrupaciones_porc_headers

with open(file_dest, 'w') as csvfile:
    w = csv.DictWriter(csvfile, headers)
    w.writeheader()
    for mesa in mesas.keys():
        row = {'departamento': mesas[mesa]['departamento'],
                'circuito': mesas[mesa]['circuito'],
                'mesa': mesa, 'habilitados': mesas[mesa]['elecores_habilitados'] ,
                'votaron': mesas[mesa]['electores_asistieron'],
                'positivos': positivos, 'participacion': mesas[mesa]['participacion']}
        for agrupacion in mesas[mesa]['agrupaciones'].keys():
            agrup_name = '{} {}'.format(agrupacion, agrupaciones[agrupacion])
            row[agrup_name] = mesas[mesa]['agrupaciones'][agrupacion]

            agrup_porc_name = '% {} {}'.format(agrupacion, agrupaciones[agrupacion])
            # print(mesas[mesa])
            row[agrup_porc_name] = mesas[mesa]['porcentajes'][agrupacion]

        w.writerow(row)

print('FIN')
