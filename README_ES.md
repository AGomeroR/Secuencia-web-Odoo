# 🎯 Optimizador de Secuencias de Sitio Web para Odoo

Optimiza automáticamente el orden de visualización de productos en tu tienda eCommerce de Odoo basándose en la completitud de información y el rendimiento de ventas.

Esta utilidad Python analiza todos los productos en tu instancia de Odoo y asigna inteligentemente valores de `website_sequence`, priorizando productos que están activos, publicados, tienen información completa de eCommerce (categorías, imágenes, descripciones) y demuestran un buen rendimiento de ventas.

**Estado**: Listo para Producción | **Python**: 3.7+ | **Versión**: 1.0.0

---

## Tabla de Contenidos

- [Características Principales](#características-principales)
- [¿Por qué Usar Esta Herramienta?](#por-qué-usar-esta-herramienta)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Cómo Funciona](#cómo-funciona)
- [Salidas y Reportes](#salidas-y-reportes)
- [Solución de Problemas](#solución-de-problemas)
- [Autor](#autor)

---

## Características Principales

- ✅ **Sistema de Priorización Inteligente en 4 Niveles**: Organiza productos por estado (Activo+Publicado, Solo Activo, Solo Publicado, Inactivo)
- ✅ **Criterios de Preparación eCommerce**: Evalúa categorías públicas, imágenes de productos y descripciones del sitio web
- ✅ **Desempate por Rendimiento de Ventas**: Usa datos de ventas reales para priorizar productos dentro del mismo nivel
- ✅ **Modo de Prueba (Dry-Run)**: Previsualiza todos los cambios sin aplicarlos a tu instancia de Odoo
- ✅ **Actualizaciones en Dos Fases**: Mecanismo seguro que evita conflictos de números de secuencia duplicados
- ✅ **Registro Completo**: Logging detallado en archivo y reportes JSON con marca de tiempo
- ✅ **Procesamiento por Lotes**: Maneja eficientemente bases de datos grandes con miles de productos
- ✅ **Indicadores de Progreso**: Retroalimentación en tiempo real con emojis y estadísticas detalladas

---

## ¿Por qué Usar Esta Herramienta?

### El Problema
Muchas instancias de Odoo tienen productos ordenados aleatoriamente o por ID, lo que significa que productos incompletos o inactivos pueden aparecer antes que productos listos para la venta con información completa.

### La Solución
Este optimizador asegura que tus mejores productos - aquellos que están activos, publicados, tienen imágenes atractivas, descripciones completas, categorías apropiadas y buen historial de ventas - aparezcan primero en tu sitio web.

### Beneficios
- 📈 **Mayor Tasa de Clics**: Productos de alta calidad aparecen primero
- 🎯 **Mejor SEO**: Orden consistente y basado en calidad
- ⚡ **Manejo Automático**: Optimiza TODOS los productos, no solo los publicados
- 📊 **Decisiones Basadas en Datos**: Usa métricas reales de ventas para priorizar

---

## Requisitos Previos

### Requisitos del Sistema
- **Python 3.7 o superior** instalado en tu sistema
- **pip** (gestor de paquetes de Python)
- Acceso para crear y editar archivo `.env`

### Requisitos de Instancia Odoo
- **Odoo v14+** (o cualquier versión compatible con API XML-RPC)
- **Cuenta de usuario** con permisos de escritura en `product.template`
- **Autenticación con API Key** habilitada y generada
- Acceso a los siguientes campos de producto:
  - `website_sequence` (campo a optimizar)
  - `website_published` (estado de publicación)
  - `active` (estado activo/inactivo)
  - `public_categ_ids` (categorías de eCommerce)
  - `image_1920` (imagen del producto)
  - `website_description` (descripción del sitio web)
  - `sales_count` (contador de ventas)

### Requisitos de Red
- Acceso HTTPS saliente a tu instancia de Odoo
- Conexión a internet estable (especialmente para bases de datos grandes)

---

## Instalación

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si usas git
git clone <url-del-repositorio>
cd "Secuencia sitio web"

# O descarga manualmente y extrae los archivos
```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Verificar Instalación

```bash
python website_sequence_optimizer.py --help
```

Deberías ver el mensaje de ayuda con las opciones disponibles.

---

## Configuración

### Generar API Key de Odoo

1. Inicia sesión en tu instancia de Odoo como administrador
2. Navega a **Configuración > Usuarios y Compañías > Usuarios**
3. Selecciona tu cuenta de usuario
4. Desplázate a la sección **"Tokens de Acceso"** o **"Access Tokens"**
5. Haz clic en **"Nuevo Token"** o **"New Token"**
6. Ingresa una descripción (ej: "Optimizador de Secuencias")
7. **Copia el valor del token** (solo se muestra una vez)

### Crear Archivo .env

Crea un archivo llamado `.env` en el directorio del proyecto con el siguiente contenido:

```env
ODOO_URL=https://tu-instancia.odoo.com
ODOO_DB=nombre_base_datos
ODOO_USER=tu_usuario
ODOO_API_KEY=tu_api_key
```

**Reemplaza los valores**:
- `ODOO_URL`: URL completa de tu instancia Odoo (incluye `https://`)
- `ODOO_DB`: Nombre exacto de tu base de datos
- `ODOO_USER`: Tu nombre de usuario o correo electrónico
- `ODOO_API_KEY`: El token que generaste en el paso anterior

### Notas Importantes de Seguridad

- ⚠️ **NUNCA** comprometas el archivo `.env` en control de versiones (Git)
- ⚠️ Mantén tu API Key segura - regénera si se expone
- ⚠️ Verifica que el formato de URL incluya el protocolo (`https://`)
- ✅ El archivo `.gitignore` ya está configurado para proteger `.env`

---

## Uso

### Uso Básico

```bash
python website_sequence_optimizer.py
```

Esto ejecutará la optimización completa y aplicará los cambios a tu instancia de Odoo.

### Modo de Prueba (Dry-Run)

```bash
python website_sequence_optimizer.py --dry-run
```

Previsualiza todos los cambios sin aplicarlos. **Siempre recomendado para la primera ejecución.**

### Modo Detallado (Verbose)

```bash
python website_sequence_optimizer.py --verbose
```

Muestra logging extendido con métricas detalladas de preparación eCommerce.

### Combinación Recomendada (Primera Ejecución)

```bash
python website_sequence_optimizer.py --dry-run --verbose
```

Esto te permite ver exactamente qué cambios se harán antes de aplicarlos.

### Opciones de Línea de Comandos

| Opción | Forma Corta | Descripción |
|--------|-------------|-------------|
| `--dry-run` | - | Previsualizar cambios sin aplicarlos a Odoo |
| `--verbose` | `-v` | Habilitar logging detallado con métricas de eCommerce |

### Flujo de Trabajo Recomendado

```bash
# 1. Primera vez: previsualizar con verbose
python website_sequence_optimizer.py --dry-run --verbose

# 2. Revisar la salida y el reporte JSON generado

# 3. Si todo se ve bien, ejecutar para aplicar cambios
python website_sequence_optimizer.py --verbose

# 4. Verificar algunos productos en Odoo para confirmar
```

---

## Cómo Funciona

### Flujo de Procesamiento

```
1. Conectar a Odoo con autenticación API Key
   ↓
2. Obtener TODOS los productos (activos e inactivos) con paginación
   ↓
3. Calcular puntuación de prioridad para cada producto
   ↓
4. Ordenar productos por puntuación (mayor a menor)
   ↓
5. Asignar secuencias incrementales (1, 2, 3, ...)
   ↓
6. Aplicar actualizaciones en dos fases para evitar conflictos
   ↓
7. Generar reporte JSON y actualizar archivo de log
```

### Algoritmo de Puntuación de Prioridad

El optimizador calcula una puntuación para cada producto basándose en múltiples criterios:

#### Puntuación Base (por Estado)

| Estado | Puntuación Base | Prioridad | Icono |
|--------|----------------|-----------|-------|
| **Activo + Publicado** | 10,000,000 | Máxima (1º) | 🟢 |
| **Solo Activo** | 1,000,000 | 2º | 🟡 |
| **Solo Publicado** | 100,000 | 3º | 🔵 |
| **Inactivo + No Publicado** | 0 | Mínima (4º) | ⚪ |

#### Bonificaciones de Preparación eCommerce

Para productos activos o publicados, se agregan puntos adicionales:

- ✅ **Tiene categorías públicas** (`public_categ_ids`): **+100,000 puntos**
- ✅ **Tiene imagen** (`image_1920`): **+10,000 puntos**
- ✅ **Tiene descripción web** (`website_description`): **+1,000 puntos**

#### Desempate por Rendimiento de Ventas

Para productos activos, se agrega el contador de ventas directamente:

- 📊 **Ventas**: **+1 punto por unidad vendida**
- Usa el campo `sales_count` para desempatar dentro del mismo nivel de prioridad

### Ejemplo de Cálculo

```
Producto A: Activo + Publicado + Categorías + Imagen + Descripción + 50 ventas
Puntuación = 10,000,000 + 100,000 + 10,000 + 1,000 + 50 = 10,111,050
→ website_sequence = 1 (primera posición)

Producto B: Activo + Publicado + Categorías + Imagen + 20 ventas
Puntuación = 10,000,000 + 100,000 + 10,000 + 20 = 10,110,020
→ website_sequence = 2 (segunda posición)

Producto C: Solo Activo + Categorías + 100 ventas
Puntuación = 1,000,000 + 100,000 + 100 = 1,100,100
→ website_sequence = 3 (tercera posición)

Producto D: Inactivo + No publicado
Puntuación = 0
→ website_sequence = [último] (menor prioridad)
```

### ¿Por qué Actualizaciones en Dos Fases?

Para evitar conflictos de secuencias duplicadas durante la actualización masiva:

- **Fase 1**: Mueve todos los productos a secuencias temporales altas (ej: 50000+)
- **Fase 2**: Establece las secuencias finales optimizadas (1, 2, 3, ...)

Este enfoque previene errores de restricción de unicidad y asegura actualizaciones limpias.

---

## Salidas y Reportes

### Archivo de Log

**Nombre**: `website_sequence_optimization.log`

- Contiene entradas con marca de tiempo de todas las operaciones
- **Modo append-only**: Se preservan ejecuciones anteriores
- Útil para auditoría y depuración
- Incluye: conexión, obtención de datos, cálculos, actualizaciones, errores

**Ejemplo de Entradas de Log**:
```
[2025-11-26 14:30:45] INFO: 🚀 Starting website sequence optimization...
[2025-11-26 14:30:46] INFO: 🔗 Connecting to Odoo...
[2025-11-26 14:30:47] INFO: ✅ Connected successfully to Odoo as user ID: 2
[2025-11-26 14:30:47] INFO: ✅ Server version: 16.0
[2025-11-26 14:30:48] INFO: 📋 Fetching ALL products (active and inactive)...
[2025-11-26 14:30:50] INFO: 📊 Total products in database: 31,312
```

### Reporte JSON

**Nombre**: `website_sequence_report_YYYYMMDD_HHMMSS.json`

Contiene resultados detallados de optimización con los siguientes campos:

- `timestamp`: Fecha y hora ISO de la ejecución
- `total_products_analyzed`: Cantidad total de productos procesados
- `dry_run`: Booleano indicando si fue una ejecución de prueba
- `updates`: Array con todos los cambios de secuencia por producto
  - Para cada producto: `id`, `name`, `current_sequence`, `new_sequence`, `criteria_met`, `score`, `active`, `published`
- `log`: Registro completo de la ejecución

### Salida de Consola

Durante la ejecución verás:

- **Indicadores de progreso** con emojis en tiempo real
- **Estadísticas de resumen**:
  - Total de productos en la base de datos
  - Desglose por estado (Activo+Publicado, Solo Activo, Solo Publicado, Inactivo)
  - Productos con categorías, imágenes, descripciones
  - Total de productos a actualizar
  - Productos con cambios de secuencia
- **Vista previa de productos** (en modo verbose):
  - Top 10 productos de mayor prioridad
  - Cambios de secuencia (antes → después)
  - Criterios cumplidos (X/3)
  - Indicadores de estado con emojis
- **Advertencias o errores** encontrados durante el procesamiento

---

## Solución de Problemas

### Problemas Comunes

#### 1. "Missing environment variables: ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY"

**Causa**: Archivo `.env` no encontrado o incompleto

**Solución**:
- Verifica que el archivo `.env` existe en el directorio del proyecto
- Asegúrate de que contiene las 4 variables requeridas
- Verifica que no hay espacios alrededor del signo `=`
- El archivo debe llamarse exactamente `.env` (no `.env.txt`)

#### 2. "Authentication failed. Check your API key and credentials."

**Causa**: API key inválida, nombre de usuario o base de datos incorrectos

**Solución**:
- Regenera tu API key en Odoo (Configuración > Usuarios > tu usuario > Tokens de Acceso)
- Verifica que el nombre de usuario/email es correcto
- Confirma que el nombre de la base de datos es exacto (sensible a mayúsculas)
- Asegúrate de que la URL incluye `https://` y el dominio correcto
- **Nota**: La autenticación con contraseña NO es compatible; debes usar API Key

#### 3. "User does not have write permissions on product.template"

**Causa**: La cuenta de usuario de Odoo carece de acceso de escritura a productos

**Solución**:
- Pide al administrador de Odoo que otorgue el rol "Product Manager" o superior a tu usuario
- O crea un usuario dedicado con permisos completos de administración
- Verifica que el usuario no está restringido a compañías/almacenes específicos

#### 4. El Script se Cuelga o Expira (Timeout)

**Causa**: Gran conjunto de datos de productos o conexión de red lenta

**Solución**:
- El script maneja lotes de 500 productos automáticamente
- Para bases de datos grandes (10,000+ productos), la ejecución puede tomar 10-30 minutos
- Verifica la velocidad de tu conexión a internet
- Incluye un retraso de 0.5 segundos entre lotes por diseño (gentil con el servidor)
- Si persiste, considera ejecutar durante horas de menor tráfico

#### 5. "Phase 1 failed for product X: ..."

**Causa**: Actualización de secuencia temporal falló para un producto específico

**Solución**:
- Verifica el estado del servidor de Odoo
- Confirma que el producto no ha sido eliminado
- Busca reglas/restricciones conflictivas en el campo `website_sequence`
- Intenta ejecutar nuevamente más tarde
- Revisa el mensaje de error completo en el archivo de log

#### 6. Algunos Productos No Se Optimizan

**Causa**: Los productos pueden tener campo `website_sequence` de solo lectura, campos faltantes, o restricciones

**Solución**:
- Verifica la configuración del producto en Odoo
- Confirma que las personalizaciones de campos no restringen actualizaciones
- Busca registros que fallaron en los logs de error
- Puedes investigar productos específicos en la interfaz de Odoo

### Depuración General

1. Ejecuta con el flag `--verbose` para salida detallada
2. Revisa el archivo de log: `website_sequence_optimization.log`
3. Revisa el reporte JSON para detalles de productos específicos
4. Ejecuta con `--dry-run` primero para ver qué cambiaría
5. Verifica las credenciales en el archivo `.env`

### Obtener Ayuda

Si necesitas asistencia adicional:
- Incluye mensajes de error completos y entradas de log relevantes
- Comparte la salida de consola y el reporte JSON (sanitiza información sensible)
- Describe tu versión de Odoo y tamaño de la base de datos
- Proporciona pasos para reproducir el problema
- Contacta: **gomex1994@gmail.com**

---

## Autor

```
Desarrollado por: Álvaro Gómez
Contacto: gomex1994@gmail.com
Versión: 1.0.0
Fecha: Noviembre 2025
```

---

**Nota**: Para reportes de errores, solicitudes de características o contribuciones, por favor contacta a **gomex1994@gmail.com**
