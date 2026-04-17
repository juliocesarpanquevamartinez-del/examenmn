import csv
import datetime 
import trab
import os
def obtener_ruta(archivo):
    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, archivo.strip("/"))

def guardar_en_csv(nombre_archivo, headers, datos):
    ruta = obtener_ruta(nombre_archivo)
    existe = True
    try: 
        with open(ruta, "r") as f: pass
    except FileNotFoundError: 
        existe = False
    ruta = obtener_ruta(nombre_archivo)
    with open(ruta, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not existe:
            writer.writeheader()
        writer.writerow(datos)
        
def leer(entity,nombre_archivo): 
    print(f"----{entity}-----")
    ruta = obtener_ruta(nombre_archivo)
    with open(ruta,"r") as f:
            lectura = csv.DictReader(f)
            for d in lectura:
                 if nombre_archivo == "Productos.csv":
                    print(f"codigo: {d['codigo']} | nombre: {d['nombre']} | valor: ${d['valor']}") 
                 elif nombre_archivo == "Mesas.csv":
                     print(f"codigo: {d['codigo']} | nombre: {d['nombre']} | Puestos: {d['puestos']}") 
                 elif nombre_archivo == "Clientes.csv":
                     print(f"Identificacion: {d['Identificacion']} | nombre: {d['nombre']} | telefono: {d['telefono']} | Email: {d['Email']}") 
                                        
def PRODUCT():
    while True:
        print("="*50)
        print("Menu Producto")
        print("1. Crear Producto ")
        print("2. Ver Productos ")
        print("3. Salir del Menu ")
        print("="*50)
        sele = input("Seleccione: ")
        if sele == "1":
            headers = ["codigo","nombre", "valor", "IVA"]
            datos = {
                "codigo": input("Código: "),
                "nombre": input("Nombre: "),
                "valor": input("Valor Unitario: "),
                "IVA": input("IVA (%): ")
            }
            guardar_en_csv("Productos.csv", headers, datos)
            print("Producto guardado.")
        elif sele == "2":
            try:
                leer("Productos","Productos.csv")
            except FileNotFoundError: print("No hay productos.")
        elif sele == "3": break

def MESAS():
    while True:
        print("="*50)
        print("Menu Mesas")
        print("1. Crear mesas ")
        print("2. Ver mesas ")
        print("3. Salir del Menu ")
        print("="*50)
        sele = input("Seleccione: ")
        if sele == "1":
            headers = ["codigo","nombre", "puestos"]
            datos = {
                "codigo": input("Código: "),
                "nombre": input("Nombre: "),
                "puestos": input("Puestos: ")
            }
            guardar_en_csv("Mesas.csv", headers, datos)
        elif sele == "2":
            try:
                leer("Mesas","Mesas.csv")
            except FileNotFoundError: print("No hay mesas.")
        elif sele == "3": break

def CLIENTES():
    while True:
        print("="*50)
        print("Menu Clientes")
        print("1. Crear clientes ")
        print("2. Ver clientes ")
        print("3. Salir del Menu ")
        print("="*50)
        sele = input("Seleccione: ")
        if sele == "1":
            headers = ["Identificacion","nombre", "telefono", "Email"]
            datos = {
                "Identificacion": input("ID: "),
                "nombre": input("Nombre: "),
                "telefono": input("Tel: "),
                "Email": input("Email: ")
            }
            guardar_en_csv("Clientes.csv", headers, datos)
        elif sele == "2":
            try:
                leer("Clientes","Clientes.csv")
            except FileNotFoundError: print("No hay clientes.")
        elif sele == "3": break

def FACTURA():
    print("--- INICIAR FACTURACIÓN ---")
    cod_m = input("Ingrese código de mesa: ")
    id_c = input("Ingrese identificación del cliente: ")

    try:
        ruta = obtener_ruta("Mesas.csv")
        with open(ruta, "r") as f:
            for m in csv.DictReader(f):
                if m['codigo'] == cod_m:
                    mesa_actual = m
        ruta = obtener_ruta("Clientes.csv")
        with open(ruta, "r") as f:
            for c in csv.DictReader(f):
                if c['Identificacion'] == id_c: cliente_actual = c
    except FileNotFoundError:
        print("Error: Archivos de Mesas o Clientes no encontrados.")
        return

    if not mesa_actual or not cliente_actual:
        print("Mesa o Cliente no encontrados.")
        return

    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    detalles = []
    total_factura = 0

    
    while True:
        cod_p = input("Código del producto: ")
        try:
            ruta = obtener_ruta("Productos.csv")
            with open(ruta, "r") as f:
                for p in csv.DictReader(f):
                    if p['codigo'] == cod_p: prod_encontrado = p
        except FileNotFoundError: break

        if prod_encontrado:
            cant = int(input(f"Cantidad de {prod_encontrado['nombre']}: "))
            v_u = float(prod_encontrado['valor'])
            iva_u = float(prod_encontrado['IVA'])
            iva_u = (iva_u/100) * v_u
            subtotal = (v_u + iva_u) * cant
            
            detalles.append({
                "codigo": cod_p, "nombre": prod_encontrado['nombre'],
                "cant": cant, "v_u": v_u, "iva": iva_u, "sub": subtotal
            })
            total_factura += subtotal
        else:
            print("Producto no existe.")
        
        if input("¿Desea agregar otro producto? (s/n): ").lower() != 's': 
            break

    
    diseno = f"\nFECHA: {fecha}\nMESA: {mesa_actual['nombre']}\n"
    diseno += f"CLIENTE: {cliente_actual['nombre']} | ID: {cliente_actual['Identificacion']}\n"
    diseno += f"TEL: {cliente_actual['telefono']} | EMAIL: {cliente_actual['Email']}\n"
    diseno += "-"*60 + "\nCOD | NOMBRE | CANT | V.UNIT | IVA | SUBTOTAL\n"
    for d in detalles:
        diseno += f"{d['codigo']} | {d['nombre']} | {d['cant']} | {d['v_u']} | {d['iva']} | {d['sub']}\n"
    diseno += "-"*60 + f"\nTOTAL A PAGAR: {total_factura}\n"
    
    print(diseno)

    if input("¿Guardar factura? (s/n): ").lower() == 's':
        with open(f"Factura_{cod_m}_{id_c}.txt", "w") as f:
             f.write(diseno)
        
        existe_v = True
        try: 
            ruta = obtener_ruta("Ventas.csv")
            with open(ruta, "r"): pass
        except: 
            existe_v = False
        ruta = obtener_ruta("Ventas.csv")
        with open(ruta, "a", newline="") as f:
            headers_v = ["fecha", "mesa", "cant_t", "bruto", "iva_t", "subtotal"]
            writer = csv.DictWriter(f, fieldnames=headers_v)
            if not existe_v: 
                writer.writeheader()
            bruto = sum(i['v_u'] * i['cant'] for i in detalles )
            iva_t = sum(i['iva'] * i['cant'] for i in detalles)
            writer.writerow({
                "fecha": fecha, 
                "mesa": cod_m, 
                "cant_t": sum(i['cant'] for i in detalles),
                "bruto": bruto, 
                "iva_t": iva_t, 
                "subtotal": total_factura
            })

        existe_det = True
        try:
            ruta = obtener_ruta("DetalleVentas.csv")
            with open(ruta, "r"): pass
        except:
            existe_det = False
        ruta = obtener_ruta("DetalleVentas.csv")
        with open(ruta, "a", newline="") as f:
            headers_det = ["fecha", "mesa", "codigo_prod", "nombre_prod", "cantidad", "subtotal_prod"]
            writer_det = csv.DictWriter(f, fieldnames=headers_det)
            
            if not existe_det:
                writer_det.writeheader()
            
            for d in detalles:
                writer_det.writerow({
                    "fecha": fecha,
                    "mesa": cod_m,
                    "codigo_prod": d['codigo'],
                    "nombre_prod": d['nombre'],
                    "cantidad": d['cant'],
                    "subtotal_prod": d['sub']
                })
        print("Venta y detalles registrados correctamente.")


def REPORTE_DE_VENTAS():
    fecha_b = input("Fecha para el reporte (YYYY-MM-DD): ")
    t_bruto, t_iva, t_final = 0, 0, 0
    encontrados = []
    
    print("\n--- RESUMEN DE VENTAS ---")
    print("Mesa | Cant | Bruto | IVA | Subtotal")
    try:
        ruta = obtener_ruta("Ventas.csv")
        with open(ruta, "r") as f:
            for v in csv.DictReader(f):
                if v['fecha'] == fecha_b:
                    print(f"{v['mesa']} | {v['cant_t']} | {v['bruto']} | {v['iva_t']} | {v['subtotal']}")
                    t_bruto += float(v['bruto'])
                    t_iva += float(v['iva_t'])
                    t_final += float(v['subtotal'])
                    encontrados.append(v)
    except FileNotFoundError: print("No hay ventas."); return

    print(f"\nTotal Venta Bruta: {t_bruto}\nTotal IVA: {t_iva}\nTotal Ventas: {t_final}")
    
    if input("¿Imprimir CSV? (s/n): ").lower() == 's':
        with open(f"Reporte_{fecha_b}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["fecha", "mesa", "cant_t", "bruto", "iva_t", "subtotal"])
            writer.writeheader()
            writer.writerows(encontrados)
def masVendi():
    if input("¿Desea ver el producto mas vendido? (s/n): ").lower() != 's': 
            return
    else:

        fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
        fecha_fin = input("Fecha inicio (YYYY-MM-DD): ")
        trab.producto_mas_vendido(fecha_inicio, fecha_fin)
