### EXPORTA LISTA M3U DE 2 LINEAS A ARCHIVO PLANO CSV (INCLUYE CAMPO tvg_name) ###

import csv

# Definir el archivo m3u
# archivo_m3u = os.getcwd() + "\ip.m3u"
archivo_m3u = "listaiptv.m3u"
archivo_csv = archivo_m3u.split("/")[-1].split(".")[0] + ".csv" 

# Lista para almacenar los datos
datos = []

# Abrir el archivo m3u en modo lectura
with open(archivo_m3u, "r") as f:
    for linea in f:
        # Buscar las etiquetas
        if linea.startswith("#EXTINF:"):
            # Obtener el valor de tvg-id
            tvg_id = linea.split('"')[1].rstrip()

            # Obtener el valor de tvg_name
            # .upper() se utiliza para ponerlo en mayusculas
            tvg_name = linea.split('"')[3].rstrip().upper()

            # Obtener el valor de tvg-logo
            tvg_logo = linea.split('"')[5].rstrip()

            # Obtener el valor de group-title 
            # .upper() se utiliza para ponerlo en mayusculas
            group_title = linea.split('"')[7].rstrip().upper()

            # Obtener el valor final
            # .upper() se utiliza para ponerlo en mayusculas
            valor_final = linea.split(",")[1].strip().rstrip().upper()

            # Leer la siguiente linea para obtener la web
            siguiente_linea = next(f, None)  # Leer la siguiente linea (puede ser None)

            # Si la siguiente linea no es None, obtener la URL
            if siguiente_linea:
                url = siguiente_linea.strip()  # Extraer URL solo si existe la linea
            else:
                # Si no hay una siguiente linea, se omite la entrada actual
                continue  # Omitir la entrada actual si no hay una URL


            # Agregar los datos a la lista, incluyendo la URL
            #datos.append([tvg_id, tvg_logo, group_title, valor_final, url])
            #datos.append([valor_final,tvg_name, group_title, tvg_logo, tvg_id, url])
            datos.append([tvg_name, group_title, tvg_logo, tvg_id, url])

# Escribir los datos a un archivo CSV
#with open(archivo_csv, "w", newline="") as f:
with open(archivo_csv, "w") as f:  # Sin newline=""
    writer = csv.writer(f)
    #writer.writerow(["tvg-id", "tvg-logo", "group-title", "Canal", "url"])
    writer.writerow(["CANAL","GRUPO","LOGO", "ID CANAL EN GUIA EPG", "FUENTE URL"])
    writer.writerows(datos)

### LEE EL ARCHIVO RESULTANTE Y LO REESCRIBE ELIMINANDO LAS LINEAS VACIAS

import pandas as pd

# Leer el archivo CSV como DataFrame
df = pd.read_csv(archivo_csv)

# Eliminar filas vacias
filas_eliminadas = df.dropna(how="all").shape[0]
df = df.dropna(how="all")

# Guarda el DataFrame sin lineas vacias
df.to_csv(archivo_csv, index=False)

#print(f"Las lineas vacias se han eliminado del archivo {df.shape[0]} lineas del archivo CSV '{archivo_csv}'.")
#print('Las lineas vacias se han eliminado del archivo ', {df.shape[0]} '{archivo_csv}')
#print("Canal: " + valor_final)

# Crear el codigo HTML
html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informacion del archivo CSV</title>
</head>
<body>
    <h1>Informacion del archivo CSV</h1>
    <p>Se ha generado el archivo CSV con la siguiente informacion:</p>
    <ul>
        <li>Numero de canales: """ + str(filas_eliminadas) + """</li>
        <li>Nombre del archivo m3u: """ + archivo_m3u + """</li>
        <li>Ubicacion del archivo csv: """ + archivo_csv + """</li>
    </ul>
    ...
</body>
</html>
"""

# Escribir el contenido HTML a un archivo
with open("resultado.html", "w") as f:
    f.write(html)

# Imprimir mensaje final con el metodo format
#print("!Proceso terminado! Se han extraido {} canales al archivo {} ".format(filas_eliminadas, archivo_csv))
# mensaje final
print("!Proceso terminado! Se han extraido " +  str(filas_eliminadas) + " canales al archivo " + archivo_csv )
