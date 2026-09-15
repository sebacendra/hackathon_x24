# 📋 Document Consolidator - Local

**Versión local sin dependencias complejas. HTML puro + Python.**

---

## 🚀 Opción 1: HTML + Browser (Más fácil, 0 setup)

### Uso:
1. Descargar `consolidator_local.html`
2. Abrir en navegador (click derecho → Abrir con navegador)
3. Pegar tu API key de Anthropic
4. Pegar `mock_data.json`
5. Apretá "GENERAR DOCUMENTO"
6. Descarga automática

**Ventajas:**
- ✅ Sin instalar nada
- ✅ Sin terminal
- ✅ Sin Python
- ✅ Funciona offline (excepto la llamada a Claude)

---

## 💻 Opción 2: Python Script (Para backend/automatización)

### Setup (5 minutos):

**1. Instalar dependencias:**
```bash
pip install anthropic
```

**2. Configurar API key:**

**Opción A: Variable de entorno**
```bash
export ANTHROPIC_API_KEY=sk-ant-v0-xxxxxxx
```

**Opción B: Archivo `.env`**
```bash
echo "ANTHROPIC_API_KEY=sk-ant-v0-xxxxxxx" > .env
```

Luego en Python:
```python
from dotenv import load_dotenv
load_dotenv()
```

**3. Ejecutar:**
```bash
python consolidator.py
```

**Output:** `output/consolidacion_empresa_abc_20240915.html`

---

## 📝 Personalizar datos

### En HTML:
1. Abre `consolidator_local.html` con editor de texto
2. Cambia el textarea con tu `mock_data.json`
3. Guarda
4. Abre en navegador

### En Python:
1. Abre `consolidator.py` con editor
2. Reemplaza la sección `mock_data = { ... }`
3. Guarda y ejecuta: `python consolidator.py`

---

## 🔑 Obtener API Key

1. Ve a https://console.anthropic.com/
2. Sign up / Sign in
3. Click en "API Keys"
4. Click "Create Key"
5. Copia: `sk-ant-v0-...`

**Importante:** No compartas tu API key

---

## 📊 Archivos generados

Los documentos se guardan como **HTML** que se puede:
- ✅ Abrir en navegador
- ✅ Abrir en Word (guardar como .docx si quieres)
- ✅ Imprimir directamente
- ✅ Compartir por email

---

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not defined"
```bash
# Opción 1: Exportar en terminal
export ANTHROPIC_API_KEY=sk-ant-v0-...

# Opción 2: Crear .env
echo "ANTHROPIC_API_KEY=sk-ant-v0-..." > .env
```

### "JSON inválido"
- Verifica que tu `mock_data.json` sea válido (usa https://jsonlint.com/)

### "Error de API"
- Verifica que tu API key sea correcta
- Verifica que tengas crédito en Anthropic

---

## 💰 Costo

- **Modelo:** Claude 3.5 Sonnet
- **Costo por documento:** ~$0.05-0.10 USD
- **24 documentos:** ~$1-2 USD

---

## 📋 Checklist

- [ ] Descargar archivos (`consolidator_local.html` y/o `consolidator.py`)
- [ ] Obtener API key de Anthropic
- [ ] (Si usas Python) `pip install anthropic`
- [ ] Configurar ANTHROPIC_API_KEY
- [ ] Customizar `mock_data.json` con tus datos
- [ ] Generar primer documento
- [ ] Validar que se vea bien
- [ ] ¡Listo para usar!

---

## 🎯 Casos de uso

✅ **Consolidar comunicaciones de cliente**  
✅ **Generar documentos de post-venta**  
✅ **Extraer timeline de eventos**  
✅ **Listar contactos y responsabilidades**  
✅ **Automatizar en backend**  

---

**¿Dudas?** Revisar los comentarios en el código o ejecutar con `--help`
