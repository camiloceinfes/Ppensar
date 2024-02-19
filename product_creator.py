from producto import Ppensar


""" Abstrac Product Creator """

class productoCreator():

    def create_product(self):
        pass

class Ppensar_Creator(productoCreator):

    def create_product(self, grado, salon, area, comp, db):
        return Ppensar().calculate_componentes(grado, salon, area, comp, db)
    
    def create_product(self, idColegio, db):
        return Ppensar().calculate_competencias(idColegio, db)

# class Mprueba_Creator(productoCreator):

#     def create_product(self):
#         pass