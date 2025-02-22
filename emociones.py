from transformers import pipeline

# Usar el modelo preentrenado
modelo_emoroBerta = "bhadresh-savani/bert-base-uncased-emotion"
analizador_emociones = pipeline("text-classification", model=modelo_emoroBerta)

# Función para analizar la emoción en el texto con un umbral de score
def analizar_emocion_emoroBerta(texto, umbral=0.7):
    resultado = analizador_emociones(texto)
    label = resultado[0]['label']
    score = resultado[0]['score']
    
    # Si el score es menor que el umbral, podemos asignar 'neutral' o ningún resultado
    if score < umbral:
        label = "neutral"
    
    # Devolver todas las emociones y sus scores
    emociones = {r['label']: r['score'] for r in resultado}

    return label, score, emociones

# Ejemplo de uso
texto = "Lo que hizo me parece completamente inaceptable"
emocion, score, todas_emociones = analizar_emocion_emoroBerta(texto) 
print(f"Emoción detectada: {emocion} con un score de: {score}")
print("Todas las emociones detectadas:", todas_emociones)
