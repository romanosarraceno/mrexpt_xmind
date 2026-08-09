# 📚 MRexpt to Markdown Processor

## 📖 Descripción

Herramienta para procesar archivos `.mrexpt` generados por **MoonReader** y convertirlos en documentos **Markdown** estructurados. Extrae anotaciones coloreadas, las limpia y permite filtrado interactivo.

## 🚀 Funcionalidades

- **Extrae anotaciones** de archivos `.mrexpt`
- **Convierte colores a niveles** de Markdown (`#`, `##`, `###`, etc.)
- **Limpia el texto** (corrige abreviaturas, espacios, mayúsculas)
- **Filtra por tema** (elimina todo lo anterior al tema seleccionado)
- **Corrige errores** interactivamente (reemplaza `1.` por el texto deseado)

## 📦 Dependencias
Solo usa biblioteca estándar de Python, no necesita instalación adicional.

## 💻 Uso
```bash
python mrexpt_xmind.py [archivo_mrexpt] [tema_filtro]
```

## 🎨 Mapeo de colores

| Color | Código | Nivel Markdown |
|-------|--------|----------------|
| 🟡 Amarillo | `2013265664` | `#` |
| 🔵 Azul | `1996532479` | `##` |
| 🟣 Morado | `-3368512` | `###` |
| 🟠 Naranja | `-28160` | `####` |
| 🟢 Verde | `-6706569` | `#####` |
| ⚪ Gris | `-2004318072` | `######` |

## 📝 Flujo de trabajo

1. **Lectura del archivo `.mrexpt`**  
   El script analiza el archivo exportado desde MoonReader y extrae todas las anotaciones con su texto y color asociado.

2. **Generación del Markdown**  
   Cada anotación se convierte en un encabezado de Markdown. El nivel del encabezado (`#`, `##`, `###`, etc.) depende del color de la anotación según el mapeo definido.

3. **Filtrado por tema (opcional)**  
   Si se proporciona un tema como argumento, el script busca todas las líneas que lo contienen y permite al usuario elegir desde qué línea cortar, eliminando todo el contenido anterior.

4. **Corrección interactiva de errores**  
   El script busca todas las ocurrencias de `1.` en el texto y permite al usuario reemplazarlas una por una desde la consola, con opción de saltar o salir en cualquier momento.

5. **Archivo final**  
   Se genera un archivo `.md` limpio y estructurado, listo para usar en cualquier editor o herramienta que soporte Markdown.

## 🔧 Personalización

El script permite varias opciones de personalización para adaptarlo a tus necesidades:

### Añadir correcciones de texto

En el método `correcciones_texto()` puedes añadir nuevas reglas de sustitución:

``` bash
# Añadir al bloque de correcciones concretas
texto = re.sub(r'texto_original', 'texto_reemplazo', texto)
```

Ejemplo:
``` bash
texto = re.sub(r'siglo', 's.', texto)  # Abreviatura de siglo
texto = re.sub(r'capitulo', 'cap.', texto)  # Abreviatura de capítulo
```

### Cambiar el mapeo de colores

Modifica el diccionario `color_to_header` en `procesar_anotaciones()` para asignar diferentes niveles:

``` bash
color_to_header = {
    "2013265664": 2,  # Ahora el amarillo será nivel 2 (##)
    "1996532479": 3,  # Azul será nivel 3 (###)
    # ...
}
```

### Desactivar correcciones específicas

Comenta o elimina las líneas que no quieras en `correcciones_texto()`:

``` bash
# texto = re.sub(r'11(?=\D|$)', 'II', texto)  # Desactivado
```

## ❓ Ejemplos de uso

### Ejemplo 1: Procesamiento básico

``` bash
python mrexpt_xmind.py HIE
```

**Resultado:** Genera `HIE T10.md` con todas las anotaciones convertidas a Markdown.

---

### Ejemplo 2: Con filtro de tema

``` bash
python mrexpt_xmind.py HIE "Tema 10"
```

**Resultado:** Elimina todo el contenido anterior a "Tema 10" y genera un Markdown limpio.

### Ejemplo 5: Entrada y salida

**Entrada (`HIE.mrexpt`):**
``` bash
#A*
#A7#El siglo XVIII en España#A8#
#A4#2013265664#A5#
#A*
#A7#La Guerra de Sucesión#A8#
#A4#1996532479#A5#
#A*
#A7#Los Borbones en el trono#A8#
#A4#-3368512#A5#
```

**Salida (`HIE T10.md`):**
``` bash
# El siglo XVIII en España
## La Guerra de Sucesión
### Los Borbones en el trono
```
