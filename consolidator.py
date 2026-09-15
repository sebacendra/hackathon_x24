#!/usr/bin/env python3
"""
Document Consolidator MVP - Local Python Script
Uso: python consolidator.py
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sys

try:
    from anthropic import Anthropic
except ImportError:
    print("❌ Falta instalar dependencias:")
    print("   pip install anthropic")
    sys.exit(1)

# ============= CONFIG =============
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY no definida")
    print("   Opción 1: export ANTHROPIC_API_KEY=sk-ant-v0-...")
    print("   Opción 2: Crea .env con: ANTHROPIC_API_KEY=sk-ant-v0-...")
    sys.exit(1)

client = Anthropic(api_key=API_KEY)

# ============= DATOS MOCK =============
mock_data = {
    "cliente": "Empresa ABC",
    "proyecto": "Proyecto XYZ - Post-venta",
    "emails": [
        {
            "id": "email_001",
            "fecha": "2024-09-01",
            "from": "contacto@empresa.com",
            "nombre_from": "Juan García",
            "asunto": "Consulta urgente - Implementación",
            "body": "Hola, escribo para consultar sobre el estado de la implementación. Tenemos problemas en la integración con nuestro backend."
        },
        {
            "id": "email_002",
            "fecha": "2024-09-02",
            "from": "gerente@empresa.com",
            "nombre_from": "María López",
            "asunto": "Re: Consulta urgente",
            "body": "Gracias por contactar. Hemos identificado el problema. Esperamos resolverlo en 48 horas. ¿Podemos coordinar una llamada?"
        }
    ],
    "whatsapp": [
        {
            "id": "wa_001",
            "fecha": "2024-09-02T14:30:00",
            "from": "Juan García",
            "rol": "Gerente Técnico",
            "mensaje": "¿Qué onda con la integración? El cliente está pidiendo news urgente"
        }
    ],
    "instagram": [
        {
            "id": "ig_001",
            "fecha": "2024-09-03",
            "from": "cliente_ig_user",
            "mensaje": "Vimos el update. Gracias por mantener informados. ¿Cuándo podemos testear?"
        }
    ],
    "notas_foto": [
        {
            "id": "nota_001",
            "fecha": "2024-09-03",
            "quien": "Analista",
            "contexto": "Requerimientos finales",
            "transcripcion": "Cliente solicita: 1) Reporte diario, 2) Alertas SMS, 3) Backup automático"
        }
    ]
}

# ============= PROMPT =============
PROMPT_TEMPLATE = """TAREA: Analiza datos de comunicaciones y extrae información estructurada.

DATOS A ANALIZAR:
{mock_data}

INSTRUCCIONES:
1. Extrae TODAS las personas mencionadas: nombre completo, rol, email (si existe), teléfono (si existe)
2. Crea TIMELINE cronológica: lista cada evento/comunicación importante con fecha, qué pasó, quién lo dijo
3. Escribe RESUMEN: 2-3 párrafos resumiendo el contexto, el problema y la situación actual
4. Define ESTADO_ACTUAL: una sola frase corta sobre cómo está ahora
5. Lista PENDIENTES: qué tareas/decisiones quedan por hacer

FORMATO DE RESPUESTA:
Debes responder EXACTAMENTE así, sin nada más, sin markdown, solo JSON puro:

{{"personas":[{{"nombre":"Juan García","rol":"Gerente Técnico","email":"juan@empresa.com","telefono":"+54911234567"}}],"timeline":[{{"fecha":"2024-09-01","evento":"Cliente reporta problema de integración","quien":"Juan García","tipo":"problema"}}],"resumen":"El cliente ABC está implementando sistema XYZ...","estado_actual":"En resolución - esperando fix en 48h","pendientes":["Resolver error de integración"]}}"""

# ============= FUNCIONES =============

def llamar_claude(mock_data):
    """Llama a Claude API y retorna JSON estructurado"""
    prompt = PROMPT_TEMPLATE.format(mock_data=json.dumps(mock_data, ensure_ascii=False, indent=2))
    
    print("📤 Llamando a Claude API...")
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = response.content[0].text
    
    # Limpiar markdown si está presente
    jsontext = response_text.strip()
    if "```json" in jsontext:
        jsontext = jsontext.split("```json")[1].split("```")[0].strip()
    elif "```" in jsontext:
        jsontext = jsontext.split("```")[1].split("```")[0].strip()
    
    try:
        resultado = json.loads(jsontext)
        print("✅ Claude respondió con JSON válido")
        return resultado
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON: {e}")
        print(f"Respuesta: {response_text[:300]}")
        raise


def generar_html(mock_data, datos_consolidados):
    """Genera documento HTML profesional"""
    print("📄 Generando documento HTML...")
    
    # Timeline
    timeline_html = '<table style="width:100%; border-collapse:collapse; margin:20px 0;">'
    timeline_html += '<tr style="background:#f0f0f0;"><th style="border:1px solid #ddd; padding:8px; text-align:left;">Fecha</th><th style="border:1px solid #ddd; padding:8px; text-align:left;">Evento</th><th style="border:1px solid #ddd; padding:8px; text-align:left;">Quién</th></tr>'
    for evento in datos_consolidados.get("timeline", []):
        timeline_html += f'<tr><td style="border:1px solid #ddd; padding:8px;">{evento.get("fecha", "-")}</td><td style="border:1px solid #ddd; padding:8px;">{evento.get("evento", "-")}</td><td style="border:1px solid #ddd; padding:8px;">{evento.get("quien", "-")}</td></tr>'
    timeline_html += '</table>'
    
    # Contactos
    contactos_html = '<table style="width:100%; border-collapse:collapse; margin:20px 0;">'
    contactos_html += '<tr style="background:#f0f0f0;"><th style="border:1px solid #ddd; padding:8px; text-align:left;">Nombre</th><th style="border:1px solid #ddd; padding:8px; text-align:left;">Rol</th><th style="border:1px solid #ddd; padding:8px; text-align:left;">Email</th></tr>'
    for persona in datos_consolidados.get("personas", []):
        contactos_html += f'<tr><td style="border:1px solid #ddd; padding:8px;">{persona.get("nombre", "-")}</td><td style="border:1px solid #ddd; padding:8px;">{persona.get("rol", "-")}</td><td style="border:1px solid #ddd; padding:8px;">{persona.get("email", "-")}</td></tr>'
    contactos_html += '</table>'
    
    # HTML final
    pendientes_html = '\n'.join([f'<li>{p}</li>' for p in datos_consolidados.get("pendientes", [])])
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Consolidacion</title>
    <style>
        body {{ font-family: Calibri, Arial, sans-serif; max-width: 900px; margin: 40px auto; line-height: 1.6; color: #333; }}
        h1 {{ font-size: 28px; text-align: center; margin-bottom: 10px; }}
        .subtitle {{ text-align: center; font-size: 14px; color: #666; margin-bottom: 30px; }}
        h2 {{ font-size: 16px; margin-top: 30px; margin-bottom: 10px; border-bottom: 2px solid #667eea; padding-bottom: 5px; }}
        h3 {{ font-size: 14px; margin-top: 15px; margin-bottom: 8px; }}
        p {{ margin: 10px 0; }}
        ul {{ margin-left: 20px; }}
        li {{ margin: 5px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #f0f0f0; font-weight: bold; }}
        .estado-box {{ background: #e3f2fd; padding: 15px; border-left: 4px solid #667eea; margin: 15px 0; }}
    </style>
</head>
<body>
    <h1>{mock_data.get('cliente', 'Cliente')}</h1>
    <p class="subtitle">{mock_data.get('proyecto', 'Proyecto')}</p>
    <p class="subtitle">Generado: {datetime.now().strftime('%d/%m/%Y')}</p>
    
    <h2>1. RESUMEN EJECUTIVO</h2>
    <p>{datos_consolidados.get('resumen', 'N/A')}</p>
    
    <h2>2. ESTADO & PENDIENTES</h2>
    <div class="estado-box">
        <strong>Estado:</strong> {datos_consolidados.get('estado_actual', 'N/A')}
    </div>
    
    <h3>Pendientes:</h3>
    <ul>
        {pendientes_html}
    </ul>
    
    <h2>3. TIMELINE</h2>
    {timeline_html}
    
    <h2>4. CONTACTOS</h2>
    {contactos_html}
</body>
</html>"""
    
    return html


def guardar_documento(html, mock_data):
    """Guarda documento HTML"""
    Path("output").mkdir(exist_ok=True)
    
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    cliente_slug = mock_data.get('cliente', 'cliente').replace(" ", "_").replace("-", "_").lower()
    output_path = f"output/consolidacion_{cliente_slug}_{fecha}.html"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path


# ============= MAIN =============

def main():
    print("\n" + "="*60)
    print("🚀 DOCUMENT CONSOLIDATOR MVP - LOCAL")
    print("="*60 + "\n")
    
    try:
        # 1. Llamar Claude
        print("1️⃣ Procesando datos con Claude...")
        datos_consolidados = llamar_claude(mock_data)
        
        # 2. Generar HTML
        print("2️⃣ Generando documento...")
        html = generar_html(mock_data, datos_consolidados)
        
        # 3. Guardar
        print("3️⃣ Guardando archivo...")
        output_path = guardar_documento(html, mock_data)
        
        print("\n" + "="*60)
        print("✅ COMPLETADO")
        print("="*60)
        print(f"📄 Documento: {output_path}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
