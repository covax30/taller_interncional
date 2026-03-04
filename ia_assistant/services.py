import os
from groq import Groq
from apy.models import Vehiculo, Insumos, Cliente, Caja, Gastos, Repuesto

def consultar_ia_con_datos(prompt_usuario):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Recopilamos datos reales para el contexto
    contexto_taller = {
        "vehiculos": Vehiculo.objects.count(),
        "insumos": Insumos.objects.count(),
        "clientes": Cliente.objects.count(),
        "repuestos": Repuesto.objects.count(),
        "total_caja": sum(c.monto for c in Caja.objects.filter(tipo_movimiento='ingreso')) - sum(c.monto for c in Caja.objects.filter(tipo_movimiento='egreso')),
        "gastos_totales": sum(g.monto for g in Gastos.objects.all())
    }

    system_prompt = f"""
    Eres el Asistente Inteligente del 'Taller Internacional de Motores'.
    Tienes acceso a la base de datos en tiempo real:
    - Vehículos registrados: {contexto_taller['vehiculos']}
    - Clientes en base de datos: {contexto_taller['clientes']}
    - Insumos en inventario: {contexto_taller['insumos']}
    - Repuestos disponibles: {contexto_taller['repuestos']}
    - Saldo estimado en Caja: ${contexto_taller['total_caja']}
    - Gastos totales registrados: ${contexto_taller['gastos_totales']}

    Responde de forma profesional, breve y técnica. Si el usuario pregunta por cantidades, usa estos datos.
    Si algo está en 0, sugiérele al usuario empezar a registrar información.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", 
                "content": "Eres T.I.M., el asistente experto del Taller Internacional de Motores..."},
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_usuario}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Lo siento, tuve un problema al conectar con mis circuitos: {str(e)}"