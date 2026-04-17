#import json
#from datetime import datetime
#
#def producto_mas_vendido(fecha_inicio, fecha_fin):
#    with open("facturas.json", "r") as file:
#        facturas = json.load(file)
#    
#    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
#    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
#    
#    conteo_productos = {}
#
#    for factura in facturas:
#        fecha_fac = datetime.strptime(factura["fecha"], "%Y-%m-%d")
#        
#        if inicio <= fecha_fac <= fin:
#            for item in factura["items"]:
#                codigo = item["codigo"]
#                if codigo not in conteo_productos:
#                    conteo_productos[codigo] = {
#                        "nombre": item["nombre"],
#                        "cantidad": 0
#                    }
#                conteo_productos[codigo]["cantidad"] += item["cantidad"]
#
#    if not conteo_productos:
#        print("No se encontraron ventas en ese rango.")
#        return
#
#    mas_vendido_id = max(conteo_productos, key=lambda x: conteo_productos[x]["cantidad"])
#    resultado = {
#        "codigo": mas_vendido_id,
#        "nombre": conteo_productos[mas_vendido_id]["nombre"],
#        "cantidad_total": conteo_productos[mas_vendido_id]["cantidad"],
#        "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#    }
#
#    with open("reports/reporte_mas_vendido.json", "w") as out_file:
#        json.dump(resultado, out_file, indent=4)
#    
#    print(f"Producto más vendido: {resultado['nombre']} ({resultado['cantidad_total']} unidades)")
#
import csv
from datetime import datetime
import os
def obtener_ruta(archivo):
    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, archivo.strip("/"))

def producto_mas_vendido(fecha_inicio, fecha_fin):
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        
        conteo_productos = {}
        ruta = obtener_ruta("DetalleVentas.csv")
        with open(ruta, "r", newline="") as f:
            lectura = csv.DictReader(f)
            
            for fila in lectura:
                
                fecha_fila = datetime.strptime(fila["fecha"], "%Y-%m-%d")
                
                
                if inicio <= fecha_fila <= fin:
                    codigo = fila["codigo_prod"]
                    cantidad = int(fila["cantidad"])
                    nombre = fila["nombre_prod"]
                    
                    if codigo not in conteo_productos:
                        conteo_productos[codigo] = {
                            "nombre": nombre,
                            "cantidad": 0
                        }
                    conteo_productos[codigo]["cantidad"] += cantidad

        if not conteo_productos:
            print("No se encontraron ventas en ese rango de fechas.")
            return

        
        mas_vendido_id = max(conteo_productos, key=lambda x: conteo_productos[x]["cantidad"])
        
        resultado = {
            "codigo": mas_vendido_id,
            "nombre": conteo_productos[mas_vendido_id]["nombre"],
            "cantidad_total": conteo_productos[mas_vendido_id]["cantidad"],
            "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        
        try:
            ruta = obtener_ruta("reporte_mas_vendido.json")
            with open(ruta, "w") as out_file:
                import json
                json.dump(resultado, out_file, indent=4)
        except Exception as e:
            print(f"No se pudo guardar el archivo de reporte: {e}")
        
        print("\n" + "*"*30)
        print(f"PRODUCTO MÁS VENDIDO: {resultado['nombre']}")
        print(f"CANTIDAD TOTAL: {resultado['cantidad_total']} unidades")
        print("*"*30 + "\n")

    except FileNotFoundError:
        print("Error: Aún no existe el archivo 'DetalleVentas.csv'. Realice una venta primero.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")