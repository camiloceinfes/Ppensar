#from app.producto import producto
from app.product_creator import Ppensar_Creator

class pensar():

    def componentes(self, grado, salon, area, comp, db):
        return Ppensar_Creator().create_product(grado, salon, area, comp, db)

