""" Abstrac Product Class """

from pensar.models.models import componentes_model, competencias_model
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import polars as pl
import pandas as pd

class producto():

    def calculate_componentes(self):
        pass
    
class Ppensar(producto):
    
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