# KeleaCare

## Descripción del proyecto
KeleaCare es una aplicación de bienestar emocional basada en inteligencia artificial y construida sobre la plataforma Streamlit. Su propósito es proporcionar una herramienta de apoyo emocional a los usuarios mediante un chatbot empático, un diario emocional para el registro de sentimientos, un perfilador de personalidad y un sistema de gestión de objetivos personales.

## Problema que resuelve
En la actualidad, muchas personas enfrentan dificultades para gestionar sus emociones y establecer metas personales. KeleaCare ayuda a abordar este problema al proporcionar:
- Un chatbot empático que puede interpretar y responder de manera comprensiva a los estados emocionales del usuario.
- Un diario emocional que permite registrar y analizar estados de ánimo a lo largo del tiempo.
- Un sistema de perfilado de personalidad basado en inteligencia artificial.
- Un módulo de gestión de objetivos personales que ayuda a los usuarios a mantenerse enfocados en sus metas.

## Dependencias
Para ejecutar KeleaCare correctamente, se requiere la instalación de las siguientes librerías y herramientas:
- **Streamlit** (para la interfaz de usuario interactiva)
- **Transformers** (para el análisis de emociones)
- **SentenceTransformer** (para la generación de embeddings de texto)
- **FAISS** (para la búsqueda de similitudes en bases de datos vectoriales)
- **Torch** (para el uso de modelos de deep learning)
- **Requests** (para comunicación con APIs externas)
- **VaderSentiment** (para análisis de sentimiento léxico)

Para instalar todas las dependencias, ejecute el siguiente comando: *pip install -r requirements.txt*

## Cómo ejecutar el proyecto

Para ejecutar KeleaCare en tu entorno local, sigue estos pasos:

1. **Clona el repositorio.**
2. **Instala las dependencias.**
3. **Ejecuta la aplicación con el siguiente comando:** *streamlit run app.py*
4. **Interactuar con la interfaz.**

## Uso del proyecto

KeleaCare cuenta con una interfaz simple y accesible que permite a los usuarios navegar entre las diferentes funcionalidades mediante un menú lateral. Se incluyen las siguientes opciones:

1. **Chatbot**: Permite interactuar con un asistente virtual que responde de manera empática según el estado emocional detectado.
2. **Diario Emocional**: Los usuarios pueden registrar su estado de ánimo y recibir un análisis de su evolución emocional.
3. **Perfil de Personalidad**: Basado en respuestas del usuario, se genera un perfil psicológico con el fin de personalizar la experiencia de uso.
4. **Objetivos Personales**: Se pueden establecer y rastrear metas personales utilizando modelos de IA para generar recomendaciones personalizadas.

## Estado del proyecto

Actualmente, KeleaCare es funcional en sus cuatro módulos principales.

## Cómo reportar problemas

Si encuentras algún error o tienes problemas al utilizar la aplicación, por favor abre un **issue** en el repositorio de GitHub en la sección de _Issues_.

## Cómo Contribuir

Las contribuciones al proyecto son bienvenidas. Para colaborar:

1. **Revisa los issues abiertos** para ver qué funcionalidades necesitan ayuda.
2. **Haz un fork** del repositorio.
3. **Crea una nueva rama** para tu contribución.
4. **Realiza un pull request** describiendo los cambios realizados.

## Créditos y Contribuyentes

Este proyecto ha sido desarrollado por un equipo de estudiantes de IA como parte de una hackathon. Agradecemos todas las contribuciones y apoyo recibido.
