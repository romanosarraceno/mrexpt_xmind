import sys
import os
import re
import subprocess
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO

class mrexpt_xmind:

    def parse_mrexpt(self, filename):
        """Lee el archivo .mrexpt y agrupa todas las anotaciones en una List {texto, color}"""
        anotaciones = []
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()

        # Divide por anotación
        bloques = data.split("#A*")
        for bloque in bloques:
            if not bloque.strip():
                continue
            # Extrae campos con regex
            texto = re.search(r"#A7#(.*?)#A8#", bloque, re.DOTALL)
            color = re.search(r"#A4#(.*?)#A5#", bloque, re.DOTALL)
            if texto:
                texto = texto.group(1).strip()
            else:
                texto = ""
            if color:
                color = color.group(1).strip()
            else:
                color = ""
            texto = self.correcciones_texto(texto)
            anotaciones.append({"texto": texto, "color": color})
        return anotaciones

    def procesar_anotaciones(self, anotaciones, archivo_markdown):
        """Itera todas las iteraciones y compone el markdown con niveles según el color"""
        # Diccionario de colores: mapea el valor decimal a nivel de encabezado Markdown
        color_to_header = {
            "2013265664": 1,    # Amarillo
            "1996532479": 2,    # Azul
            "-3368512": 3,      # Morado
            "-28160": 4,        # Naranja
            "-6706569": 5,      # Verde
            "-2004318072": 6    # Gris
        }
        lineas_markdown = []

        for a in anotaciones:
            nivel = color_to_header.get(a["color"], 1)
            if a["texto"]:
                lineas_markdown.append(f"{'#' * nivel} {a['texto']}")

        with open(archivo_markdown, "w", encoding="utf-8") as f:
            f.write('\n'.join(lineas_markdown))

    def filtrar_por_tema(self, archivo_markdown, tema):
        """Filtra el markdown eliminando todo lo anterior al tema especificado.
        Muestra todas las líneas donde aparece el tema y permite elegir desde cuál cortar."""

        # Leer el archivo
        with open(archivo_markdown, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        print(f"BUSCANDO TEMA: '{tema}' ")

        # Buscar líneas que contengan el tema
        indices_encontrados = []
        for i, linea in enumerate(lineas):
            if tema.lower() in linea.lower():
                indices_encontrados.append(i)

        if not indices_encontrados:
            print(f"No se encontró '{tema}' en el markdown.")
            return False

        # Mostrar todas las líneas encontradas con su contexto
        print(f"\nEncontrado en {len(indices_encontrados)} línea(s):")
        print("-" * 60)

        for idx in indices_encontrados:
            # Mostrar la línea encontrada y las 2 anteriores para contexto
            inicio = max(0, idx - 2)
            print(f"\n Opción {idx}:")
            for j in range(inicio, idx + 1):
                if j == idx:
                    print(f"   🔴 Línea {j}: {lineas[j].strip()}  <--- ¡AQUÍ!")
                else:
                    print(f"      Línea {j}: {lineas[j].strip()}")

        # Preguntar al usuario desde qué línea quiere cortar
        print("\n" + "-" * 60)
        print("¿Desde qué línea quieres eliminar?")
        print("  - Introduce el número de línea para cortar desde ahí")
        print("  - Introduce 'q' para cancelar")

        while True:
            respuesta = input("\nLínea de corte (o 'q'): ").strip()

            if respuesta.lower() == 'q':
                print("Operación cancelada.")
                return False

            try:
                linea_corte = int(respuesta)
                if linea_corte in indices_encontrados:
                    break
                else:
                    print(f"   El número {linea_corte} no está en las opciones encontradas.")
                    print(f"   Opciones válidas: {indices_encontrados}")
            except ValueError:
                print("Por favor, introduce un número válido o 'q'.")

        # Mostrar confirmación
        print(f"\nSe eliminarán TODAS las líneas anteriores a la línea {linea_corte}")
        print(f"   (líneas 0 a {linea_corte - 1})")
        print(f"   Se mantendrán desde la línea {linea_corte} en adelante.")

        confirmar = input("\n¿Confirmas el borrado? (s/n): ")
        if confirmar.lower() == 's':
            # Guardar el archivo filtrado
            lineas_filtradas = lineas[linea_corte:]
            with open(archivo_markdown, "w", encoding="utf-8") as f:
                f.writelines(lineas_filtradas)
            print(f"Archivo filtrado. Quedan {len(lineas_filtradas)} líneas.")
            return True
        else:
            print("Operación cancelada.")
            return False

    def corregir_errores_consola(self, archivo_markdown):
        """Busca '1.' y permite corregirlos interactivamente."""
        with open(archivo_markdown, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        lineas_modificadas = []
        cambios_realizados = 0

        for i, linea in enumerate(lineas):
            if '1.' in linea:
                print(f"\nLínea {i}: {linea.strip()}")
                print("Contiene '1.' - ¿Quieres corregirlo?")
                respuesta = input("Introduce el texto correcto (Enter para saltar, 'q' para salir): ")

                if respuesta.lower() == 'q':
                    print("Saliendo de correcciones...")
                    break
                elif respuesta.strip():
                    # Reemplazar '1.' por el texto introducido
                    linea_corregida = linea.replace('1.', respuesta.strip())
                    lineas_modificadas.append(linea_corregida)
                    cambios_realizados += 1
                    print(f"Corregido: '{linea.strip()}' → '{linea_corregida.strip()}'")
                else:
                    lineas_modificadas.append(linea)
            else:
                lineas_modificadas.append(linea)

        if cambios_realizados > 0:
            with open(archivo_markdown, "w", encoding="utf-8") as f:
                f.writelines(lineas_modificadas)
            print(f"\nSe realizaron {cambios_realizados} correcciones.")
        else:
            print("\nNo se realizaron cambios.")

        return cambios_realizados

    def mayuscula_inicial(self, match):
        return match.group(1).upper()

    def correcciones_texto(self, texto):

        # correcciones concretas
        texto = re.sub(r'iglo xm','. XIII',texto)
        texto = re.sub(r'iglo xrv', '. XIV', texto)
        texto = re.sub(r'[s|S]iglo', 's.', texto)
        texto = re.sub(r'11(?=\D|$)', 'II', texto)
        texto = re.sub(r'^l.', '1.', texto)
        texto = re.sub(r'1.s', 'Los', texto)

        # correcciones cardinales
        #texto = re.sub(r'[o|O]ccidente', 'Occ.', texto)
        #texto = re.sub(r'[o|O]riente', 'Or.', texto)
        #texto = re.sub(r'[n|N]orte', 'N.', texto)
        #texto = re.sub(r'[s|S]ur', 'S.', texto)
        #texto = re.sub(r'[^a-zA-Z][e|E]ste[^a-zA-Z]', 'E.', texto)
        #texto = re.sub(r'[o|O]este', 'O.', texto)

        # correcciones generales
        texto = re.sub(r'^(\s*[a-záéíóúñ])', self.mayuscula_inicial, texto)
        texto = re.sub(r'-\s*\n', '', texto, flags=re.MULTILINE)
        texto = re.sub(r' - ', ' ', texto)
        texto = re.sub(r'\n', '', texto, flags=re.MULTILINE)
        texto = re.sub(r'­', '', texto, flags=re.MULTILINE)
        texto = re.sub(r' +', ' ', texto)
        texto = re.sub(r'^\( +', '(', texto)
        texto = re.sub(r' +\)', ')', texto)

        return texto

    def execute(self, input_mrexpt, output_md, tema=None):
        print(f"Procesando {input_mrexpt}.mrexpt...")

        # Paso 1: Parsear y generar markdown
        anotaciones = self.parse_mrexpt(input_mrexpt + ".mrexpt")
        self.procesar_anotaciones(anotaciones, output_md + ".md")
        print(f"Markdown generado: {output_md}.md")

        # Paso 2: Filtrar por tema si se especifica
        print("\nFiltro por tema...")
        if tema:
            self.filtrar_por_tema(output_md + ".md", tema)

        # Paso 3: Corregir errores '1.' en consola
        print("\nIniciando corrección de errores '1.'...")
        self.corregir_errores_consola(output_md + ".md")

        print("\nProceso completado!")

if __name__ == "__main__":

    asignatura = sys.argv[1]
    tema = sys.argv[2] if len(sys.argv) > 2 else None

    a = mrexpt_xmind()
    a.execute(asignatura, asignatura + " T10", tema)
