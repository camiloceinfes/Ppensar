from fastapi import HTTPException, status
from pensar.models.models import Pensar
from sqlalchemy.orm import Session
from functools import reduce
from sqlalchemy import text
import polars as pl
import pandas as pd
import numpy as np
import json

class Ppensar():
    
    def get_global_params(self, code, year, db):
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_EnlazaaParametrosGenerales"
        
        try:
            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @Anno=:Anno")
            result = db.execute(query, {"Codigo": code, "Anno": year }).fetchall()
            
            return json.loads(result[0][0])
        except Exception as e:
            print(f'error {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
        
    def get_tests(self, code, current_year, state, db):
        pensar = db.query(Pensar).filter(Pensar.año_ciclo == current_year).all()
        if not pensar:
            return { 
                "status_code": "404",
                "message": "Resource not found" 
            }
        return pensar

    def get_tasks(self,code, year, idGrade, idClassroom, idPrueba, idArea, db):
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_PuntajeGlobalPorAprendizaje"
        
        try:
            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @Anno=:Anno, @Grado=:Grado, @Salon=:Salon, @IDPrueba=:IDPrueba,@IDArea=:IDArea")
            result = db.execute(query, {"Codigo": code, "Anno": year, "Grado": idGrade, "Salon": idClassroom, "IDPrueba": idPrueba, "IDArea": idArea }).fetchall()
            
            return json.loads(result[0][0])
        except Exception as e:
            print(f'error {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")

    def global_results(self, db):
        return ''

    def cycle_results(self, db):
        return ''

    def calculate_componentes(self, codigoColegio, grado, salon, idComponente, idArea, db):
        
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_PuntajeGlobalPorComponente"
        try:
            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @Grado=:Grado, @Salon=:Salon, @IDArea=:IDArea, @IDComponente=:IDComponente")
            result = db.execute(query, {"Codigo": codigoColegio, "Grado": grado, "Salon": salon, "IDArea": idArea, "IDComponente": idComponente}).fetchall()
            print(result)
            return json.loads(result[0][0])
        
        except Exception as e:
            print(f'error {e}')
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
    
    def calculate_competencias(self, codigoColegio, grado, salon, idCompetencia, idArea, db):
    
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_PuntajeGlobalPorCompetencia"
        try:

            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @Grado=:Grado, @Salon=:Salon, @IDArea=:IDArea, @IDCompetencia=:IDCompetencia")
            result = db.execute(query, {"Codigo": codigoColegio, "Grado": grado, "Salon": salon, "IDArea": idArea, "IDCompetencia": idCompetencia}).fetchall()
            
            return json.loads(result[0][0])

        except Exception as e:
            print(f'error {e}')
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
    
    def calculate_area(self, codigoColegio: int, anio: int, idPurba: int, idArea: int, grado: int, salon: int, db: Session): 

        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_Desempeno"

        try:
            query = text(f"EXEC {procedure_name} @CODIGO=:CODIGO, @ANNOA=:ANNOA, @IDPRUEBA=:IDPRUEBA, @IDAREA=:IDAREA, @GRADO=:GRADO, @SALON=:SALON")
            result = db.execute(query, {"CODIGO": codigoColegio, "ANNOA": anio, "IDPRUEBA": idPurba, "IDAREA": idArea, "GRADO": grado, "SALON": salon}).fetchall()
            
            df = pl.DataFrame(result)
            new_df = pl.DataFrame(
            {
                'prueba': df['column_0'].apply(lambda x: x[0]),
                'grado': df['column_0'].apply(lambda x: x[1]),
                'salon': df['column_0'].apply(lambda x: x[2]),
                'area': df['column_0'].apply(lambda x: x[3]),
                'Grado Actual': df['column_0'].apply(lambda x: x[4]),
                'Ciclo Anterior': df['column_0'].apply(lambda x: x[5])
            }
        )
            grouped = new_df.groupby('area')
            grado_actual_dict = {}
            ciclo_anterior_dict = {}

            for area, group in grouped:
                grado_actual_dict[area] = group['Grado Actual'].to_list()
                ciclo_anterior_dict[area] = group['Ciclo Anterior'].to_list()

            sorted_keys = sorted(grado_actual_dict.keys())
            grado_actual_dict = {llave: grado_actual_dict[llave] for llave in sorted_keys}
            ciclo_anterior_dict = {llave: ciclo_anterior_dict[llave] for llave in sorted_keys}

            avrs_list_grado_actual = []
            avrs_list_ciclo_anterior = []

            # print(sorted_keys)
            # print(f"Naturales: {np.mean(ciclo_anterior_dict[sorted_keys[0]])}")
            # print(f"Definitiva: {np.mean(ciclo_anterior_dict[sorted_keys[1]])}")
            # print(f"Inglés: {np.mean(ciclo_anterior_dict[sorted_keys[2]])}")
            # print(f"Matemáticas: {np.mean(ciclo_anterior_dict[sorted_keys[3]])}")
            
            for i in sorted_keys:
                avrs_list_grado_actual.append(np.round(np.mean(grado_actual_dict[i]), 0))
                avrs_list_ciclo_anterior.append(np.round(np.mean(ciclo_anterior_dict[i]), 0))
            
            json_areas = {
                        "title": "Desempeño por área",
                        "label": "Promedio",
                        "labels": sorted_keys,
                        "datasets": [
                            {
                            "label": "Ciclo anterior",
                            "data": avrs_list_ciclo_anterior
                            },
                            {
                            "label": "Grado actual",
                            "data": avrs_list_grado_actual 
                            }
                        ]
                    }
            
            return json_areas
        except Exception as e:
            print(f'error {e}')
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")

    def calculate_grado(self, codigoColegio: int, anio: int, idPurba: int, idArea: int, grado: int, salon: int, db: Session): 

        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_Desempeno"

        try:
            query = text(f"EXEC {procedure_name} @CODIGO=:CODIGO, @ANNOA=:ANNOA, @IDPRUEBA=:IDPRUEBA, @IDAREA=:IDAREA, @GRADO=:GRADO, @SALON=:SALON")
            result = db.execute(query, {"CODIGO": codigoColegio, "ANNOA": anio, "IDPRUEBA": idPurba, "IDAREA": idArea, "GRADO": grado, "SALON": salon}).fetchall()
            
            df = pl.DataFrame(result)
            new_df = pl.DataFrame(
            {
                'prueba': df['column_0'].apply(lambda x: x[0]),
                'grado': df['column_0'].apply(lambda x: x[1]),
                'salon': df['column_0'].apply(lambda x: x[2]),
                'area': df['column_0'].apply(lambda x: x[3]),
                'Grado Actual': df['column_0'].apply(lambda x: x[4]),
                'Ciclo Anterior': df['column_0'].apply(lambda x: x[5])
            }
        )
            grouped = new_df.groupby('grado')
            grado_actual_dict = {}
            ciclo_anterior_dict = {}

            for area, group in grouped:
                grado_actual_dict[area] = group['Grado Actual'].to_list()
                ciclo_anterior_dict[area] = group['Ciclo Anterior'].to_list()

            sorted_keys = sorted(grado_actual_dict.keys())
            grado_actual_dict = {llave: grado_actual_dict[llave] for llave in sorted_keys}
            ciclo_anterior_dict = {llave: ciclo_anterior_dict[llave] for llave in sorted_keys}

            avrs_list_grado_actual = []
            avrs_list_ciclo_anterior = []

            # print(sorted_keys)
            # print(f"Naturales: {np.mean(ciclo_anterior_dict[sorted_keys[0]])}")
            # print(f"Definitiva: {np.mean(ciclo_anterior_dict[sorted_keys[1]])}")
            # print(f"Inglés: {np.mean(ciclo_anterior_dict[sorted_keys[2]])}")
            # print(f"Matemáticas: {np.mean(ciclo_anterior_dict[sorted_keys[3]])}")
            
            for i in sorted_keys:
                avrs_list_grado_actual.append(np.round(np.mean(grado_actual_dict[i]), 0))
                avrs_list_ciclo_anterior.append(np.round(np.mean(ciclo_anterior_dict[i]), 0))
            
            json_areas = {
                        "title": "Desempeño por grado",
                        "label": "Promedio",
                        "labels": sorted_keys,
                        "datasets": [
                            {
                            "label": "Ciclo anterior",
                            "data": avrs_list_ciclo_anterior
                            },
                            {
                            "label": "Grado actual",
                            "data": avrs_list_grado_actual 
                            }
                        ]
                    }
            
            return json_areas
        except Exception as e:
            print(f'error {e}')
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")

    def parameters(self, codigoColegio, anio, db):
    
        return ''
        

# CREATE OR ALTER PROCEDURE [dbo].[SPR_Pensar_EnlazaaParametrosGenerales] (
#     @Codigo int = 6340,
#     @Anno int = 2023
# )