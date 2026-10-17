"""Demo: validación y cotización con proveedores ficticios. Sin cuentas externas ni pagos."""
import argparse, csv, datetime, hashlib, json, math, re, time
from pathlib import Path

SOURCE_URL = "https://www.workana.com/job/desarrollo-de-agente-ia-para-automatizacion-de-ventas-b2b-en-whatsapp-y-google-sheets"
MARGEN_MIN = 0.16

def crear_muestra():
    rows = []
    familias = [
        ("Office 14 i5 16/512", "Notebook", "i5 16 512 14 office", 1850),
        ("Office 15 i5 16/512", "Notebook", "i5 16 512 15 office", 1990),
        ("Gamer RTX 16/512", "Notebook", "gamer rtx 16 512", 3400),
        ("Tablet 128", "Tablet", "tablet 128", 850),
        ("Accesorio USB-C", "Accesorio", "usbc", 72),
    ]
    for idx in range(10):
        proveedor = f"Proveedor DEMO {idx+1:02d}"
        for j, (nombre, cat, spec, precio) in enumerate(familias):
            sku = f"{cat[:2].upper()}-{j+1:02d}"
            stock = (idx*3+j*5)%18
            if j==0 and idx==1: stock=0
            actual=round(precio+(idx-5)*23+(j*11),2)
            anterior=round(actual*(0.79 if idx==3 and j==0 else 1.00),2)
            rows.append({"proveedor":proveedor,"sku":sku,"nombre":nombre,"categoria":cat,"especificaciones":spec,"costo_anterior":anterior,"costo_actual":actual,"stock":stock,"entrega_dias":1+(idx+j)%5})
    rows.append({"proveedor":"Proveedor DEMO 99","sku":"INV-00","nombre":"Producto inválido","categoria":"Notebook","especificaciones":"office i5 16 512","costo_anterior":100,"costo_actual":0,"stock":-2,"entrega_dias":1})
    return rows

def precio_venta(costo,margen_min=MARGEN_MIN):
    if costo <= 0 or not 0 < margen_min < 1: raise ValueError("costo o margen inválido")
    return math.ceil(costo/(1-margen_min)/10)*10

def validacion(r):
    problemas=[]
    if float(r['costo_actual'])<=0:problemas.append('COSTO_NO_VALIDO')
    if int(r['stock'])<0:problemas.append('STOCK_NEGATIVO')
    if int(r['entrega_dias'])<0:problemas.append('ENTREGA_INVALIDA')
    if not r['sku'] or not r['nombre'] or not r['proveedor']:problemas.append('CAMPO_OBLIGATORIO_VACIO')
    return problemas

def construir_catalogo(filas):
    correctos=[];errores=[];cambios=[]
    for r in filas:
        err=validacion(r)
        if err:
            errores.append({'proveedor':r['proveedor'],'sku':r['sku'],'errores':err})
            continue
        old=float(r['costo_anterior']);new=float(r['costo_actual'])
        if old>0 and abs((new-old)/old)>=0.10:
            cambios.append({'proveedor':r['proveedor'],'sku':r['sku'],'cambio_porcentual':round((new-old)/old*100,2),'anterior':old,'actual':new})
        venta=precio_venta(new)
        correctos.append({**r,'precio_venta':venta,'margen_bruto':round((venta-new)/venta,4)})
    return correctos,errores,cambios

def extraer_intencion(mensaje):
    text=mensaje.lower()
    if 'notebook' in text or 'laptop' in text:tipo='Notebook'
    elif 'tablet' in text or 'ipad' in text:tipo='Tablet'
    else:tipo='Accesorio'
    requisitos=[]
    for tok in ('i5','16','512','office','gamer','rtx'):
        if re.search(r'(?<!\w)'+re.escape(tok)+r'(?!\w)',text):requisitos.append(tok)
    return tipo,requisitos

def cotizar(catalogo,mensaje):
    categoria,requisitos=extraer_intencion(mensaje)
    candidatos=[r for r in catalogo if r['categoria']==categoria and int(r['stock'])>0]
    def afinidad(r):return sum(int(x in r['especificaciones']) for x in requisitos)
    if not candidatos:return {'estado':'SIN_STOCK','mensaje':'No hay productos disponibles en el catálogo DEMO.'}
    max_af=max(afinidad(r) for r in candidatos)
    aptos=[r for r in candidatos if afinidad(r)==max_af]
    aptos.sort(key=lambda r:(-int(r['stock']),int(r['entrega_dias']),-float(r['margen_bruto'])))
    elegidos=aptos[:3]
    textos=[]
    for ix,r in enumerate(elegidos):
        titulo='Recomendación' if ix==0 else f'Alternativa {ix}'
        textos.append(f"{titulo}: {r['nombre']} | S/ {r['precio_venta']:.2f} | stock {r['stock']} | entrega {r['entrega_dias']} día(s).")
    return {'estado':'COTIZACION_DEMO','requisitos_detectados':requisitos,'seleccion':elegidos,'mensaje':'Cotización de DEMOSTRACIÓN — PRECIOS Y STOCK FICTICIOS, NO ENVIAR A CLIENTES.\n'+'\n'.join(textos)+'\nCondiciones de pago y entrega sujetas a confirmación.'}

def ejecutar(destino):
    t0=time.perf_counter()
    out=Path(destino);out.mkdir(parents=True,exist_ok=True)
    filas=crear_muestra();catalogo,errores,cambios=construir_catalogo(filas)
    cot=cotizar(catalogo,'Necesito notebook office i5 16/512, stock inmediato y entrega rápida.')
    with (out/'catalogo_demo.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(catalogo[0].keys()));w.writeheader();w.writerows(catalogo)
    (out/'alertas_demo.json').write_text(json.dumps({'errores':errores,'cambios_relevantes':cambios},ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'cotizacion_demo.txt').write_text(cot['mensaje'],encoding='utf-8')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    log={'ejecutado_utc':now,'fuente_demanda_publica':SOURCE_URL,'fuente_cotizaciones':'DATOS_SINTETICOS',
         'proveedores_demo':len({r['proveedor'] for r in filas if not validacion(r)}),
         'filas_procesadas':len(filas),'filas_validas':len(catalogo),'filas_rechazadas':len(errores),
         'alertas_variacion':len(cambios),'cotizacion_estado':cot['estado'],
         'opciones_cotizadas':len(cot.get('seleccion',[])),
         'margen_minimo_comprobado':all(r['margen_bruto']>=MARGEN_MIN for r in catalogo),
         'duracion_segundos':round(time.perf_counter()-t0,5),
         'salidas_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*')) if p.is_file()},
         'ventas_confirmadas':0,'cobros_confirmados':0,'clientes_contactados':0,
         'entorno':'DEMO_LOCAL: sin integración con cuentas comerciales, WhatsApp o pagos'}
    (out/'registro_prueba.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(log,ensure_ascii=False,indent=2));return log

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='resultados')
    ejecutar(parser.parse_args().out)
