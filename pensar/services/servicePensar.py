from fastapi import HTTPException, status
from collections import namedtuple
from sqlalchemy.orm import Session
from functools import reduce
from sqlalchemy import text
from datetime import datetime
import polars as pl
import pandas as pd
import numpy as np
import os
import json
import math 

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
        
    def get_tests(self, code, year, idTest, db):
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_GradoCicloDesempeno"
        
        try:
            query = text(f"EXEC {procedure_name} @CODIGO=:Codigo, @ANNOA=:Anno, @IDPRUEBA=:IDPrueba, @CICLO_GRADO=:CicloGrado")
            result = db.execute(query, {"Codigo": code, "Anno": year, "IDPrueba": idTest or -1, "CicloGrado": -3  }).fetchall()

            tests = []
            
            for row in result:
                date = row[7]
                formatted_date = None  # Initialize formatted_date
                if date:
                    formatted_date = datetime.strftime(date, "%Y-%m-%d")
                    
                test = {
                    "id": row[0],
                    "name": row[1],
                    "img": row[2],
                    "globalScore": row[5],
                    "resultsTotal": row[6],
                    "date": formatted_date or None,
                }
                
                tests.append(test)

            return tests
        except Exception as e:
            print(f'error {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        

    def get_tasks(self,code, year, idGrade, idClassroom, idPrueba, idArea, db):
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_PuntajeGlobalPorAprendizaje"
        
        try:
            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @Anno=:Anno, @Grado=:Grado, @Salon=:Salon, @IDPrueba=:IDPrueba,@IDArea=:IDArea")

            tasks = db.execute(query, {"Codigo": code, "Anno": year, "Grado": idGrade or 0, "Salon": idClassroom or 0, "IDPrueba": idPrueba or 0, "IDArea": idArea or 0 }).fetchall()

            if tasks and tasks[0][0] is not None:
                return json.loads(tasks[0][0])
                
            return []
        except Exception as e:
            print(f'error {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
        
    def global_results(self, code, year, idPrueba, db):
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_GlobalDesempeno"
        
        try:
            query = text(f"EXEC {procedure_name} @CODIGO=:Codigo, @ANNOA=:Anno, @IDPRUEBA=:IDPrueba")
            result = db.execute(query, {"Codigo": code, "Anno": year, "IDPrueba": idPrueba or -2 }).fetchall()
            
            performance = []
            
            for row in result:
                name = row[1]
                current_cycle = float(row[2])
                previous_cycle = float(row[3])
                data = {
                    "currentCycle": math.floor(current_cycle),
                    "previosCycle": math.floor(previous_cycle)
                }
                obj_response = {
                    "name": name,
                    "data": [data]
                }
                performance.append(obj_response)
            
            return performance
        except Exception as e:
            print(f'error {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    def cycle_results(self, code, year, idPrueba, db):
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_GradoCicloDesempeno"
    
        try:
            query = text(f"EXEC {procedure_name} @CODIGO=:Codigo, @ANNOA=:Anno, @IDPRUEBA=:IDPrueba, @CICLO_GRADO=:CicloGrado")
            result = db.execute(query, {"Codigo": code, "Anno": year, "IDPrueba": idPrueba or -2, "CicloGrado": -1}).fetchall()

            performance = {}
            global_score_by_cycle = self.calculate_weighted_average(code, year, idPrueba, db)
            
            # Initialize percentage dictionary
            percentage_dict = {item['cycle']: item['score'] for item in global_score_by_cycle}
            
            for row in result:
                cycle = row[3]
                grade = row[4]
                score_grade = float(row[5])
                
                if cycle not in performance:
                    performance[cycle] = {
                        "cycle": cycle,
                        "percentage": percentage_dict.get(cycle, 0),  # Initialize percentage with 0 if not found
                        "grades": []
                    }
                
                data = {
                    "name": f"{grade}°",
                    "score": score_grade
                }
                performance[cycle]["grades"].append(data)
            
            # Convert dictionary values to list
            performance_list = list(performance.values())
            
            return performance_list  # list of dictionaries
        except Exception as e:
            print(f'error {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        
    def calculate_weighted_average(self, code, year, idPrueba, db):
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_GradoCicloDesempeno"
        
        try:
            query = text(f"EXEC {procedure_name} @CODIGO=:Codigo, @ANNOA=:Anno, @IDPRUEBA=:IDPrueba, @CICLO_GRADO=:CicloGrado")
            result = db.execute(query, {"Codigo": code, "Anno": year, "IDPrueba": idPrueba or -2, "CicloGrado": -2  }).fetchall()
            
            scores = []
            
            for row in result:
                global_score = row[5]
                
                obj = {
                    "cycle": row[3],
                    "score": global_score
                }
                
                scores.append(obj)
            
            return scores
        except Exception as e:
            print(f'error {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    def calculate_componentes(self, codigoColegio, anio, grado, salon, idComponente, idArea, db):
        
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_PuntajeGlobalPorComponente"
        try:
            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @ANNO=:ANNO, @Grado=:Grado, @Salon=:Salon, @IDArea=:IDArea, @IDComponente=:IDComponente")
            result = db.execute(query, {"Codigo": codigoColegio, "ANNO": anio, "Grado": grado, "Salon": salon, "IDArea": idArea, "IDComponente": idComponente}).fetchall()
            #print(result)
            return json.loads(result[0][0])
        
        except Exception as e:
            print(f'error {e}')
            #return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
            return []
    
    def calculate_competencias(self, codigoColegio, anio, grado, salon, idCompetencia, idArea, db):
    
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_PuntajeGlobalPorCompetencia"
        try:

            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @ANNO=:ANNO, @Grado=:Grado, @Salon=:Salon, @IDArea=:IDArea, @IDCompetencia=:IDCompetencia")
            result = db.execute(query, {"Codigo": codigoColegio, "ANNO": anio, "Grado": grado, "Salon": salon, "IDArea": idArea, "IDCompetencia": idCompetencia}).fetchall()
            
            return json.loads(result[0][0])

        except Exception as e:
            print(f'error {e}')
            #return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
            return []
    
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
                            "data": avrs_list_ciclo_anterior,
                            "backgroundColor": "#026190"
                            },
                            {
                            "label": "Grado actual",
                            "data": avrs_list_grado_actual,
                            "backgroundColor": "#DC3D3D"
                            }
                        ]
                    }
            
            return json_areas
        except Exception as e:
            print(f'error {e}')
            #return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
            return []

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
                            "data": avrs_list_ciclo_anterior,
                            "backgroundColor": "#026190"
                            },
                            {
                            "label": "Grado actual",
                            "data": avrs_list_grado_actual,
                            "backgroundColor": "#DC3D3D"
                            }
                        ]
                    }
            
            return json_areas
        except Exception as e:
            print(f'error {e}')
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")

    def parameters(self, codigoColegio, anio, db):
    
        return ''
    
    def calculate_prueba_estudiantes(self, codigoColegio, anio, idPrueba, db):
    
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_ListNotas"
        try:

            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @ANNOA=:ANNOA, @IDPRUEBA=:IDPRUEBA")
            result = db.execute(query, {"Codigo": codigoColegio, "ANNOA": anio, "IDPRUEBA": idPrueba}).fetchall()
            
            print(result)
            #return json.loads(result[0][0])
            df = pl.DataFrame(result)
            #df_pandas = df.to_pandas()
            
            data = {
                'Puesto': df['column_0'].apply(lambda x: x[0]),
                'IdPrueba': df['column_0'].apply(lambda x: x[1]),
                'Nombre Prueba': df['column_0'].apply(lambda x: x[2]),
                'IdResultado': df['column_0'].apply(lambda x: x[3]),
                'Grado': df['column_0'].apply(lambda x: x[4]),
                'Salon': df['column_0'].apply(lambda x: x[5]),
                'Estudiante': df['column_0'].apply(lambda x: x[6]),
                'Nombres y Apellidos': df['column_0'].apply(lambda x: x[7]),
                'Genérico': df['column_0'].apply(lambda x: x[8]),
                'No Genérico': df['column_0'].apply(lambda x: x[9]),
                'Biología': df['column_0'].apply(lambda x: x[10]),
                'Química': df['column_0'].apply(lambda x: x[11]),
                'Física': df['column_0'].apply(lambda x: x[12]),
                'C.T.S': df['column_0'].apply(lambda x: x[13]),
                'Sociales': df['column_0'].apply(lambda x: x[14]),
                'Ciudadanas': df['column_0'].apply(lambda x: x[15]),
                'Lenguaje': df['column_0'].apply(lambda x: x[16]),
                'Inglés': df['column_0'].apply(lambda x: x[17]),
                'Definitiva': df['column_0'].apply(lambda x: x[18]),
                'Global': df['column_0'].apply(lambda x: x[19])
            }
            new_df = pd.DataFrame(data)
            new_df = new_df.fillna(0)
            new_df = new_df.to_dict(orient='records')

            lista = []

            for elemento in new_df:
            
                dicc = {
                        "id": elemento['Puesto'],
                        "grado": elemento['Grado'],
                        "lista": elemento['Estudiante'],
                        "nombre": elemento['Nombres y Apellidos'],
                        "puesto": elemento['Puesto'],
                        "genericos": elemento['Genérico'],
                        "numGenericos": elemento['No Genérico'],
                        "biologia": elemento['Biología'],
                        "quimica": elemento['Química'],
                        "fisica": elemento['Física'],
                        "cts": elemento['C.T.S'],
                        "sociales": elemento['Sociales'],
                        "ciudadanas": elemento['Ciudadanas'],
                        "lenguaje": elemento['Lenguaje'],
                        "ingles": elemento['Inglés'],
                        "definitiva": elemento['Definitiva'],
                        "global": elemento['Global'],
                        "empty": ""
                    }
            
                lista.append(dicc)
                
            #print(lista)
            return lista

        except Exception as e:
            print(f'error {e}')
            #return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
            return []
        
    def students_tasks(self, code, year, idGrade, classroom, idPrueba, idArea, taskName, db):
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_EstudiantePorAprendizaje"
        
        try:
            query = text(f"EXEC {procedure_name} @Codigo=:Codigo, @Anno=:Anno, @Grado=:Grado, @Salon=:Salon, @IDPrueba=:IDPrueba,@IDArea=:IDArea, @Tarea=:Tarea")

            students_tasks = db.execute(query, {"Codigo": code, "Anno": year, "Grado": idGrade, "Tarea": taskName, "Salon": classroom or 0, "IDPrueba": idPrueba or 0, "IDArea": idArea or 0  }).fetchall()

            if students_tasks and students_tasks[0][0] is not None:
                return json.loads(students_tasks[0][0])
                
            return []
        except Exception as e:
            print(f'error {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
        
    def detail_test(self, db):
    
        procedure_name = "BD_MARTESDEPRUEBA.dbo.SPR_Pensar_DetallePrueba"
        try:
            query = text(f"EXEC {procedure_name} ")
            result = db.execute(query, {}).fetchall()

            ejemplo = json.loads(result[0][0])
            return ejemplo["data"]        
        
        except Exception as e:
            print(f'error {e}')
            #return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="Internal Server Error")
            return []
