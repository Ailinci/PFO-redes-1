"""
Cliente de Chat con Sockets
Autor: Ailín Ojeda Pytel
Fecha: 9/2025
"""

import socket
import sys

# Configuración del cliente
HOST = 'localhost'
PORT = 5000

def conectar_servidor():
    """
    Establece conexión con el servidor de chat.
    
    Returns:
        socket.socket: Socket conectado al servidor, None en caso de error
    """
    try:
        # Crear socket TCP/IP para el cliente
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conectar al servidor
        cliente_socket.connect((HOST, PORT))
        
        print(f"✅ Conectado exitosamente al servidor {HOST}:{PORT}")
        return cliente_socket
        
    except ConnectionRefusedError:
        print(f"❌ Error: No se puede conectar al servidor en {HOST}:{PORT}")
        print("   Asegúrate de que el servidor esté ejecutándose.")
        return None
    except socket.gaierror:
        print(f"❌ Error: No se puede resolver la dirección {HOST}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado al conectar: {e}")
        return None

def enviar_mensajes(cliente_socket):
    """
    Maneja el envío de mensajes al servidor en un bucle interactivo.
    
    Args:
        cliente_socket: Socket conectado al servidor
    """
    print("\n" + "=" * 50)
    print("💬 CLIENTE DE CHAT INICIADO")
    print("=" * 50)
    print("📝 Escribe tus mensajes (escribe 'exito' para terminar)")
    print("-" * 50)
    
    try:
        while True:
            # Solicitar mensaje al usuario
            mensaje = input("Tú: ").strip()
            
            # Verificar si el usuario quiere salir
            if mensaje.lower() == 'exito':
                print("👋 Desconectando del servidor...")
                break
            
            # Verificar que el mensaje no esté vacío
            if not mensaje:
                print("⚠️  El mensaje no puede estar vacío")
                continue
            
            try:
                # Enviar mensaje al servidor
                cliente_socket.send(mensaje.encode('utf-8'))
                
                # Recibir respuesta del servidor
                respuesta = cliente_socket.recv(1024).decode('utf-8')
                
                # Mostrar respuesta del servidor
                print(f"Servidor: {respuesta}")
                print("-" * 50)
                
            except ConnectionResetError:
                print("❌ Error: El servidor cerró la conexión inesperadamente")
                break
            except socket.error as e:
                print(f"❌ Error de comunicación: {e}")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Interrupción del usuario. Desconectando...")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """
    Función principal del cliente.
    """
    print("🔄 Iniciando cliente de chat...")
    
    # Conectar al servidor
    cliente_socket = conectar_servidor()
    
    if cliente_socket is None:
        print("❌ No se puede continuar sin conexión al servidor. Saliendo...")
        sys.exit(1)
    
    try:
        # Comenzar sesión de chat
        enviar_mensajes(cliente_socket)
    except Exception as e:
        print(f"❌ Error fatal en el cliente: {e}")
    finally:
        # Cerrar conexión
        if cliente_socket:
            cliente_socket.close()
            print("✅ Conexión cerrada correctamente")

if __name__ == "__main__":
    main()