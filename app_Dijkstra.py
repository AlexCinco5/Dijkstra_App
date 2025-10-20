# Importamos la librería osmnx y le ponemos el alias 'ox' que usaremos para descargar los mapas y datos de calles.
# Importamos networkx con el alias 'nx' que usaremos para el manejo de grafos y el algoritmo de Dijkstra.
# Importamos matplotlib.pyplot con el alias 'plt' que usaremos para mostrar el mapa en una ventana.
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Aquí hago una división ya que lo siguiente se usa para la interfaz gráfica
# Importamos tkinter con el alias 'tk' que usaremos para crear ventanas e interfaces gráficas.
# Desde tkinter, importamos 'messagebox' que usaremos para mostrar ventanas emergentes de error o información.
# Desde tkinter, importamos "ttk" que usaremos para crear un "LabelFrame" con un estilo visual más moderno.

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 

# Ahora vamos a crear una clase que contendrá toda la lógica de nuestra ventana gráfica para ingresar las coordenadas
class VentanaCoordenadas:
    # El método __init__ es el "constructor", se ejecuta automáticamente cuando creamos una nueva "VentanaCoordenadas" y la "ventana_raiz" es la ventana principal de Tkinter que le pasamos como argumento
    def __init__(self, ventana_raiz):
        # Guardamos la ventana raíz en una variable de la clase para usarla después
        self.ventana = ventana_raiz
        self.ventana.title("Calculador de la Ruta más Óptima con Dijkstra") # Este es el título de nuestra ventana
        
        # Creamos una variable 'coordenadas' y la inicializamos en 'None' que es el valor por defecto y aquí guardaremos los números que el usuario ingrese
        self.coordenadas = None
        # Aquí comenzamos a crear los componentes gráficos (etiquetas, cajas de texto, botones, etc.) todo lo que el usuario verá e interactuará
        # Creamos una etiqueta (Label) para el título "Punto de Origen" y 'grid' es el sistema que usamos para posicionar componentes en filas (row) y columnas (column)
        tk.Label(ventana_raiz, text="Punto de Origen", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        # Creamos la etiqueta "Latitud:" y 'sticky="e"' la alinea a la derecha
        tk.Label(ventana_raiz, text="Latitud:").grid(row=1, column=0, padx=5, sticky="e")
        # Creamos la caja de texto (Entry) para la latitud de origen
        self.caja_lat_origen = tk.Entry(ventana_raiz, width=25)
        # Posicionamos la caja de texto en su lugar para mejor apariencia
        self.caja_lat_origen.grid(row=1, column=1, padx=10, pady=2)
        # Repetimos el proceso para la longitud de origen
        tk.Label(ventana_raiz, text="Longitud:").grid(row=2, column=0, padx=5, sticky="e")
        # Creamos la caja de texto para la longitud de origen
        self.caja_lon_origen = tk.Entry(ventana_raiz, width=25)
        self.caja_lon_origen.grid(row=2, column=1, padx=10, pady=2)
        
        # Repetimos el proceso para los datos del punto de destino y quedaría listo
        tk.Label(ventana_raiz, text="Punto de Destino", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=(10, 5))
        
        tk.Label(ventana_raiz, text="Latitud:").grid(row=4, column=0, padx=5, sticky="e")
        self.caja_lat_destino = tk.Entry(ventana_raiz, width=25)
        self.caja_lat_destino.grid(row=4, column=1, padx=10, pady=2)
        
        tk.Label(ventana_raiz, text="Longitud:").grid(row=5, column=0, padx=5, sticky="e")
        self.caja_lon_destino = tk.Entry(ventana_raiz, width=25)
        self.caja_lon_destino.grid(row=5, column=1, padx=10, pady=2)

        # Ahora generamos un recuadro con algunas recomendaciones por si el usuario no sabe qué coordenadas ingresar
        # Primero creamos un 'LabelFrame' (un contenedor con título) usando 'ttk' para un mejor estilo visual
        marco_recomendaciones = ttk.LabelFrame(ventana_raiz, text=" Puntos de Interés (Copiar y Pegar) ")
        # Posicionamos el marco, haciendo que se expanda horizontalmente con 'sticky="ew"'
        marco_recomendaciones.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Posteriormente, definimos una función interna para crear las cajas de recomendación y esto nos evitará repetir el mismo código 3 veces
        def crear_caja_recomendacion(etiqueta, valor_lat, valor_lon):
            # Creamos la etiqueta del lugar
            tk.Label(marco_recomendaciones, text=etiqueta, font=("Arial", 9, "bold")).pack(fill="x", padx=5, pady=(5,0))
            # Creamos un 'Frame' simple para agrupar la latitud y longitud en una sola línea
            frame_coords = tk.Frame(marco_recomendaciones)
            frame_coords.pack(fill="x", padx=5)
            
            tk.Label(frame_coords, text="Lat:").pack(side="left")
            # Creamos la caja de texto para la latitud
            caja_lat = tk.Entry(frame_coords, width=15)
            # Insertamos el valor de la latitud en la caja
            caja_lat.insert(0, valor_lat)
            # La ponemos en modo "solo lectura" para que solo se pueda copiar y no modificar
            caja_lat.config(state="readonly")
            caja_lat.pack(side="left", fill="x", expand=True, padx=(2, 5))
            
            # Hacemos lo mismo para la longitud y listo
            tk.Label(frame_coords, text="Lon:").pack(side="left")
            caja_lon = tk.Entry(frame_coords, width=15)
            caja_lon.insert(0, valor_lon)
            caja_lon.config(state="readonly")
            caja_lon.pack(side="left", fill="x", expand=True, padx=(2, 0))

        # Llamamos a nuestra función interna 3 veces para crear las recomendaciones personalizadas
        crear_caja_recomendacion("Santo Domingo:", "17.0654", "-96.7219")
        crear_caja_recomendacion("Aeropuerto XOX:", "17.001766", "-96.722585")
        crear_caja_recomendacion("Anáhuac Oaxaca:", "16.998783", "-96.751939")

        # Finalmente, creamos el botón "Calcular Ruta" y con 'command=self.enviar_datos' le decimos al botón que ejecute el método 'enviar_datos' de esta clase
        self.boton_enviar = tk.Button(ventana_raiz, text="Calcular Ruta", font=("Arial", 10, "bold"), command=self.enviar_datos)
        # Posicionamos el botón en su lugar y listo, terminamos la interfaz gráfica
        self.boton_enviar.grid(row=7, column=0, columnspan=2, pady=10)

    # Este método se activa al presionar el botón "Calcular Ruta" y en él validamos y guardamos los datos ingresados
    def enviar_datos(self):
        # Usamos un bloque 'try except' para validar la entrada y que los datos sean números válidos
        try:
            # Intentamos convertir el texto de cada caja a un número decimal para latitud y longitud
            latitud_origen = float(self.caja_lat_origen.get())
            longitud_origen = float(self.caja_lon_origen.get())
            latitud_destino = float(self.caja_lat_destino.get())
            longitud_destino = float(self.caja_lon_destino.get())

            # Si todas las conversiones fueron exitosas, guardamos los números en nuestro diccionario 'self.coordenadas' que usará el script principal
            self.coordenadas = {
                'lat_origen': latitud_origen,
                'lon_origen': longitud_origen,
                'lat_destino': latitud_destino,
                'lon_destino': longitud_destino
            }
            # Cerramos la ventana ya que los datos son válidos y el script puede continuar
            self.ventana.destroy()
            
        except ValueError:
            # Si la conversión 'float()' falla,se ejecuta este bloque y mostramos un mensaje de error
            messagebox.showerror("Error", "Introduce solo valores válidos de latitud y longitud (números decimales).")

    # Este método es llamado por el script principal para obtener las coordenadas ingresadas por el usuario
    def obtener_coordenadas(self):
        # 'self.ventana.wait_window()' pausa la ejecución del script aquí mismo y espera hasta que 'self.ventana' sea cerrada
        self.ventana.wait_window()
        # Una vez que la ventana se cierra, devolvemos el diccionario en 'self.coordenadas' y listo, tenemos los datos para el análisis
        return self.coordenadas

# Metemos todo nuestro código de análisis en una función que acepta el diccionario 'coordenadas' como argumento para traducir la GUI del código principal
def ejecutar_analisis_ruta(coordenadas):
    # Configuramos OSMnx para que muestre mensajes en la consola y use el caché para no descargar el mapa cada vez que corremos el script y tarde más
    ox.settings.log_console = True
    ox.settings.use_cache = True
    
    # Primero definimos la lista de lugares que queremos descargar y modelar
    lista_de_lugares = [
        "Oaxaca de Juárez, Oaxaca, Mexico",
        "Santa Cruz Xoxocotlán, Oaxaca, Mexico",
        "San Raymundo Jalpan, Oaxaca, Mexico",
        "San Antonio de la Cal, Oaxaca, Mexico",
        "San Agustín de las Juntas, Oaxaca, Mexico"
    ]
    
    print(f"Iniciando la descarga de {lista_de_lugares}")

    try:
        # Una vez definidos, usamos 'ox.graph_from_place' para descargar los mapas y datos de calles de OSM, con 'network_type="drive"' filtramos calles solo para autos
        # El grafo que devuelve está en coordenadas de tipo Latitud, Longitud
        grafo_original_latlon = ox.graph_from_place(lista_de_lugares, network_type='drive', simplify=True)
        print("Descarga completada exitosamente")
    except Exception as e:
        # Si falla la descarga se muestra el error y terminamos la función
        print(f"Error en la descarga del grafo: {e}")
        return # Salimos de la función y se termina el análisis

    # Proyectamos el grafo y lo convertimos de Latitud, Longitud a un sistema de coordenadas en Metros para que la longitud de las calles esté en metros
    grafo_proyectado_metros = ox.project_graph(grafo_original_latlon)
    # Ahora vamos a realizar el calculo de pesos (tiempo de viaje) para cada arista del grafo
    # Lo primero es definir nuestras constantes 
    VELOCIDAD_POR_DEFECTO_KMH = 20.0
    FACTOR_CONVERSION_MS = 3.6
    
    # Obtenemos una lista de todas las aristas o calles y sus datos
    aristas_del_grafo = list(grafo_proyectado_metros.edges(keys=True, data=True))
    
    # Creamos diccionarios vacíos para guardar los nuevos atributos de velocidad y tiempo
    diccionario_velocidades_kmh = {}
    diccionario_tiempos_segundos = {}

    # Iteramos sobre cada arista que obtuvimos y (nodo_u, nodo_v, clave_arista) es el ID único de la arista, luego usamos 'datos_arista' para obtener sus atributos
    for nodo_u, nodo_v, clave_arista, datos_arista in aristas_del_grafo:
        
        id_arista = (nodo_u, nodo_v, clave_arista)
        # Asumimos la velocidad por defecto al inicio de cada iteración
        velocidad_calle_kmh = VELOCIDAD_POR_DEFECTO_KMH
        
        # Revisamos si la arista tiene el atributo 'maxspeed', que indica la velocidad máxima permitida en esa calle
        if 'maxspeed' in datos_arista:
            dato_velocidad_maxima = datos_arista['maxspeed']
            # Hacemos un 'try except' porque este dato puede ser una lista ['40', '50'] o un string '60 km/h'
            try:
                if isinstance(dato_velocidad_maxima, list):
                    # Si es una lista, la limpiamos y sacamos el promedio de los valores numéricos que contenga
                    lista_valores_velocidad = [float(val.split()[0]) for val in dato_velocidad_maxima if val.split()[0].isdigit()]
                    if lista_valores_velocidad:
                        velocidad_calle_kmh = sum(lista_valores_velocidad) / len(lista_valores_velocidad)
                elif isinstance(dato_velocidad_maxima, str):
                    # Si es un string, extraemos solo el número al inicio del string
                    partes_velocidad = dato_velocidad_maxima.split()
                    if partes_velocidad[0].isdigit():
                        velocidad_calle_kmh = float(partes_velocidad[0])
            except Exception:
                # Si algo falla, no hacemos nada y se queda la velocidad por defecto para esa calle
                velocidad_calle_kmh = VELOCIDAD_POR_DEFECTO_KMH
        
        # Obtenemos la longitud en metros desde los datos de la arista
        longitud_calle_metros = datos_arista['length']
        # Convertimos la velocidad a metros/segundo para el cálculo del tiempo de viaje
        velocidad_calle_ms = velocidad_calle_kmh / FACTOR_CONVERSION_MS
        
        # Calculamos el tiempo en segundos (Tiempo = Distancia / Velocidad) y si la velocidad es 0, asignamos un tiempo "infinito"
        tiempo_viaje_segundos = longitud_calle_metros / velocidad_calle_ms if velocidad_calle_ms > 0 else float('inf')
        
        # Guardamos los nuevos valores en nuestros diccionarios y listos para asignarlos al grafo
        diccionario_velocidades_kmh[id_arista] = velocidad_calle_kmh
        diccionario_tiempos_segundos[id_arista] = tiempo_viaje_segundos

    # Ahora, asignamos todos los nuevos atributos al grafo de una sola vez usando 'nx.set_edge_attributes'
    nx.set_edge_attributes(grafo_proyectado_metros, diccionario_velocidades_kmh, 'velocidad_kmh')
    nx.set_edge_attributes(grafo_proyectado_metros, diccionario_tiempos_segundos, 'tiempo_viaje_segundos')

    # Ahora inicializamos la ruta como 'None' antes de calcularla con los datos del usuario
    ruta_optima_nodos = None
    try:
        # Obtenemos las coordenadas del diccionario que recibimos del usuario a través de la interfaz gráfica
        latitud_origen = coordenadas['lat_origen']
        longitud_origen = coordenadas['lon_origen']
        latitud_destino = coordenadas['lat_destino']
        longitud_destino = coordenadas['lon_destino']
        
        # Definimos una función rápida para encontrar el nodo más cercano con las coordenadas dadas
        def obtener_nodo_mas_cercano(grafo, lat, lon):
            # Usamos el grafo 'grafo_original_latlon' porque está en (Lat, Lon), igual que nuestras coordenadas y 'ox.nearest_nodes' espera las coordenadas en orden Longitud, Latitud
            return ox.nearest_nodes(grafo, X=lon, Y=lat)
        # Buscamos el nodo de inicio más cercano 
        nodo_origen = obtener_nodo_mas_cercano(grafo_original_latlon, latitud_origen, longitud_origen)
        # Buscamos el nodo de fin más cercano 
        nodo_destino = obtener_nodo_mas_cercano(grafo_original_latlon, latitud_destino, longitud_destino)

        # Le pedimos a 'networkx' que encuentre el camino más corto ('shortest_path') a través del grafo usando el algoritmo de Dijkstra
        # Usamos 'grafo_proyectado_metros' porque tiene los atributos en metros y "weight='tiempo_viaje_segundos'" le dice a Dijkstra que minimice la suma de este atributo, no la distancia
        ruta_optima_nodos = nx.shortest_path(
            grafo_proyectado_metros,
            source=nodo_origen,
            target=nodo_destino,
            weight='tiempo_viaje_segundos'
        )
        print("Mejor ruta calculada exitosamente")

    except nx.NetworkXNoPath:
        # Esto pasa si no hay un camino posible entre los nodos seleccionados
        print(f"ERRORZOTE no hay camino")
    except Exception as e:
        # Capturamos cualquier otro error
        print(f"Errorcito: {e}")

    # Verificamos si 'ruta_optima_nodos' se pudo calcular o no
    if ruta_optima_nodos:
        # Inicializamos nuestros contadores para distancia y tiempo
        distancia_total_metros = 0
        tiempo_total_segundos = 0
        
        # Iteramos sobre los pares de nodos (calles) de la ruta
        for nodo_u, nodo_v in zip(ruta_optima_nodos[:-1], ruta_optima_nodos[1:]):
            # Obtenemos las aristas paralelas entre estos dos nodos
            datos_multiples_aristas = grafo_proyectado_metros.get_edge_data(nodo_u, nodo_v)
            # Elegimos la arista que Dijkstra eligió que se basa en el menor tiempo de viaje
            arista_optima = min(datos_multiples_aristas.values(), key=lambda x: x['tiempo_viaje_segundos'])
            
            # Sumamos los valores de esa arista a nuestros contadores
            distancia_total_metros += arista_optima['length']
            tiempo_total_segundos += arista_optima['tiempo_viaje_segundos']

        # Convertimos las unidades para que sean legibles en el resumen final
        distancia_total_km = distancia_total_metros / 1000
        tiempo_total_minutos = tiempo_total_segundos / 60
        
        # Mostramos el resumen en la consola para el usuario
        print(f"Distancia Física Total: {distancia_total_km:.2f} km")
        print(f"Tiempo Estimado de Viaje: {tiempo_total_minutos:.2f} minutos")
        
        
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
            bgcolor='k',               
            figsize=(15, 15),
            show=False,                 
            close=False                 
        )
        
        # Añadimos un título simple al mapa para una mejor presentación
        eje.set_title(
            "Ruta Óptima de Oaxaca (Dijkstra por Tiempo)",
            fontsize=20,
            color='white' 
        )

        # Creamos el texto del resumen que vimos en la consola para ponerlo en el mapa y mostrarlo al usuario
        texto_resumen = (
            f"Distancia Física Total: {distancia_total_km:.2f} km\n"
            f"Tiempo Estimado de Viaje: {tiempo_total_minutos:.2f} min"
        )
        # Usamos eje.text() para poner texto sobre los ejes de el mapa y mostrar el resumen
        eje.text(
            0.03,                           
            0.97,                           
            texto_resumen,                  
            transform=eje.transAxes,        
            fontsize=14,
            color='black',                 
            verticalalignment='top',        
            bbox=dict(boxstyle='round,pad=0.5', 
                      fc='white',               
                      ec='cyan',                
                      lw=1,                     
                      alpha=0.8)                
        )

        print("Mostrando mapa. Cierra la ventana del mapa para terminar el programa")
        plt.show()

    else:
        # Esto se ejecuta si 'ruta_optima_nodos' sigue siendo 'None'
        print("\nNo se pudo calcular una ruta, checa los puntos ingresados")
    print("\nBYE BYE BYE")

# Esta condición especial '__name__ == "__main__"' se asegura de que este código solo se ejecute cuando corremos este archivo .py directamente.
if __name__ == "__main__":
    
    # Creamos la ventana "raíz" o principal de Tkinter que vizualizaremos
    ventana_raiz = tk.Tk()
    
    # Creamos una instancia de nuestra clase 'VentanaCoordenadas' y le pasamos la ventana raíz para que dibuje sobre ella
    aplicacion_gui = VentanaCoordenadas(ventana_raiz)
    
    # Llamamos al método que pausará el script y esperará a que el usuario interactúe con la ventana.
    # La variable 'coordenadas_ingresadas' recibirá el diccionario con los datos ingresados por el usuario.
    coordenadas_ingresadas = aplicacion_gui.obtener_coordenadas()
    
    # Verificamos si 'coordenadas_ingresadas' tiene datos o es 'None'
    if coordenadas_ingresadas:
        print("Coordenadas recibidas correctamente")
        print(coordenadas_ingresadas)
        #  Si todo es correcto, llamamos a nuestra función principal de análisis y le pasamos las coordenadas
        ejecutar_analisis_ruta(coordenadas_ingresadas)
    else:
        # Si 'coordenadas_ingresadas' es 'None'
        print("Operación Invalida")