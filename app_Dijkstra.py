# -----------------------------------------------------------------
# Proyecto: Aplicación de Dijkstra en Red Vial (App.Dijkstra)
# Autor: Gemini (asistiendo a Alejandro Cinco)
# Fecha: 19 de octubre de 2025
# 
# Descripción:
# Script con GUI (Tkinter) para entrada de coordenadas y
# visualización de ruta óptima (Dijkstra) con fondo negro.
# El resumen (distancia/tiempo) se muestra en un cuadro en el mapa.
# -----------------------------------------------------------------

# --- PASO 0: IMPORTACIÓN DE LIBRERÍAS ---

# Importamos la librería osmnx y le ponemos el alias 'ox'.
# La usaremos para descargar los mapas y datos de calles.
import osmnx as ox

# Importamos networkx con el alias 'nx'.
# La usaremos para el manejo de grafos y el algoritmo de Dijkstra.
import networkx as nx

# Importamos matplotlib.pyplot con el alias 'plt'.
# La usaremos para mostrar el mapa en una ventana.
import matplotlib.pyplot as plt

# --- Importaciones para la ventana (GUI) ---

# Importamos tkinter con el alias 'tk'.
# Es la librería estándar de Python para crear ventanas e interfaces gráficas.
import tkinter as tk

# Desde tkinter, importamos 'messagebox'.
# Lo usaremos para mostrar ventanas emergentes de error o información.
from tkinter import messagebox

# Desde tkinter, importamos 'ttk' (themed tk widgets).
# Lo usaremos para crear un 'LabelFrame' con un estilo visual más moderno.
from tkinter import ttk 

# -----------------------------------------------------------------
# --- CLASE PARA MANEJAR LA VENTANA DE ENTRADA (GUI) ---
# -----------------------------------------------------------------
class VentanaCoordenadas:
    """
    Esta clase define todo el comportamiento y los componentes
    de nuestra ventana inicial de entrada de datos.
    """
    
    # El método __init__ es el "constructor". Se ejecuta automáticamente
    # cuando creamos una nueva 'VentanaCoordenadas'.
    # 'ventana_raiz' es la ventana principal de Tkinter que le pasamos.
    def __init__(self, ventana_raiz):
        
        # Guardamos la ventana raíz en una variable de la clase.
        self.ventana = ventana_raiz
        # Le ponemos un título a nuestra ventana.
        self.ventana.title("Calculadora de Ruta Óptima (Dijkstra)")
        
        # Creamos una variable 'coordenadas' y la inicializamos en 'None'.
        # Aquí guardaremos los números que el usuario ingrese.
        self.coordenadas = None
        
        # --- Creación de Widgets (Componentes de la ventana) ---
        
        # --- Origen ---
        # Creamos una etiqueta (Label) para el título "Punto de Origen".
        # 'grid' es el sistema que usamos para posicionar componentes en filas (row) y columnas (column).
        tk.Label(ventana_raiz, text="Punto de Origen", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        # Creamos la etiqueta "Latitud:". 'sticky="e"' la alinea al Este (derecha).
        tk.Label(ventana_raiz, text="Latitud:").grid(row=1, column=0, padx=5, sticky="e")
        # Creamos la caja de texto (Entry) para la latitud de origen.
        self.caja_lat_origen = tk.Entry(ventana_raiz, width=25)
        # Posicionamos la caja de texto.
        self.caja_lat_origen.grid(row=1, column=1, padx=10, pady=2)
        
        tk.Label(ventana_raiz, text="Longitud:").grid(row=2, column=0, padx=5, sticky="e")
        # Creamos la caja de texto para la longitud de origen.
        self.caja_lon_origen = tk.Entry(ventana_raiz, width=25)
        self.caja_lon_origen.grid(row=2, column=1, padx=10, pady=2)
        
        # --- Destino ---
        # Repetimos el proceso para los datos del punto de destino.
        tk.Label(ventana_raiz, text="Punto de Destino", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=(10, 5))
        
        tk.Label(ventana_raiz, text="Latitud:").grid(row=4, column=0, padx=5, sticky="e")
        self.caja_lat_destino = tk.Entry(ventana_raiz, width=25)
        self.caja_lat_destino.grid(row=4, column=1, padx=10, pady=2)
        
        tk.Label(ventana_raiz, text="Longitud:").grid(row=5, column=0, padx=5, sticky="e")
        self.caja_lon_destino = tk.Entry(ventana_raiz, width=25)
        self.caja_lon_destino.grid(row=5, column=1, padx=10, pady=2)

        # --- RECUADRO DE RECOMENDACIONES ---
        # Creamos un 'LabelFrame' (un contenedor con título) usando 'ttk'.
        marco_recomendaciones = ttk.LabelFrame(ventana_raiz, text=" Puntos de Interés (Copiar y Pegar) ")
        # Posicionamos el marco, haciendo que se expanda horizontalmente ('sticky="ew"').
        marco_recomendaciones.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Definimos una función interna para crear las cajas de recomendación.
        # Esto nos evita repetir el mismo código 3 veces.
        def crear_caja_recomendacion(etiqueta, valor_lat, valor_lon):
            # Creamos la etiqueta del lugar (ej. "Santo Domingo:").
            tk.Label(marco_recomendaciones, text=etiqueta, font=("Arial", 9, "bold")).pack(fill="x", padx=5, pady=(5,0))
            # Creamos un 'Frame' simple para agrupar la latitud y longitud en una línea.
            frame_coords = tk.Frame(marco_recomendaciones)
            frame_coords.pack(fill="x", padx=5)
            
            tk.Label(frame_coords, text="Lat:").pack(side="left")
            # Creamos la caja de texto para la latitud.
            caja_lat = tk.Entry(frame_coords, width=15)
            # Insertamos el valor de la latitud (ej. "17.0654").
            caja_lat.insert(0, valor_lat)
            # La ponemos en modo "solo lectura" para que solo se pueda copiar.
            caja_lat.config(state="readonly")
            caja_lat.pack(side="left", fill="x", expand=True, padx=(2, 5))
            
            # Hacemos lo mismo para la longitud.
            tk.Label(frame_coords, text="Lon:").pack(side="left")
            caja_lon = tk.Entry(frame_coords, width=15)
            caja_lon.insert(0, valor_lon)
            caja_lon.config(state="readonly")
            caja_lon.pack(side="left", fill="x", expand=True, padx=(2, 0))

        # Llamamos a nuestra función interna 3 veces con los datos de cada lugar.
        crear_caja_recomendacion("📍 Santo Domingo:", "17.0654", "-96.7219")
        crear_caja_recomendacion("✈️ Aeropuerto XOX:", "16.9993", "-96.7266")
        crear_caja_recomendacion("🎓 Anáhuac Oaxaca:", "16.9971", "-96.7561")

        # --- Botón de Enviar ---
        # Creamos el botón principal.
        # 'command=self.enviar_datos' le dice al botón que ejecute
        # el método 'enviar_datos' de esta clase cuando se le haga clic.
        self.boton_enviar = tk.Button(ventana_raiz, text="Calcular Ruta", font=("Arial", 10, "bold"), command=self.enviar_datos)
        # Posicionamos el botón en la fila 7.
        self.boton_enviar.grid(row=7, column=0, columnspan=2, pady=10)

    # Este método se activa al presionar el botón "Calcular Ruta".
    def enviar_datos(self):
        # Usamos un bloque 'try...except' para validar la entrada.
        try:
            # Intentamos convertir el texto de cada caja a un número decimal (float).
            latitud_origen = float(self.caja_lat_origen.get())
            longitud_origen = float(self.caja_lon_origen.get())
            latitud_destino = float(self.caja_lat_destino.get())
            longitud_destino = float(self.caja_lon_destino.get())
            
            # Si todas las conversiones fueron exitosas, guardamos los números
            # en nuestro diccionario 'self.coordenadas'.
            self.coordenadas = {
                'lat_origen': latitud_origen,
                'lon_origen': longitud_origen,
                'lat_destino': latitud_destino,
                'lon_destino': longitud_destino
            }
            # Destruimos (cerramos) la ventana de Tkinter.
            # Esto hará que el script principal continúe.
            self.ventana.destroy()
            
        except ValueError:
            # Si 'float()' falla (ej. si el usuario escribió "abc"),
            # se ejecuta este bloque.
            # Mostramos una ventana emergente de error.
            messagebox.showerror("Error de Entrada", "Por favor, introduce solo números válidos.")

    # Este método es llamado por el script principal.
    def obtener_coordenadas(self):
        # 'self.ventana.wait_window()' es la magia de Tkinter.
        # Pausa la ejecución del script aquí mismo y espera
        # hasta que 'self.ventana' sea destruida (lo cual hacemos en 'enviar_datos').
        self.ventana.wait_window()
        # Una vez que la ventana se cierra, devolvemos el diccionario
        # 'self.coordenadas' (que tendrá datos o seguirá siendo 'None' si cerraron con la 'X').
        return self.coordenadas

# -----------------------------------------------------------------
# --- FUNCIÓN PRINCIPAL DE ANÁLISIS DE RUTA ---
# -----------------------------------------------------------------
# Metemos todo nuestro código de análisis en una gran función
# que acepta el diccionario 'coordenadas' como argumento.
def ejecutar_analisis_ruta(coordenadas):
    
    # Configuramos OSMnx para que muestre mensajes en la consola
    # y use el caché para no descargar el mapa cada vez.
    ox.settings.log_console = True
    ox.settings.use_cache = True
    
    # --- PASO 1: DESCARGA Y MODELADO DEL MAPA ---
    # Definimos la lista de lugares que queremos descargar.
    lista_de_lugares = [
        "Oaxaca de Juárez, Oaxaca, Mexico",
        "Santa Cruz Xoxocotlán, Oaxaca, Mexico",
        "San Raymundo Jalpan, Oaxaca, Mexico",
        "San Antonio de la Cal, Oaxaca, Mexico",
        "San Agustín de las Juntas, Oaxaca, Mexico"
    ]
    
    print(f"Iniciando la descarga de la red vial para: {lista_de_lugares}")
    print("... esto puede tardar varios minutos la primera vez ...")

    try:
        # Usamos 'ox.graph_from_place' para descargar el mapa.
        # 'network_type="drive"' filtra solo calles para autos.
        # El grafo que devuelve está en coordenadas (Latitud, Longitud).
        grafo_original_latlon = ox.graph_from_place(lista_de_lugares, network_type='drive', simplify=True)
        print("¡Grafo en Latitud/Longitud descargado exitosamente!")
    except Exception as e:
        # Si falla la descarga (ej. sin internet), informamos y terminamos.
        print(f"Error crítico al descargar el grafo: {e}")
        return # Salimos de la función

    # Proyectamos el grafo. Lo convertimos de (Lat, Lon) a un
    # sistema de coordenadas en Metros (UTM).
    # ¡Esto es crucial para que 'length' (longitud) esté en metros!
    grafo_proyectado_metros = ox.project_graph(grafo_original_latlon)
    print("¡Grafo proyectado a metros (UTM) exitosamente!")

    # --- PASO 2: CÁLCULO DE PESOS (TIEMPO DE VIAJE) ---
    print("Iniciando cálculo de pesos (tiempo de viaje)...")
    # Definimos nuestras constantes
    VELOCIDAD_POR_DEFECTO_KMH = 20.0
    FACTOR_CONVERSION_MS = 3.6
    
    # Obtenemos una lista de TODAS las aristas (calles) y sus datos.
    aristas_del_grafo = list(grafo_proyectado_metros.edges(keys=True, data=True))
    
    # Creamos diccionarios vacíos para guardar los nuevos atributos
    diccionario_velocidades_kmh = {}
    diccionario_tiempos_segundos = {}

    # Iteramos sobre cada arista (calle) que obtuvimos
    # (nodo_u, nodo_v, clave_arista) es el ID único de la arista.
    # 'datos_arista' es un diccionario con la info (length, maxspeed, etc.)
    for nodo_u, nodo_v, clave_arista, datos_arista in aristas_del_grafo:
        
        id_arista = (nodo_u, nodo_v, clave_arista)
        # Asumimos la velocidad por defecto al inicio
        velocidad_calle_kmh = VELOCIDAD_POR_DEFECTO_KMH
        
        # Revisamos si la arista tiene el atributo 'maxspeed'
        if 'maxspeed' in datos_arista:
            dato_velocidad_maxima = datos_arista['maxspeed']
            # Hacemos un 'try...except' porque este dato puede ser
            # una lista ['40', '50'] o un string '60 km/h'.
            try:
                if isinstance(dato_velocidad_maxima, list):
                    # Si es una lista, la limpiamos y sacamos el promedio
                    lista_valores_velocidad = [float(val.split()[0]) for val in dato_velocidad_maxima if val.split()[0].isdigit()]
                    if lista_valores_velocidad:
                        velocidad_calle_kmh = sum(lista_valores_velocidad) / len(lista_valores_velocidad)
                elif isinstance(dato_velocidad_maxima, str):
                    # Si es un string, extraemos solo el número
                    partes_velocidad = dato_velocidad_maxima.split()
                    if partes_velocidad[0].isdigit():
                        velocidad_calle_kmh = float(partes_velocidad[0])
            except Exception:
                # Si algo falla, no hacemos nada y se queda la velocidad por defecto
                velocidad_calle_kmh = VELOCIDAD_POR_DEFECTO_KMH
        
        # Obtenemos la longitud en metros (que ya viene en 'datos_arista')
        longitud_calle_metros = datos_arista['length']
        # Convertimos la velocidad a metros/segundo
        velocidad_calle_ms = velocidad_calle_kmh / FACTOR_CONVERSION_MS
        
        # Calculamos el tiempo en segundos (Tiempo = Distancia / Velocidad)
        # Si la velocidad es 0, asignamos un tiempo "infinito"
        tiempo_viaje_segundos = longitud_calle_metros / velocidad_calle_ms if velocidad_calle_ms > 0 else float('inf')
        
        # Guardamos los nuevos valores en nuestros diccionarios
        diccionario_velocidades_kmh[id_arista] = velocidad_calle_kmh
        diccionario_tiempos_segundos[id_arista] = tiempo_viaje_segundos

    # Ahora, asignamos todos los nuevos atributos al grafo de una sola vez
    nx.set_edge_attributes(grafo_proyectado_metros, diccionario_velocidades_kmh, 'velocidad_kmh')
    nx.set_edge_attributes(grafo_proyectado_metros, diccionario_tiempos_segundos, 'tiempo_viaje_segundos')
    print("¡Pesos (tiempo_viaje_segundos) calculados!")

    # --- PASO 3: SELECCIÓN DE PUNTOS Y CÁLCULO DE RUTA ---
    
    # Inicializamos la ruta como 'None'
    ruta_optima_nodos = None
    try:
        # Obtenemos las coordenadas del diccionario que recibimos de la GUI
        latitud_origen = coordenadas['lat_origen']
        longitud_origen = coordenadas['lon_origen']
        latitud_destino = coordenadas['lat_destino']
        longitud_destino = coordenadas['lon_destino']
        
        print("Buscando nodos (intersecciones) más cercanos...")
        
        # Definimos una función rápida para encontrar el nodo más cercano
        def obtener_nodo_mas_cercano(grafo, lat, lon):
            # IMPORTANTE: Usamos el grafo 'grafo_original_latlon'
            # porque está en (Lat, Lon), igual que nuestras coordenadas.
            # 'ox.nearest_nodes' espera las coordenadas en orden (X, Y), es decir, (Longitud, Latitud).
            return ox.nearest_nodes(grafo, X=lon, Y=lat)

        # Buscamos el nodo de inicio más cercano
        nodo_origen = obtener_nodo_mas_cercano(grafo_original_latlon, latitud_origen, longitud_origen)
        # Buscamos el nodo de fin más cercano
        nodo_destino = obtener_nodo_mas_cercano(grafo_original_latlon, latitud_destino, longitud_destino)
        
        print(f"-> Nodo de Origen (ID): {nodo_origen}")
        print(f"-> Nodo de Destino (ID): {nodo_destino}")

        print("\nCalculando la ruta óptima usando Dijkstra...")
        # ¡Esta es la llamada al algoritmo de Dijkstra!
        # Le pedimos a 'networkx' que encuentre el camino más corto ('shortest_path')
        # Usamos 'grafo_proyectado_metros' porque tiene los atributos en metros.
        # 'weight='tiempo_viaje_segundos'' es la clave: le decimos a Dijkstra
        # que minimice la suma de este atributo, no la distancia.
        ruta_optima_nodos = nx.shortest_path(
            grafo_proyectado_metros,
            source=nodo_origen,
            target=nodo_destino,
            weight='tiempo_viaje_segundos'
        )
        print("¡Ruta óptima (basada en tiempo) encontrada!")

    except nx.NetworkXNoPath:
        # Esto pasa si no hay un camino posible (ej. calles desconectadas)
        print(f"ERROR: No se encontró una ruta transitable entre los nodos seleccionados.")
    except Exception as e:
        # Capturamos cualquier otro error
        print(f"Ha ocurrido un error inesperado durante el cálculo de ruta: {e}")

    # --- PASO 4: VISUALIZACIÓN Y RESUMEN DE RESULTADOS (CUADRO DE TEXTO CORREGIDO) ---

    # Verificamos si 'ruta_optima_nodos' se pudo calcular
    if ruta_optima_nodos:
        
        # 1. --- Calcular Resumen del Recorrido (Método Manual) ---
        # Inicializamos nuestros contadores
        distancia_total_metros = 0
        tiempo_total_segundos = 0
        
        # Iteramos sobre los pares de nodos (calles) de la ruta
        for nodo_u, nodo_v in zip(ruta_optima_nodos[:-1], ruta_optima_nodos[1:]):
            # Obtenemos las aristas paralelas (si existen)
            datos_multiples_aristas = grafo_proyectado_metros.get_edge_data(nodo_u, nodo_v)
            # Elegimos la arista que Dijkstra eligió (la de menor tiempo)
            arista_optima = min(datos_multiples_aristas.values(), key=lambda x: x['tiempo_viaje_segundos'])
            
            # Sumamos los valores de esa arista a nuestros totales
            distancia_total_metros += arista_optima['length']
            tiempo_total_segundos += arista_optima['tiempo_viaje_segundos']

        # Convertimos las unidades para que sean legibles
        distancia_total_km = distancia_total_metros / 1000
        tiempo_total_minutos = tiempo_total_segundos / 60
        
        # 2. --- Mostrar Resumen en Consola (como respaldo) ---
        print("\n--- RESUMEN DE LA RUTA ÓPTIMA (basada en TIEMPO) ---")
        print(f"Distancia Física Total: {distancia_total_km:.2f} km")
        print(f"Tiempo Estimado de Viaje: {tiempo_total_minutos:.2f} minutos")
        
        # 3. --- Generar Visualización del Mapa (Estilo Original Negro) ---
        print("Generando el mapa de la ruta...")
        
        # Creamos la figura y los ejes usando la función de OSMnx
        figura, eje = ox.plot_graph_route(
            grafo_proyectado_metros,
            ruta_optima_nodos,
            route_color='cyan',
            route_linewidth=3,
            route_alpha=0.8,
            orig_dest_size=100,
            ax=None,
            node_size=0,
            edge_linewidth=0.5,
            edge_color='#999999',
            bgcolor='k',                # Fondo NEGRO
            figsize=(15, 15),
            show=False,                 # <-- ¡¡LA CORRECCIÓN ESTÁ AQUÍ!!
            close=False                 # <-- ¡¡Y AQUÍ!!
        )
        
        # --- INICIO DE LA MODIFICACIÓN (CUADRO DE TEXTO) ---
        
        # 4.A. Añadimos un título simple al mapa
        eje.set_title(
            "Ruta Óptima de Oaxaca (Dijkstra por Tiempo)",
            fontsize=20,
            color='white' # Color de texto blanco
        )

        # 4.B. Creamos el texto del resumen que vimos en la consola
        texto_resumen = (
            f"Distancia Física Total: {distancia_total_km:.2f} km\n"
            f"Tiempo Estimado de Viaje: {tiempo_total_minutos:.2f} min"
        )
        
        # 4.C. Añadimos el cuadro de texto (bbox) al mapa
        # Usamos eje.text() para poner texto sobre los ejes (el mapa)
        eje.text(
            0.03,                           # Posición X: 3% desde la izquierda
            0.97,                           # Posición Y: 97% desde abajo (casi arriba)
            texto_resumen,                  # El string que acabamos de crear
            transform=eje.transAxes,        # Coordenadas relativas a los ejes (de 0 a 1)
            fontsize=14,
            color='black',                  # Letra NEGRA para alto contraste
            verticalalignment='top',        # Alineamos el texto desde su parte superior
            # 'bbox' dibuja una caja alrededor del texto
            bbox=dict(boxstyle='round,pad=0.5', # Estilo: redondeado, con relleno
                      fc='white',               # Relleno BLANCO
                      ec='cyan',                # 'edgecolor' (borde): cyan
                      lw=1,                     # 'linewidth' (grosor borde): 1
                      alpha=0.8)                # Transparencia de la caja (blanca semitransparente)
        )
        # --- FIN DE LA MODIFICACIÓN ---

        print("Mostrando mapa. Cierra la ventana del mapa para terminar el script.")
        # 5. Finalmente, mostramos la ventana de Matplotlib con el mapa
        #    (Esto ahora funciona porque 'show=False' detuvo a OSMnx)
        plt.show()

    else:
        # Esto se ejecuta si 'ruta_optima_nodos' sigue siendo 'None'
        print("\nNo se pudo calcular una ruta.")
        # Mostramos un mensaje emergente para informar al usuario
        messagebox.showinfo("Resultado", "No se pudo encontrar una ruta transitable con los puntos seleccionados.")

    print("\n--- Fin del programa ---")

# -----------------------------------------------------------------
# --- BLOQUE DE EJECUCIÓN PRINCIPAL ---
# -----------------------------------------------------------------
# Esta condición especial '__name__ == "__main__"'
# se asegura de que este código solo se ejecute
# cuando corremos este archivo .py directamente.
if __name__ == "__main__":
    
    # 1. Creamos la ventana "raíz" o principal de Tkinter.
    ventana_raiz = tk.Tk()
    
    # 2. Creamos una instancia de nuestra clase 'VentanaCoordenadas'
    #    y le pasamos la ventana raíz para que dibuje sobre ella.
    aplicacion_gui = VentanaCoordenadas(ventana_raiz)
    
    # 3. Llamamos al método que pausará el script
    #    y esperará a que el usuario interactúe con la ventana.
    #    La variable 'coordenadas_ingresadas' recibirá el diccionario
    #    o 'None'.
    coordenadas_ingresadas = aplicacion_gui.obtener_coordenadas()
    
    # 4. Verificamos si 'coordenadas_ingresadas' tiene datos.
    #    (Si el usuario cerró con la 'X', será 'None' y esto será 'False').
    if coordenadas_ingresadas:
        print("Coordenadas recibidas, iniciando análisis...")
        print(coordenadas_ingresadas)
        # 5. ¡Llamamos a nuestra función principal de análisis
        #    y le pasamos los datos de la GUI!
        ejecutar_analisis_ruta(coordenadas_ingresadas)
    else:
        # Si 'coordenadas_ingresadas' es 'None'
        print("Operación cancelada por el usuario.")