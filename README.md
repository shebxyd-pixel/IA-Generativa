# Kofu v0.7 (Beta)

Plataforma de Inteligencia Artificial para Microsoft Office.

## Requisitos del sistema

- **Sistema Operativo**: Windows 10 o superior
- **Python**: Versión 3.10 o superior
- **Microsoft Office**: PowerPoint y Word instalados
- **Conexión a Internet**: Para investigación web (modo Online)

## Instalación

1. Instala Python desde [python.org](https://www.python.org/)
2. Abre una terminal en la carpeta del proyecto
3. Ejecuta: `pip install -r requirements.txt`

## Uso rápido

1. **Inicia el servidor**: Haz doble clic en `iniciar.bat` o ejecuta `cd backend && py server.py`
2. **Abre la interfaz**: Abre el archivo `web/index.html` en tu navegador
3. **Comienza a usar Kofu**: Escribe tus mensajes y crea documentos o presentaciones

## Funcionalidades principales

- **Chat interactivo**: Habla con Kofu
- **Crear documentos Word**: Genera documentos automáticos
- **Crear presentaciones PowerPoint**: Genera presentaciones automáticas
- **Modo Local**: Usa Kofu sin conexión a internet
- **Modo Online**: Investigación web y funciones avanzadas
- **Plantillas personalizadas**: Usa tus propias plantillas de Office
- **Carga de archivos**: Procesa documentos, imágenes, audio y más usando MarkItDown
- **Razonamiento offline avanzado**: Integración con Ollama para usar modelos locales

## Integración con MarkItDown

Kofu usa **MarkItDown** para convertir diversos tipos de archivos a Markdown/texto para su procesamiento por modelos de lenguaje.

### Funcionalidades habilitadas por MarkItDown

- **Formatos soportados:
  - PDF (.pdf)
  - Documentos de Word (.docx)
  - Presentaciones de PowerPoint (.pptx)
  - Hojas de cálculo Excel (.xlsx, .xls)
  - Imágenes (.jpg, .jpeg, .png, .gif, .bmp, .tiff)
  - Audio (.wav, .mp3, .m4a, .ogg, .flac)
  - HTML, texto plano, Markdown, CSV, JSON, XML
  - EPUB, ZIP, Outlook (.msg), Jupyter Notebooks (.ipynb)

- **Uso:
  - Arrastra y suelta un archivo en la interfaz de Kofu
  - Selecciona un documento o presentación para generar
  - Kofu extraerá el contenido del archivo y podrás usarlo para crear nuevos documentos o presentaciones

- **Seguridad**:
  - MarkItDown procesa los archivos con las restricciones del proceso actual
  - Kofu sanitiza todas las entradas antes de procesarlas para garantizar seguridad

### Configuración avanzada

MarkItDown está incluido en el proyecto en modo editable desde la carpeta `markitdown/`. Para más información sobre MarkItDown, consulta `markitdown/README.md`.

## Integración con Ollama (Razonamiento offline)

Kofu tiene integración con Ollama para usar modelos locales y razonamiento avanzado sin conexión a internet.

### Cómo configurar Ollama:
1. Descarga e instala Ollama desde [ollama.com/download](https://ollama.com/download)
2. Descarga un modelo (recomendado: `ollama pull llama3`)
3. Configura tu archivo .env con: USE_OLLAMA=true
4. Inicia Kofu con `iniciar.bat`

## Primeros pasos

1. Selecciona el tipo de documento (Word o PowerPoint)
2. (Opcional) Selecciona una plantilla
3. (Opcional) Carga un archivo para usar su contenido
4. Escribe tu solicitud y envía
5. Kofu creará el documento o presentación automáticamente

## Para más información

Consulta el `Manual de Usuario.md` para instrucciones detalladas y solución de problemas.
