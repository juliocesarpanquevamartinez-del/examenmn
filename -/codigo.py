import funcionees as f
while True:
        print("="*50)
        print("-----Menu Principal-----")
        print("1. Menu Producto ")
        print("2. Menu Mesas")
        print("3. Menu Clientes ")
        print("4. facturar ")
        print("5. reporte de ventas ")
        print("6. ver producto mas vendido  ")
        print("7. salir del menu  ")
        print("="*50)
        sele = input("Opción: ")
        
        match sele :
            case "1": f.PRODUCT()
            case "2": f.MESAS()
            case "3": f.CLIENTES()
            case "4": f.FACTURA()
            case "5": f.REPORTE_DE_VENTAS()
            case "6": f.masVendi()
            case "7": 
                print("saliste del menu ") 
                break
            case _: print("opcion invalida ")