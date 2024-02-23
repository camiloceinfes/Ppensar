
from pensar.models.models import componentes_model, competencias_model, Pensar
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from functools import reduce
import polars as pl
import pandas as pd
import json

class Ppensar():
    def get_tests(self, code, current_year, state, db):
        print('Entro aqui')
        pensar = db.query(Pensar).filter(Pensar.año_ciclo == current_year).all()
        if not pensar:
            return { 
                "status_code": "404",
                "message": "Resource not found" 
            }
        return pensar

    def get_tasks(self, grado, salon, area, db):
        return ''

    def global_results(self, db):
        return ''

    def cycle_results(self, db):
        return ''

    def calculate_componentes(self, grado, salon, area, comp, db):
        lista = []
        lista_filtro = []
        lista_filtro.append(componentes_model.grado == grado)
        if salon != None:
            lista_filtro.append(componentes_model.salon == salon)
        if area != None:
            lista_filtro.append(componentes_model.area == area)
        if comp != None:
            lista_filtro.append(componentes_model.componente == comp)

        consulta1 = db.query(componentes_model.tipo_rejilla, componentes_model.componente, componentes_model.ciclo_anterior_plantel, 
                        componentes_model.ciclo_anterior_nacional ,componentes_model.ciclo_actual_nacional, componentes_model.ciclo_actual_plantel
                        ).filter(and_(*lista_filtro)).all()
        
        print(consulta1)

        for componente in consulta1:
            tiporejilla = componente.tipo_rejilla
            nombrecomp  = componente.componente
            nacional_an = componente.ciclo_anterior_nacional
            plantel_an  = componente.ciclo_anterior_plantel
            nacional_ac = componente.ciclo_actual_nacional
            plantel_ac  = componente.ciclo_actual_plantel

            if tiporejilla == 'old':
                comp1 = {"tiporejilla" : tiporejilla,
                        "nombre"       : nombrecomp,
                        "nacional"     : nacional_an,
                        "plantel"      : plantel_an
                }
                lista.append(comp1)

            if tiporejilla == 'new':
                comp2 = {"tiporejilla"  : tiporejilla,
                        "nombre"        : nombrecomp,
                        "nacional"      : {
                        "ciclo_actual"  : nacional_ac,
                        "ciclo_anterior": nacional_an
                    },
                    "plantel" : {
                        "ciclo_actual"  : plantel_ac,
                        "ciclo_anterior": plantel_an                            
                    }
                }
                lista.append(comp2)

        return lista
    
    def calculate_competencias(self, idColegio: int, db: Session):
        df = pl.read_database(db.query(competencias_model).filter(competencias_model.IDplantel == idColegio).statement, db.bind)
        df = df.with_columns(
            pl.when((pl.col("grado") == 1) | (pl.col("grado") == 2) | (pl.col("grado") == 3))
            .then(1)
            .when((pl.col("grado") == 4) | (pl.col("grado") == 5))
            .then(2)
            .when((pl.col("grado") == 6) | (pl.col("grado") == 7))
            .then(3)
            .when((pl.col("grado") == 8) | (pl.col("grado") == 9))
            .then(4)
            .otherwise(5)
            .alias("CicloActual") #Pregunta_Estado
        )

        pid_1 = df.groupby('nombrePrueba').mean().select(['nombrePrueba', 'porcentaje_de_acierto']).with_columns(structure = pl.lit('nombrePrueba')).rename({'nombrePrueba': 'name'}).to_pandas()
        group_list = ['nombrePrueba', 'pregunta_Estado']
        pid_2 = df.groupby(group_list).mean().sort(group_list).select(['pregunta_Estado', 'porcentaje_de_acierto', 'nombrePrueba']).with_columns(structure = pl.lit('pregunta_Estado')).rename({'pregunta_Estado': 'name', 'nombrePrueba': 'anterior'}).to_pandas()
        group_list.append('CicloActual')
        pid_3 = df.groupby(group_list).mean().sort(group_list).select(['CicloActual', 'porcentaje_de_acierto', 'pregunta_Estado']).with_columns(structure = pl.lit('CicloActual')).rename({'CicloActual': 'name', 'pregunta_Estado': 'anterior'}).to_pandas()
        group_list.append('grado')
        pid_4 = df.groupby(group_list).mean().sort(group_list).select(['grado', 'porcentaje_de_acierto', 'CicloActual']).with_columns(structure = pl.lit('grado')).rename({'grado': 'name', 'CicloActual': 'anterior'}).to_pandas()
        group_list.append('area')
        pid_5 = df.groupby(group_list).mean().sort(group_list).select(['area', 'porcentaje_de_acierto', 'grado']).with_columns(structure = pl.lit('area')).rename({'area': 'name', 'grado': 'anterior'}).to_pandas()
        group_list.append('componente')
        pid_6 = df.groupby(group_list).mean().sort(group_list).select(['componente', 'porcentaje_de_acierto', 'area']).with_columns(structure = pl.lit('componente')).rename({'componente': 'name', 'area': 'anterior'}).to_pandas()
        group_list.append('competencia')
        pid_7 = df.groupby(group_list).mean().sort(group_list).select(['competencia', 'porcentaje_de_acierto', 'componente']).with_columns(structure = pl.lit('competencia')).rename({'competencia': 'name', 'componente': 'anterior'}).to_pandas()
        pid = pd.concat([pid_1, pid_2, pid_3, pid_4, pid_5, pid_6, pid_7], ignore_index=True)

        def convertir_a_string(valor):
            if isinstance(valor, int):
                return 'Grado ' + str(valor)
            else:
                return valor

        pid['name'] = pid['name'].apply(lambda x: convertir_a_string(x))
        pid["id"] = pid.index + 1
        anterior_to_id = pid.set_index('name')['id'].to_dict()
        pid['pid'] = pid['anterior'].map(anterior_to_id)
        pid.fillna('0', inplace=True)
        pid.drop(columns='anterior', inplace=True)
        pid['pid'] = pd.to_numeric(pid['pid'], downcast='integer')
        pid['porcentaje_de_acierto'] = (pid['porcentaje_de_acierto'] * 100).round(2)
        pid = pid.rename(columns={'porcentaje_de_acierto': 'value'}).to_dict(orient='records')

        return pid
    
    def calculate_area(self, idColegio: int, anio: str, idPrueba: int, db: Session):

        #consulta = db.query(pensar_dw).filter(and_(pensar_dw.Colegio == idColegio)).all()

        with open(r'C:\Users\Camilo\Documents\tareas milton 8a\Nueva carpeta\app\prueba.json', 'r') as archivo:
            datos = json.load(archivo)

        # filtros = [(pl.col('IDplantel') == idColegio), (pl.col('anio') == anio)]
        # df = pl.DataFrame(datos).filter(filtros)
            
        df = pl.DataFrame(datos)    
        condiciones = []
        condiciones.append(pl.col('IDplantel') == idColegio)
        if anio is not None:
            condiciones.append(pl.col('anio') == anio)
        if idPrueba is not None:
            condiciones.append(pl.col('idPrueba') == idPrueba)
        if condiciones:
            df = df.filter(reduce(lambda a, b: a & b, condiciones))

        df_filtrado = df.filter(pl.col('regilla') == 'no tiene')

        if len(df_filtrado) > 0:

            areas = []
            ciclo_anterior = []
            grado_actual = []

            for area, ciclo, grado in zip(df_filtrado['area'], df_filtrado['ciclo_anterior'], df_filtrado['grado_actual']):
                areas.append(area)
                ciclo_anterior.append(ciclo)
                grado_actual.append(grado)

            # Imprimir los valores obtenidos
            print(areas)
            print(ciclo_anterior)
            print(grado_actual)
            # json_areas = {
            #             "title": "Desempeño por área",
            #             "label": "Promedio",
            #             "labels": areas,
            #             "datasets": [
            #                 {
            #                 "label": "Ciclo anterior",
            #                 "data": ciclo_anterior
            #                 },
            #                 {
            #                 "label": "Grado actual",
            #                 "data": grado_actual
            #                 }
            #             ]
            #             }
            # return json_areas
            
        return 'pepa'

            
# def findPensarAvg(
#     db: Session,
#     idColegio: int,
#     model_avg: ModelAvgName
# ):
#     df = pl.read_database(db.query(pensar_dw).filter(pensar_dw.Colegio == idColegio).statement, db.bind)
#     if model_avg.value == 'Area':
#          areas = df.groupby(['Area', 'Pregunta_Estado']).mean().select(['Area', 'Pregunta_Estado', 'Porcentaje_de_acierto']).with_columns(pl.col('Porcentaje_de_acierto').mul(100).round(2)).rename({'Area': 'labels', 'Porcentaje_de_acierto': 'data', 'Pregunta_Estado': 'label'}).sort('labels')#.to_pandas()#.to_dict('records')
#          json_areas = {
#                         "title": "Desempeño por área",
#                         "label": "Promedio",
#                         "labels": list(areas['labels'].unique().sort()),
#                         "datasets": [
#                             {
#                             "label": "Ciclo anterior",
#                             "data": list(areas.filter(pl.col('label') == 'Diagnóstico')['data'])
#                             },
#                             {
#                             "label": "Grado actual",
#                             "data": list(areas.filter(pl.col('label') == 'Actual')['data'])
#                             }
#                         ]
#                         }
#          return json_areas
    
    # if model_avg.value == 'Grado':
    #      df_grade = df.groupby(['Grado', 'Pregunta_Estado']).mean().select(['Grado', 'Pregunta_Estado', 'Porcentaje_de_acierto']).with_columns(pl.col('Porcentaje_de_acierto').mul(100).round(2)).rename({'Grado': 'labels', 'Porcentaje_de_acierto': 'data', 'Pregunta_Estado': 'label'}).sort('labels')
    #      len_grade = list(df_grade.filter(pl.col('labels') <= 3)['labels'])
    #      try:
    #         df_grade = pl.concat([pl.DataFrame({"labels": len_grade, "label": ['Diagnóstico']*len(len_grade), "data": [0.0]*len(len_grade)}), df_grade]).sort('labels')
    #      except:
    #           pass      
    #      print(df_grade)
    #      json_grade = {
    #                     "title": "Desempeño por grado",
    #                     "label": "Promedio",
    #                     "labels": list(df_grade['labels'].unique().sort()),
    #                     "datasets": [
    #                         {
    #                         "label": "Ciclo anterior",
    #                         "data": list(df_grade.filter(pl.col('label') == 'Diagnóstico')['data'])
    #                         },
    #                         {
    #                         "label": "Grado actual",
    #                         "data": list(df_grade.filter(pl.col('label') == 'Actual')['data'])
    #                         }
    #                     ]
    #                     }
    #      return json_grade
#     return 'Nada'
    

            # df = pl.read_database(db.query(pensar_dw).filter(pensar_dw.Colegio == idColegio).statement, db.bind)
        # areas = df.groupby(['Area', 'Pregunta_Estado']).mean().select(['Area', 'Pregunta_Estado', 'Porcentaje_de_acierto']).with_columns(pl.col('Porcentaje_de_acierto').mul(100).round(2)).rename({'Area': 'labels', 'Porcentaje_de_acierto': 'data', 'Pregunta_Estado': 'label'}).sort('labels')#.to_pandas()#.to_dict('records')