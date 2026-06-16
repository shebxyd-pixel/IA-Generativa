import re
import bleach
import os

# ==================================================
# 🛡️ SANITIZACIÓN CONTRA INYECCIÓN DE SCRIPTS Y CÓDIGO
# ==================================================
class SanitizadorEntrada:
    def __init__(self):
        # Caracteres y patrones prohibidos (inyección, comandos, etiquetas)
        self.patrones_peligrosos = [
            r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>",  # Etiquetas script
            r"javascript:", r"vbscript:", r"onload=", r"onclick=", r"onerror=",  # Eventos JS
            r"eval\s*\(", r"exec\s*\(", r"system\s*\(", r"shell\s*\(",  # Ejecución de código
            r"drop\s+table", r"select\s+.*\s+from", r"insert\s+into", r"delete\s+from",  # SQL
            r"rm\s+-rf", r"mkdir\s+", r"rmdir\s+", r"chmod\s+", r"sudo\s+",  # Comandos sistema
            r"<iframe", r"<object", r"<embed", r"<svg", r"<link", r"<meta"  # Etiquetas peligrosas
        ]
        # Configuración de limpieza de HTML/permitidos
        self.etiquetas_permitidas = ["b", "i", "u", "strong", "em", "p", "ul", "ol", "li", "h1", "h2", "h3"]
        self.atributos_permitidos = {}

    def limpiar_texto(self, texto: str) -> str:
        if not isinstance(texto, str):
            texto = str(texto)

        # Paso 1: Eliminar patrones peligrosos con expresiones regulares
        for patron in self.patrones_peligrosos:
            texto = re.sub(patron, "", texto, flags=re.IGNORECASE)

        # Paso 2: Limpiar HTML restante, solo dejar etiquetas seguras
        texto_limpio = bleach.clean(
            texto,
            tags=self.etiquetas_permitidas,
            attributes=self.atributos_permitidos,
            strip=True,
            strip_comments=True
        )

        # Paso 3: Eliminar caracteres de control y códigos ocultos
        texto_limpio = re.sub(r"[\x00-\x1F\x7F-\x9F]", "", texto_limpio)

        # Paso 4: Normalizar espacios
        texto_limpio = re.sub(r"\s+", " ", texto_limpio).strip()

        return texto_limpio

    def es_entrada_segura(self, texto: str) -> bool:
        """Verifica si la entrada no tiene contenido peligroso después de limpiar"""
        texto_limpio = self.limpiar_texto(texto)
        # Si al limpiar se eliminó todo el contenido peligroso y queda texto útil
        return len(texto_limpio) > 0 and len(texto_limpio) <= 10000  # Límite mayor para prompts largos

    def sanitizar_nombre_archivo(self, nombre: str) -> str:
        """Sanitiza nombres de archivos para prevenir path traversal"""
        # Eliminar caracteres peligrosos para nombres de archivos
        nombre_limpio = re.sub(r'[<>:"/\\|?*]', '', nombre)
        # Eliminar rutas absolutas o relativas
        nombre_limpio = os.path.basename(nombre_limpio)
        # Limitar longitud
        if len(nombre_limpio) > 255:
            nombre_limpio = nombre_limpio[:255]
        return nombre_limpio
