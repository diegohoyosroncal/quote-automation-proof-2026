import unittest
from motor import crear_muestra, construir_catalogo, precio_venta, cotizar, MARGEN_MIN

class MotorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogo,cls.errores,cls.cambios=construir_catalogo(crear_muestra())
    def test_diez_proveedores(self):
        self.assertEqual(len({x['proveedor'] for x in self.catalogo}),10)
    def test_cincuenta_productos(self):
        self.assertEqual(len(self.catalogo),50)
    def test_precio_respeta_margen(self):
        self.assertTrue(all(x['margen_bruto']>=MARGEN_MIN for x in self.catalogo))
    def test_precio_invalido(self):
        with self.assertRaises(ValueError):precio_venta(0)
    def test_alerta_variacion(self):
        self.assertGreaterEqual(len(self.cambios),1)
    def test_anomalia_detectada(self):
        self.assertEqual(self.errores[0]['errores'],['COSTO_NO_VALIDO','STOCK_NEGATIVO'])
    def test_cotizacion_tres_opciones(self):
        q=cotizar(self.catalogo,'notebook office i5 16/512')
        self.assertEqual(q['estado'],'COTIZACION_DEMO')
        self.assertEqual(len(q['seleccion']),3)
    def test_prioridad_stock_antes_que_entrega(self):
        q=cotizar(self.catalogo,'notebook office i5 16/512')
        opts=q['seleccion']
        self.assertEqual([x['stock'] for x in opts],sorted([x['stock'] for x in opts],reverse=True))
    def test_ninguna_salida_autoriza_envio(self):
        q=cotizar(self.catalogo,'notebook i5 16/512')
        self.assertIn('FICTICIOS',q['mensaje'])
    def test_caso_que_no_hay_stock(self):
        q=cotizar([],'tablet 128')
        self.assertEqual(q['estado'],'SIN_STOCK')

if __name__=='__main__':unittest.main(verbosity=2)
