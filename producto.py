""" Abstrac Product Class """

from app.pensar.models.models import pensar
from sqlalchemy import or_, and_
import numpy as np

class producto():

    def calculate_componentes(self):
        pass
    
class Ppensar(producto):
    
    def calculate_componentes(self, grado, salon, area, comp, db):
        
        lista = []
        lista_filtro = []
        lista_filtro.append(pensar.grado == grado)
        if salon != None:
            lista_filtro.append(pensar.salon == salon)
        if area != None:
            lista_filtro.append(pensar.area == area)
        if comp != None:
            lista_filtro.append(pensar.componente == comp)

        consulta1 = db.query(pensar.tipo_rejilla, pensar.componente, pensar.ciclo_anterior_plantel, 
                        pensar.ciclo_anterior_nacional ,pensar.ciclo_actual_nacional, pensar.ciclo_actual_plantel
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