# Chat Básico Cliente-Servidor con Sockets y Base de Datos

## 📋 Descripción

Este proyecto implementa un sistema de chat básico usando sockets TCP/IP en Python, donde múltiples clientes pueden conectarse a un servidor central que almacena todos los mensajes en una base de datos SQLite.

## 🚀 Características

- **Servidor multi-cliente**: Maneja múltiples conexiones simultáneas usando threading
- **Base de datos SQLite**: Almacena mensajes con timestamps e IP de origen
- **Manejo de errores robusto**: Gestiona puertos ocupados, errores de BD y desconexiones
- **Interfaz intuitiva**: Cliente con interfaz de consola fácil de usar
- **Código bien documentado**: Comentarios explicativos en cada sección clave

## 📁 Estructura del Proyecto

```
chat-cliente-servidor/
├── servidor.py          # Servidor de chat con sockets
├── cliente.py           # Cliente de chat
├── README.md           # Este archivo
└── chat_mensajes.db    # Base de datos SQLite (se crea automáticamente)
```

## 📊 Esquema de Base de Datos

La tabla `mensajes` contiene los siguientes campos:

| Campo       | Tipo     | Descripción                    |
|------------|----------|--------------------------------|
| id         | INTEGER  | ID único autoincremental       |
| contenido  | TEXT     | Contenido del mensaje          |
| fecha_envio| DATETIME | Timestamp del mensaje          |
| ip_cliente | TEXT     | Dirección IP del cliente       |

## 🔧 Requisitos

- Python 3.6 o superior
- Módulos estándar de Python (incluidos por defecto):
  - `socket`
  - `sqlite3`
  - `threading`
  - `datetime`

## ⚡ Instalación y Uso

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/Ailinci/PFO-redes-1
cd chat-cliente-servidor
```

### 2. Ejecutar el servidor

```bash
python servidor.py
```

**Salida esperada:**
```
==================================================
🚀 INICIANDO SERVIDOR DE CHAT
==================================================
✅ Base de datos 'chat_mensajes.db' inicializada correctamente
🌐 Socket inicializado correctamente en localhost:5000
🔊 Servidor escuchando en localhost:5000
⏳ Esperando conexiones de clientes...
📋 Presiona Ctrl+C para detener el servidor
```

### 3. Ejecutar el cliente (en otra terminal)

```bash
python cliente.py
```

**Salida esperada:**
```
🔄 Iniciando cliente de chat...
✅ Conectado exitosamente al servidor localhost:5000

==================================================
💬 CLIENTE DE CHAT INICIADO
==================================================
📝 Escribe tus mensajes (escribe 'salir' para terminar)
--------------------------------------------------
Tú: 
```

### 4. Enviar mensajes

1. Escribe un mensaje en el cliente y presiona Enter
2. El servidor recibirá el mensaje, lo guardará en la BD y enviará confirmación
3. El cliente mostrará la respuesta del servidor
4. Escribe `salir` para desconectar el cliente

## 🔨 Funcionalidades Implementadas

### Servidor (`servidor.py`)

- ✅ **Inicialización del socket**: Función `inicializar_socket()`
- ✅ **Aceptar conexiones**: Función `aceptar_conexiones()`
- ✅ **Guardar en BD**: Función `guardar_mensaje_bd()`
- ✅ **Manejo de errores**: Puerto ocupado, BD inaccesible
- ✅ **Respuesta al cliente**: Formato "Mensaje recibido: [contenido]"
- ✅ **Multi-cliente**: Usando threading para conexiones simultáneas

### Cliente (`cliente.py`)

- ✅ **Conexión al servidor**: Función `conectar_servidor()`
- ✅ **Envío múltiple de mensajes**: Loop interactivo
- ✅ **Condición de salida**: Escribir "salir"
- ✅ **Mostrar respuestas**: Cada respuesta del servidor se muestra
- ✅ **Manejo de errores**: Conexión perdida, servidor no disponible

## 🛠️ Manejo de Errores

El proyecto incluye manejo de errores para:

- **Puerto ocupado**: Detecta si el puerto 5000 está en uso
- **Base de datos inaccesible**: Maneja errores de SQLite
- **Conexiones perdidas**: Detecta desconexiones abruptas
- **Mensajes vacíos**: Valida entrada del usuario
- **Interrupciones del usuario**: Manejo de Ctrl+C

## 👨‍💻 Autor

**Ailín Ojeda Pytel**
- Email: [aipilinpi.ojeda@gmail.com]
**Entrega**: 7/9/2025