import json
from datetime import datetime

def producto_mas_vendido(fecha_inicio, fecha_fin):
    with open("facturas.json", "r") as file:
        facturas = json.load(file)
    
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    
    conteo_productos = {}

    for factura in facturas:
        fecha_fac = datetime.strptime(factura["fecha"], "%Y-%m-%d")
        
        if inicio <= fecha_fac <= fin:
            for item in factura["items"]:
                codigo = item["codigo"]
                if codigo not in conteo_productos:
                    conteo_productos[codigo] = {
                        "nombre": item["nombre"],
                        "cantidad": 0
                    }
                conteo_productos[codigo]["cantidad"] += item["cantidad"]

    if not conteo_productos:
        print("No se encontraron ventas en ese rango.")
        return

    mas_vendido_id = max(conteo_productos, key=lambda x: conteo_productos[x]["cantidad"])
    resultado = {
        "codigo": mas_vendido_id,
        "nombre": conteo_productos[mas_vendido_id]["nombre"],
        "cantidad_total": conteo_productos[mas_vendido_id]["cantidad"],
        "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("reports/reporte_mas_vendido.json", "w") as out_file:
        json.dump(resultado, out_file, indent=4)
    
    print(f"Producto más vendido: {resultado['nombre']} ({resultado['cantidad_total']} unidades)")

