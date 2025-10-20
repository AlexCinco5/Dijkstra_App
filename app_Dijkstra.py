# -----------------------------------------------------------------
# Proyecto: Aplicación de Dijkstra en Red Vial (App.Dijkstra)
# Autor: Gemini (asistiendo a Alejandro Cinco)
# Fecha: 19 de octubre de 2025
# 
# Descripción:
# Este script lanza una ventana (GUI) para pedir coordenadas y luego
# calcula la ruta óptima (basada en tiempo) usando OSMnx y Dijkstra.
# Todas las variables están en español.
# -----------------------------------------------------------------

# --- PASO 0: IMPORTACIÓN DE LIBRERÍAS ---

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Importaciones para la ventana (GUI)
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Usaremos un 'LabelFrame' estilizado

# -----------------------------------------------------------------
# --- CLASE PARA MANEJAR LA VENTANA DE ENTRADA (GUI) ---
# -----------------------------------------------------------------
class VentanaCoordenadas:
    """
    Esta clase crea y maneja la ventana inicial para pedir
    las coordenadas de origen y destino al usuario.
    """
    def __init__(self, ventana_raiz):
        # Configuración de la ventana principal
        self.ventana = ventana_raiz
        self.ventana.title("Calculadora de Ruta Óptima (Dijkstra)")
        
        # Variable para almacenar los datos de salida
        self.coordenadas = None
        
        # --- Creación de Widgets (Etiquetas, Cajas de Texto, Botón) ---
        
        # --- Origen ---
        tk.Label(ventana_raiz, text="Punto de Origen", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        tk.Label(ventana_raiz, text="Latitud:").grid(row=1, column=0, padx=5, sticky="e")
        self.caja_lat_origen = tk.Entry(ventana_raiz, width=25)
        self.caja_lat_origen.grid(row=1, column=1, padx=10, pady=2)
        
        tk.Label(ventana_raiz, text="Longitud:").grid(row=2, column=0, padx=5, sticky="e")
        self.caja_lon_origen = tk.Entry(ventana_raiz, width=25)
        self.caja_lon_origen.grid(row=2, column=1, padx=10, pady=2)
        
        # --- Destino ---
        tk.Label(ventana_raiz, text="Punto de Destino", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=(10, 5))
        
        tk.Label(ventana_raiz, text="Latitud:").grid(row=4, column=0, padx=5, sticky="e")
        self.caja_lat_destino = tk.Entry(ventana_raiz, width=25)
        self.caja_lat_destino.grid(row=4, column=1, padx=10, pady=2)
        
        tk.Label(ventana_raiz, text="Longitud:").grid(row=5, column=0, padx=5, sticky="e")
        self.caja_lon_destino = tk.Entry(ventana_raiz, width=25)
        self.caja_lon_destino.grid(row=5, column=1, padx=10, pady=2)

        # --- RECUADRO DE RECOMENDACIONES ---
        marco_recomendaciones = ttk.LabelFrame(ventana_raiz, text=" Puntos de Interés (Copiar y Pegar) ")
        marco_recomendaciones.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Usamos 'readonly' para permitir copiar pero no editar
        def crear_caja_recomendacion(etiqueta, valor_lat, valor_lon):
            tk.Label(marco_recomendaciones, text=etiqueta, font=("Arial", 9, "bold")).pack(fill="x", padx=5, pady=(5,0))
            
            frame_coords = tk.Frame(marco_recomendaciones)
            frame_coords.pack(fill="x", padx=5)
            
            tk.Label(frame_coords, text="Lat:").pack(side="left")
            caja_lat = tk.Entry(frame_coords, width=15)
            caja_lat.insert(0, valor_lat)
            caja_lat.config(state="readonly")
            caja_lat.pack(side="left", fill="x", expand=True, padx=(2, 5))
            
            tk.Label(frame_coords, text="Lon:").pack(side="left")
            caja_lon = tk.Entry(frame_coords, width=15)
            caja_lon.insert(0, valor_lon)
            caja_lon.config(state="readonly")
            caja_lon.pack(side="left", fill="x", expand=True, padx=(2, 0))

        crear_caja_recomendacion("📍 Santo Domingo:", "17.0654", "-96.7219")
        crear_caja_recomendacion("✈️ Aeropuerto XOX:", "16.9993", "-96.7266")
        crear_caja_recomendacion("🎓 Anáhuac Oaxaca:", "16.9971", "-96.7561") # Coordenadas del CRIT, que está al lado.

        # --- Botón de Enviar ---
        self.boton_enviar = tk.Button(ventana_raiz, text="Calcular Ruta", font=("Arial", 10, "bold"), command=self.enviar_datos)
        self.boton_enviar.grid(row=7, column=0, columnspan=2, pady=10) # Fila actualizada

    def enviar_datos(self):
        """
        Se ejecuta al presionar el botón.
        Valida que los datos sean números y los guarda.
        """
        try:
            # Intentamos convertir todas las entradas a números (float)
            latitud_origen = float(self.caja_lat_origen.get())
            longitud_origen = float(self.caja_lon_origen.get())
            latitud_destino = float(self.caja_lat_destino.get())
            longitud_destino = float(self.caja_lon_destino.get())
            
            # Si tiene éxito, guardamos los datos en un diccionario
            self.coordenadas = {
                'lat_origen': latitud_origen,
                'lon_origen': longitud_origen,
                'lat_destino': latitud_destino,
                'lon_destino': longitud_destino
            }
            
            # Cerramos la ventana para que el script principal continúe
            self.ventana.destroy()
            
        except ValueError:
            # Si falla la conversión a float, mostramos un error
            messagebox.showerror("Error de Entrada", "Por favor, introduce solo números válidos (ej. 17.0654 o -96.7219)")

    def obtener_coordenadas(self):
        """
        Esta función detiene el script principal hasta que
        la ventana se cierre (con el botón o la 'X').
        """
        self.ventana.wait_window()
        return self.coordenadas

# -----------------------------------------------------------------
# --- FUNCIÓN PRINCIPAL DE ANÁLISIS DE RUTA ---
# -----------------------------------------------------------------
def ejecutar_analisis_ruta(coordenadas):
    """
    Esta función contiene todo el proceso de descarga, cálculo
    y visualización de la ruta. Se ejecuta DESPUÉS de
    obtener las coordenadas de la ventana GUI.
    """
    
    # Configuramos OSMnx
    ox.settings.log_console = True
    ox.settings.use_cache = True
    
    # --- PASO 1: DESCARGA Y MODELADO DEL MAPA ---
    lista_de_lugares = [
        "Oaxaca de Juárez, Oaxaca, Mexico",
        "Santa Cruz Xoxocotlán, Oaxaca, Mexico",
        "San Raymundo Jalpan, Oaxaca, Mexico"
    ]
    
    print(f"Iniciando la descarga de la red vial para: {lista_de_lugares}")
    print("... esto puede tardar varios minutos la primera vez ...")

    try:
        # Grafo con coordenadas geográficas (Latitud, Longitud)
        grafo_original_latlon = ox.graph_from_place(lista_de_lugares, network_type='drive', simplify=True)
        print("¡Grafo en Latitud/Longitud descargado exitosamente!")
    except Exception as e:
        print(f"Error crítico al descargar el grafo: {e}")
        return # Detenemos la ejecución si no hay mapa

    # Grafo proyectado a un sistema métrico (UTM)
    grafo_proyectado_metros = ox.project_graph(grafo_original_latlon)
    print("¡Grafo proyectado a metros (UTM) exitosamente!")

    # --- PASO 2: CÁLCULO DE PESOS (TIEMPO DE VIAJE) ---
    print("Iniciando cálculo de pesos (tiempo de viaje)...")
    VELOCIDAD_POR_DEFECTO_KMH = 20.0
    FACTOR_CONVERSION_MS = 3.6
    
    aristas_del_grafo = list(grafo_proyectado_metros.edges(keys=True, data=True))
    
    # Diccionarios para almacenar los nuevos atributos
    diccionario_velocidades_kmh = {}
    diccionario_tiempos_segundos = {}

    for nodo_u, nodo_v, clave_arista, datos_arista in aristas_del_grafo:
        
        id_arista = (nodo_u, nodo_v, clave_arista)
        velocidad_calle_kmh = VELOCIDAD_POR_DEFECTO_KMH
        
        if 'maxspeed' in datos_arista:
            dato_velocidad_maxima = datos_arista['maxspeed']
            try:
                if isinstance(dato_velocidad_maxima, list):
                    lista_valores_velocidad = [float(val.split()[0]) for val in dato_velocidad_maxima if val.split()[0].isdigit()]
                    if lista_valores_velocidad:
                        velocidad_calle_kmh = sum(lista_valores_velocidad) / len(lista_valores_velocidad)
                elif isinstance(dato_velocidad_maxima, str):
                    partes_velocidad = dato_velocidad_maxima.split()
                    if partes_velocidad[0].isdigit():
                        velocidad_calle_kmh = float(partes_velocidad[0])
            except Exception:
                velocidad_calle_kmh = VELOCIDAD_POR_DEFECTO_KMH
        
        longitud_calle_metros = datos_arista['length']
        velocidad_calle_ms = velocidad_calle_kmh / FACTOR_CONVERSION_MS
        
        tiempo_viaje_segundos = longitud_calle_metros / velocidad_calle_ms if velocidad_calle_ms > 0 else float('inf')
        
        diccionario_velocidades_kmh[id_arista] = velocidad_calle_kmh
        diccionario_tiempos_segundos[id_arista] = tiempo_viaje_segundos

    nx.set_edge_attributes(grafo_proyectado_metros, diccionario_velocidades_kmh, 'velocidad_kmh')
    nx.set_edge_attributes(grafo_proyectado_metros, diccionario_tiempos_segundos, 'tiempo_viaje_segundos')
    print("¡Pesos (tiempo_viaje_segundos) calculados!")

    # --- PASO 3: SELECCIÓN DE PUNTOS Y CÁLCULO DE RUTA ---
    
    ruta_optima_nodos = None
    try:
        # Obtenemos las coordenadas del diccionario que nos pasó la GUI
        latitud_origen = coordenadas['lat_origen']
        longitud_origen = coordenadas['lon_origen']
        latitud_destino = coordenadas['lat_destino']
        longitud_destino = coordenadas['lon_destino']
        
        print("Buscando nodos (intersecciones) más cercanos...")
        
        def obtener_nodo_mas_cercano(grafo, lat, lon):
            # Usamos el grafo original (lat/lon) para buscar nodos cercanos
            return ox.nearest_nodes(grafo, X=lon, Y=lat)

        nodo_origen = obtener_nodo_mas_cercano(grafo_original_latlon, latitud_origen, longitud_origen)
        nodo_destino = obtener_nodo_mas_cercano(grafo_original_latlon, latitud_destino, longitud_destino)
        
        print(f"-> Nodo de Origen (ID): {nodo_origen}")
        print(f"-> Nodo de Destino (ID): {nodo_destino}")

        print("\nCalculando la ruta óptima usando Dijkstra...")
        ruta_optima_nodos = nx.shortest_path(
            grafo_proyectado_metros,
            source=nodo_origen,
            target=nodo_destino,
            weight='tiempo_viaje_segundos'
        )
        print("¡Ruta óptima (basada en tiempo) encontrada!")

    except nx.NetworkXNoPath:
        print(f"ERROR: No se encontró una ruta transitable entre los nodos seleccionados.")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado durante el cálculo de ruta: {e}")

    # --- PASO 4: VISUALIZACIÓN Y RESUMEN DE RESULTADOS ---

    if ruta_optima_nodos:
        
        # 1. --- Calcular Resumen del Recorrido (Método Manual) ---
        distancia_total_metros = 0
        tiempo_total_segundos = 0
        
        for nodo_u, nodo_v in zip(ruta_optima_nodos[:-1], ruta_optima_nodos[1:]):
            # Obtenemos las aristas paralelas (si existen)
            datos_multiples_aristas = grafo_proyectado_metros.get_edge_data(nodo_u, nodo_v)
            # Elegimos la arista que Dijkstra eligió (la de menor tiempo)
            arista_optima = min(datos_multiples_aristas.values(), key=lambda x: x['tiempo_viaje_segundos'])
            
            distancia_total_metros += arista_optima['length']
            tiempo_total_segundos += arista_optima['tiempo_viaje_segundos']

        distancia_total_km = distancia_total_metros / 1000
        tiempo_total_minutos = tiempo_total_segundos / 60
        
        print("\n--- RESUMEN DE LA RUTA ÓPTIMA (basada en TIEMPO) ---")
        print(f"Distancia Física Total: {distancia_total_km:.2f} km")
        print(f"Tiempo Estimado de Viaje: {tiempo_total_minutos:.2f} minutos")
        
        # 3. --- Descargar Geometrías de Áreas Verdes ---
        print("Descargando geometrías de áreas verdes (parques, etc.)...")
        try:
            etiquetas_osm = {'leisure': ['park', 'garden', 'recreation_ground'],
                             'landuse': ['grass', 'forest', 'meadow'],
                             'natural': ['wood', 'scrub']}
            geometrias_verdes = ox.features.features_from_place(lista_de_lugares, tags=etiquetas_osm)
            sistema_coordenadas_grafo = grafo_proyectado_metros.graph['crs']
            geometrias_verdes_proyectadas = geometrias_verdes.to_crs(sistema_coordenadas_grafo)
            print("Áreas verdes descargadas y proyectadas.")
        except Exception as e:
            print(f"No se pudieron descargar o procesar las áreas verdes: {e}")
            geometrias_verdes_proyectadas = None

        # 4. --- Generar Visualización del Mapa ---
        print("Generando el mapa de la ruta...")
        
        figura, eje = plt.subplots(figsize=(15, 15), facecolor='white')

        if geometrias_verdes_proyectadas is not None and not geometrias_verdes_proyectadas.empty:
            geometrias_verdes_proyectadas.plot(ax=eje, fc='#8BC34A', ec='none', alpha=0.5)

        figura, eje = ox.plot_graph_route(
            grafo_proyectado_metros, ruta_optima_nodos,
            route_color='cyan', route_linewidth=3, route_alpha=0.8,
            orig_dest_size=100, ax=eje, node_size=0,
            edge_linewidth=0.5, edge_color='#6D4C41', # Calles color café
            bgcolor='none', show=False, close=False
        )
        
        eje.set_title(f"Ruta Óptima de Oaxaca (Dijkstra por Tiempo)", fontsize=20, color='black')

        texto_resumen = (
            f"Distancia Total: {distancia_total_km:.2f} km\n"
            f"Tiempo Estimado: {tiempo_total_minutos:.2f} min"
        )
        eje.text(0.03, 0.97, texto_resumen, transform=eje.transAxes,
                 fontsize=14, color='black', verticalalignment='top',
                 bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))

        print("Mostrando mapa. Cierra la ventana del mapa para terminar el script.")
        plt.show()

    else:
        print("\nNo se pudo calcular una ruta.")
        # Mostramos el error también en una ventana emergente
        messagebox.showinfo("Resultado", "No se pudo encontrar una ruta transitable con los puntos seleccionados.")

    print("\n--- Fin del programa ---")

# -----------------------------------------------------------------
# --- BLOQUE DE EJECUCIÓN PRINCIPAL ---
# -----------------------------------------------------------------
if __name__ == "__main__":
    # 1. Creamos la ventana raíz de Tkinter
    ventana_raiz = tk.Tk()
    
    # 2. Creamos una instancia de nuestra aplicación de ventana
    aplicacion_gui = VentanaCoordenadas(ventana_raiz)
    
    # 3. Llamamos a la función que detiene el script
    #    y espera a que la ventana se cierre (inicia el mainloop).
    coordenadas_ingresadas = aplicacion_gui.obtener_coordenadas()
    
    # 4. Verificamos si obtuvimos coordenadas
    if coordenadas_ingresadas:
        print("Coordenadas recibidas, iniciando análisis...")
        print(coordenadas_ingresadas)
        # 5. ¡Llamamos a nuestra función principal con los datos!
        ejecutar_analisis_ruta(coordenadas_ingresadas)
    else:
        print("Operación cancelada por el usuario.")