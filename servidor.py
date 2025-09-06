import socket
import sqlite3
import threading
from datetime import datetime
import sys
import os

# Configuración del servidor
HOST = 'localhost'
PORT = 5000
DATABASE_NAME = 'chat_mensajes.db'

def inicializar_base_datos():
    """
    Inicializa la base de datos SQLite y crea la tabla de mensajes si no existe.
    
    Returns:
        bool: True si la inicialización fue exitosa, False en caso contrario
    """
    try:
        # Conexión a la base de datos (se crea automáticamente si no existe)
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Crear tabla de mensajes con los campos requeridos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio DATETIME NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Base de datos '{DATABASE_NAME}' inicializada correctamente")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al inicializar la base de datos: {e}")
        return False

def guardar_mensaje_bd(contenido, ip_cliente):
    """
    Guarda un mensaje en la base de datos SQLite.
    
    Args:
        contenido (str): Contenido del mensaje a guardar
        ip_cliente (str): Dirección IP del cliente que envió el mensaje
    
    Returns:
        tuple: (True, fecha_envio) si el mensaje se guardó correctamente, (False, None) en caso contrario
    """
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Obtener fecha y hora actual
        fecha_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insertar el mensaje en la base de datos
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha_envio, ip_cliente))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Mensaje guardado en BD: '{contenido[:50]}...' en timestamp {fecha_envio}")
        return True, fecha_envio
        
    except sqlite3.Error as e:
        print(f"❌ Error al guardar mensaje en base de datos: {e}")
        return False, None
    except Exception as e:
        print(f"❌ Error inesperado al guardar mensaje: {e}")
        return False, None

def manejar_cliente(conn_cliente, direccion_cliente):
    """
    Maneja la comunicación con un cliente específico en un hilo separado.
    
    Args:
        conn_cliente: Socket de conexión con el cliente
        direccion_cliente: Tupla con (IP, puerto) del cliente
    """
    ip_cliente = direccion_cliente[0]
    print(f"🔗 Nuevo cliente conectado desde: {direccion_cliente}")
    
    try:
        while True:
            # Recibir mensaje del cliente
            mensaje = conn_cliente.recv(1024).decode('utf-8')
            
            # Si no hay mensaje, el cliente se desconectó
            if not mensaje:
                print(f"📤 Cliente {ip_cliente} se desconectó")
                break
            
            print(f"📨 Mensaje recibido de {ip_cliente}: {mensaje}")
            
            # Guardar mensaje en la base de datos
            guardado, fecha_envio = guardar_mensaje_bd(mensaje, ip_cliente)
            if guardado:
                # Enviar confirmación al cliente
                respuesta = f"Mensaje recibido: {fecha_envio}"
                conn_cliente.send(respuesta.encode('utf-8'))
            else:
                # Error al guardar, notificar al cliente
                respuesta = "Error: No se pudo guardar el mensaje en la base de datos"
                conn_cliente.send(respuesta.encode('utf-8'))
    
    except ConnectionResetError:
        print(f"🔌 Conexión con cliente {ip_cliente} perdida bruscamente")
    except Exception as e:
        print(f"❌ Error al manejar cliente {ip_cliente}: {e}")
    finally:
        # Cerrar conexión con el cliente
        conn_cliente.close()
        print(f"❌ Conexión cerrada con {ip_cliente}")

def inicializar_socket():
    """
    Inicializa y configura el socket del servidor.
    
    Returns:
        socket.socket: Socket configurado del servidor, None en caso de error
    """
    try:
        # Configuración del socket TCP/IP
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Permitir reutilizar la dirección (evitar error "Address already in use")
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Vincular socket al host y puerto especificados
        servidor_socket.bind((HOST, PORT))
        
        print(f"🌐 Socket inicializado correctamente en {HOST}:{PORT}")
        return servidor_socket
        
    except socket.error as e:
        if e.errno == 98:  # Puerto ocupado (Linux/Mac)
            print(f"❌ Error: El puerto {PORT} está ocupado. Cierra otras aplicaciones que lo usen.")
        elif e.errno == 10048:  # Puerto ocupado (Windows)
            print(f"❌ Error: El puerto {PORT} está ocupado. Cierra otras aplicaciones que lo usen.")
        else:
            print(f"❌ Error de socket: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado al inicializar socket: {e}")
        return None

def aceptar_conexiones(servidor_socket):
    """
    Acepta conexiones entrantes y maneja cada cliente en un hilo separado.
    
    Args:
        servidor_socket: Socket del servidor configurado
    """
    try:
        # Configurar el socket para escuchar conexiones (máximo 5 en cola)
        servidor_socket.listen(5)
        print(f"🔊 Servidor escuchando en {HOST}:{PORT}")
        print("⏳ Esperando conexiones de clientes...")
        print("📋 Presiona Ctrl+C para detener el servidor")
        
        while True:
            try:
                # Aceptar nueva conexión de cliente
                conn_cliente, direccion_cliente = servidor_socket.accept()
                
                # Crear hilo para manejar el cliente (permitir múltiples clientes)
                hilo_cliente = threading.Thread(
                    target=manejar_cliente,
                    args=(conn_cliente, direccion_cliente)
                )
                hilo_cliente.daemon = True  # Hilo demonio (se cierra con el programa principal)
                hilo_cliente.start()
                
            except socket.error as e:
                print(f"❌ Error al aceptar conexión: {e}")
                continue
                
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
    except Exception as e:
        print(f"❌ Error inesperado en el bucle principal: {e}")
    finally:
        servidor_socket.close()
        print("✅ Servidor cerrado correctamente")

def main():
    """
    Función principal del servidor.
    """
    print("=" * 50)
    print("🚀 INICIANDO SERVIDOR DE CHAT")
    print("=" * 50)
    
    # 1. Inicializar base de datos
    if not inicializar_base_datos():
        print("❌ No se puede continuar sin base de datos. Saliendo...")
        sys.exit(1)
    
    # 2. Inicializar socket del servidor
    servidor_socket = inicializar_socket()
    if servidor_socket is None:
        print("❌ No se puede continuar sin socket. Saliendo...")
        sys.exit(1)
    
    # 3. Comenzar a aceptar conexiones
    try:
        aceptar_conexiones(servidor_socket)
    except Exception as e:
        print(f"❌ Error fatal en el servidor: {e}")
    finally:
        if servidor_socket:
            servidor_socket.close()

if __name__ == "__main__":
    main()