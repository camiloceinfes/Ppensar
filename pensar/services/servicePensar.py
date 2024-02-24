from pensar.models.models import componentes_model, competencias_model
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from functools import reduce
from sqlalchemy import text
import polars as pl
import pandas as pd
import json

class Ppensar():
    
    def calculate_componentes(self, idColegio, grado, salon, idArea, comp, db):

        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_Componentes"

        try:

            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @Grado=:Grado, @Salon=:Salon, @IDArea=:IDArea, @IDComponente=:IDComponente")
            result = db.execute(query, {"Codigo": idColegio, "Grado": grado, "Salon": salon, "IDArea": idArea, "IDComponente": comp}).fetchall()
            return json.loads(result[0][0])
        
        except Exception as e:
            return f'error {e}'
    
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

        #datos = db.query(pensar_dw).filter(and_(pensar_dw.Colegio == idColegio)).all()

        with open(r'C:\Users\Camilo\Documents\tareas milton 8a\Nueva carpeta\app\prueba.json', 'r') as archivo:
            datos = json.load(archivo)
            
        df = pl.DataFrame(datos)    
        condiciones = []
        condiciones.append(pl.col('IDplantel') == idColegio)
        if anio is not None:
            condiciones.append(pl.col('anio') == anio)
        if idPrueba is not None:
            condiciones.append(pl.col('idPrueba') == idPrueba)
        if condiciones:
            df = df.filter(reduce(lambda a, b: a & b, condiciones))

        print(df)
        areas = []
        ciclo_anterior = []
        grado_actual = []

        for area, ciclo, grado in zip(df['area'], df['ciclo_anterior'], df['grado_actual']):
            areas.append(area)
            ciclo_anterior.append(ciclo)
            grado_actual.append(grado)

        json_areas = {
                    "title": "Desempeño por área",
                    "label": "Promedio",
                    "labels": ['Inglés', 'Lenguaje', 'Ciencias Naturales', 'Sociales', 'Matematicas'],
                    "datasets": [
                        {
                        "label": "Ciclo anterior",
                        "data": ciclo_anterior
                        },
                        {
                        "label": "Grado actual",
                        "data": grado_actual
                        }
                    ]
                    }
        return json_areas    
    

    def calculate_grado(self, idColegio: int, anio: str, idPrueba: int, idArea: int, db: Session):

        #datos = db.query(pensar_dw).filter(and_(pensar_dw.Colegio == idColegio)).all()

        with open(r'C:\Users\Camilo\Documents\tareas milton 8a\Nueva carpeta\app\prueba.json', 'r') as archivo:
            datos = json.load(archivo)
            
        df = pl.DataFrame(datos)    
        condiciones = []
        condiciones.append(pl.col('IDplantel') == idColegio)
        if anio is not None:
            condiciones.append(pl.col('anio') == anio)
        if idPrueba is not None:
            condiciones.append(pl.col('idPrueba') == idPrueba)
        if condiciones:
            df = df.filter(reduce(lambda a, b: a & b, condiciones))

        print(df)
        areas = []
        ciclo_anterior = []
        grado_actual = []

        for area, ciclo, grado in zip(df['area'], df['ciclo_anterior'], df['grado_actual']):
            areas.append(area)
            ciclo_anterior.append(ciclo)
            grado_actual.append(grado)

        json_areas = {
                    "title": "Desempeño por área",
                    "label": "Promedio",
                    "labels": ['Inglés', 'Lenguaje', 'Ciencias Naturales', 'Sociales', 'Matematicas'],
                    "datasets": [
                        {
                        "label": "Ciclo anterior",
                        "data": ciclo_anterior
                        },
                        {
                        "label": "Grado actual",
                        "data": grado_actual
                        }
                    ]
                    }
        return json_areas    