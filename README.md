# ⛴️ HellasGo: Optimizador Inteligente de Viajes a Grecia

**HellasGo** es una aplicación web interactiva desarrollada en **Streamlit (Python)** diseñada para simplificar y optimizar la planificación de viajes a las islas griegas (enfocada inicialmente en **Agistri, Milos, Tinos, Symi y Halki**). Combina algoritmos de decisión multicriterio, datos de vuelos en tiempo real, opciones reales de alojamiento y estimaciones de costes de vida.

---

## 🚀 Características Principales

* **🏆 Optimizador Multicriterio (MCDA):** Pondera de forma dinámica el coste total, el tiempo de transporte y la calidad del alojamiento según las preferencias del usuario.
* **✈️ Búsqueda en Tiempo Real:** Integración con API de vuelos (RapidAPI - Sky Scrapper) con un robusto sistema de *degradación elegante* (fallback) para garantizar la estabilidad ante fallos de cuota.
* **🏨 Catálogo de Alojamientos Verificados:** Base de datos curada de **50 opciones reales** (10 por isla) entre hoteles boutique y Airbnbs, con cálculo de precio dinámico según el número de noches.
* **💰 Simulador de Presupuesto:** Permite establecer un límite de gasto máximo para filtrar y alertar instantáneamente sobre los destinos asequibles.
* **✨ Filtro por "Vibe" / Estilo de Viaje:** Ajusta las recomendaciones según intereses específicos (playas paradisíacas, tranquilidad, gastronomía, romántico/relajado, etc.).
* **🍔 Calculadora de Gasto Diario:** Estima el coste de vida local (comidas, tabernas y transporte interno) por cada destino.
* **📥 Exportador de Informes:** Generador de planes de viaje personalizados descargables en formato Markdown.
* **⚓ Información de Conexión:** Horarios detallados, frecuencias y puertos de salida para los ferris.

---

## 🛠️ Stack Tecnológico

* **Frontend & UI:** [Streamlit](https://streamlit.io/) (Python)
* **Manipulación y Análisis de Datos:** `pandas`
* **Conectividad API / Red:** `requests`
* **Control de Versiones:** Git & GitHub
* **Despliegue en la Nube:** Streamlit Community Cloud

---

## 📂 Estructura del Proyecto
---

## ⚙️ Instalación y Ejecución Local

Si deseas clonar y ejecutar este proyecto en tu propio entorno de desarrollo:

1. **Clonar el repositorio:**
2. **Crear y activar un entorno virtual:**
3. **Instalar las dependencias:**
4. **Ejecutar la aplicación:**
---

## 🌐 Despliegue en Producción

La aplicación se encuentra desplegada y accesible en la nube mediante **Streamlit Community Cloud**, garantizando disponibilidad pública y actualización continua integrada directamente con los cambios de la rama `main` de este repositorio.
