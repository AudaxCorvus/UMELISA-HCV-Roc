Aquí tienes el archivo `README.md` completo para el repositorio de GitHub:

```markdown
# UMELISA HCV - Sistema de Análisis de Placas

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Sistema de escritorio para el análisis de placas de laboratorio UMELISA HCV. Permite cargar archivos de fluorescencia, procesar controles, interpretar resultados mediante curvas ROC y visualizar datos de manera interactiva.

## 📋 Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Características](#características)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Guía de Uso](#guía-de-uso)
- [Formato de Archivos](#formato-de-archivos)
- [Procesamiento de Datos](#procesamiento-de-datos)
- [Curva ROC](#curva-roc)
- [Generación de Datos de Prueba](#generación-de-datos-de-prueba)
- [Solución de Problemas](#solución-de-problemas)
- [Contribución](#contribución)
- [Licencia](#licencia)

## 🎯 Descripción General

UMELISA HCV es una aplicación desarrollada para laboratorios que utilizan el sistema UMELISA para detección de Hepatitis C. La herramienta automatiza el procesamiento de lecturas de placas de 96 pozos, aplica controles de calidad según criterios SUMA y clasifica muestras como Positivo, Negativo, Borderline o Repetir.

### Flujo de Trabajo
1. Carga del archivo `.flu` con valores de fluorescencia
2. Extracción automática de controles (blanco, positivo, negativo)
3. Validación de la placa según parámetros SUMA
4. Cálculo de valores CALC por muestra
5. Interpretación usando cutoff (manual o entrenado con ROC)
6. Visualización de resultados (tabla, placa coloreada, gráficos)
7. Entrenamiento de curva ROC con datos históricos

## ✨ Características

| Característica | Descripción |
|----------------|-------------|
| **Carga de placas** | Soporte para archivos `.flu` con 96 valores |
| **Controles automáticos** | Extrae y calcula BB, NN, PP y RELAC |
| **Validación SUMA** | Verifica controles según umbrales configurables |
| **Interpretación flexible** | Cutoff manual o entrenado con ROC |
| **Curva ROC dinámica** | Entrenamiento continuo con pesos personalizados |
| **Visualización** | Placa coloreada, tabla de resultados, gráficos |
| **Carga masiva** | Procesamiento de múltiples archivos desde carpeta |
| **Persistencia** | Guardado automático de datos ROC |

## 💻 Requisitos del Sistema

### Software
- **Python**: 3.8 o superior
- **Sistema operativo**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 11+

### Dependencias Principales
```
numpy >= 1.21.0
scikit-learn >= 1.0.0
matplotlib >= 3.5.0
tkinter (incluido con Python)
```

### Hardware Recomendado
- **Procesador**: 2 cores a 1.5 GHz
- **RAM**: 2 GB (4 GB para procesamiento masivo)
- **Almacenamiento**: 100 MB para datos
- **Resolución**: 1024x768 o superior

## 📦 Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/umelisa-hcv.git
cd umelisa-hcv
```

### 2. Crear Entorno Virtual (Recomendado)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verificar Instalación
```bash
python -c "import numpy, sklearn, matplotlib; print('✅ Todas las dependencias instaladas correctamente')"
```

### 5. Ejecutar la Aplicación
```bash
python main.py
```

Para Windows también puedes usar el script:
```cmd
run.bat
```

## 📁 Estructura del Proyecto

```
umelisa-hcv/
│
├── main.py                      # Aplicación principal (GUI)
├── generate_plates.py           # Utilidad para generar datos de prueba
├── requirements.txt             # Dependencias del proyecto
├── run.bat                      # Script de inicio para Windows
│
├── models/                      # Capa de datos
│   ├── __init__.py
│   ├── plate_model.py          # Modelo de placa (96 pozos)
│   └── assay_model.py          # Modelo de ensayo (procesamiento)
│
├── controllers/                 # Capa de lógica de negocio
│   ├── __init__.py
│   ├── assay_controller.py     # Controlador de ensayos
│   └── roc_controller.py       # Controlador de curva ROC
│
├── views/                       # Capa de presentación
│   ├── __init__.py
│   └── assay_view.py           # Vista principal (Tkinter)
│
└── data/                        # Datos persistentes
    └── roc_data.json           # Datos de entrenamiento ROC (autogenerado)
```

## 🖥️ Guía de Uso

### Menú Archivo
| Opción | Atajo | Descripción |
|--------|-------|-------------|
| Abrir placa | `Ctrl+O` | Carga archivo `.flu` desde el sistema |
| Salir | `Ctrl+Q` | Cierra la aplicación |

### Menú Procesamiento
| Opción | Descripción |
|--------|-------------|
| Interpretar con cutoff actual | Reinterpreta usando el cutoff entrenado del ROC |
| Interpretar con cutoff manual | Permite ingresar un valor numérico (ej. 0.3) |

### Menú Visualización
| Opción | Descripción |
|--------|-------------|
| Ver placa completa | Muestra los 96 pozos con códigos de colores |
| Ver tabla de resultados | Tabla detallada con valores F1, F2, CALC y resultado |
| Ver imagen valores | Gráfico de barras con fluorescencia por muestra |

### Menú ROC
| Opción | Descripción |
|--------|-------------|
| Actualizar ROC | Agrega el ensayo actual al entrenamiento |
| Ver información del ROC | Muestra cutoff actual, AUC y total de muestras |
| Cargar varios archivos | Procesa múltiples archivos `.flu` de una carpeta |
| Limpiar registro ROC | Elimina todos los datos entrenados |

### Códigos de Color en la Placa

| Color | Significado |
|-------|-------------|
| 🟢 Verde claro | Borderline (zona gris) |
| 🔴 Rojo claro | Positivo |
| ⚪ Blanco | Negativo |
| 🔵 Azul claro | Repetir (inconsistencia en duplicados) |
| 🟡 Amarillo | Controles (blanco) |
| 🔵 Azul | Controles positivos |
| 🟤 Marrón | Controles negativos |
| ⚫ Gris | Pozo vacío (valor 0) |

## 📄 Formato de Archivos

### Archivo `.flu` (Fluorescencia)
El archivo debe contener 96 valores numéricos, uno por línea, ordenados por **columna primero**:

```
# Columna 1 (pozos A1, B1, C1, ..., H1)
1.23
0.98
2.45
3.12
1.87
2.34
1.56
2.01

# Columna 2 (pozos A2, B2, ..., H2)
...
```

**Características soportadas:**
- Separador decimal: punto (.) o coma (,)
- Comentarios: líneas que comienzan con `#` se ignoran
- Líneas vacías: se omiten automáticamente
- Valores no numéricos: se reemplazan con 0.0

### Ejemplo de Archivo Válido
```
0.95
0.88
125.32
124.87
3.45
3.12
# ... continuar hasta 96 valores
```

## 🔬 Procesamiento de Datos

### Posiciones de Controles (Fijas)

| Control | Pozo 1 | Pozo 2 | Descripción |
|---------|--------|--------|-------------|
| Blanco | A1 | B1 | Blanco del sistema |
| Positivo | C1 | D1 | Control positivo UMELISA |
| Negativo | E1 | F1 | Control negativo |

### Cálculos Internos

| Variable | Fórmula | Descripción |
|----------|---------|-------------|
| **BB** | (B1 + B2) / 2 | Promedio de blancos |
| **NN** | (N1 + N2) / 2 | Promedio de negativos |
| **PP** | min(P1, P2) | Valor mínimo de positivos |
| **RELAC** | (NN - BB) / (PP - BB) | Relación de validación |
| **CALC** | (F - BB) / (PP - BB) | Valor normalizado por muestra |
| **Cutoff** | cut_factor × (PP - BB) + BB | Umbral de decisión |

### Validación SUMA

La placa es **VÁLIDA** solo si se cumplen todas las condiciones:

| Condición | Requisito | Error si no cumple |
|-----------|-----------|-------------------|
| Blancos | B1 < 10.0 y B2 < 10.0 | "Blanco ≥ 10" |
| Negativos | N1 < BB+10 y N2 < BB+10 | "Negativo > BB+10" |
| Positivos | 60 < P1 < 180 y 60 < P2 < 180 | "P fuera de 60-180" |
| Relación | RELAC < 0.1 | "Ratio ≥ 0.1" |

### Interpretación de Muestras

| Condición | Resultado |
|-----------|-----------|
| Ambos CALC < cutoff_low | **Negativo** |
| Ambos CALC > cutoff | **Positivo** |
| Ambos en zona gris | **BL** (Borderline) |
| Uno positivo y otro negativo | **Repetir** |
| CV entre duplicados > 20% | **Repetir** |

*cutoff_low = cut_factor × 0.85 × (PP - BB) + BB*

## 📊 Curva ROC

### Algoritmo de Entrenamiento

El sistema implementa un entrenamiento continuo de curva ROC con las siguientes características:

1. **Generación de etiquetas**: Usa cutoff fijo de referencia (0.3) para evitar circularidad
2. **Pesos personalizados**: Asigna pesos según cercanía al cutoff
3. **Máximo de muestras**: 500 muestras (evita sobrecarga)
4. **Optimización**: Índice de Youden (tpr - fpr) para seleccionar cutoff óptimo

### Pesos por Zona

| Rango de CALC | Etiqueta | Peso |
|---------------|----------|------|
| > 0.3 + 15% | Positivo | 1.0 |
| > 0.3 | Positivo | 0.5 |
| [0.255 - 0.3] | Negativo | 0.3 |
| < 0.255 | Negativo | 1.0 |

### Fórmulas ROC
- **Sensibilidad**: TPR = TP / (TP + FN)
- **Especificidad**: TNR = TN / (TN + FP)
- **AUC**: Área bajo la curva ROC
- **Cutoff óptimo**: max(TPR - FPR)

## 🧪 Generación de Datos de Prueba

La utilidad `generate_plates.py` permite crear archivos `.flu` simulados para pruebas:

```bash
python generate_plates.py
```

### Características de los Datos Generados
- **500 placas** por defecto (configurable)
- Valores realistas con distribución normal
- Controles dentro de rangos válidos
- Opción para generar placas inválidas
- Guardado en carpeta `placas_generadas/`

### Configuración
```python
NUM_PLACAS = 500          # Número de placas a generar
# Cambiar en el archivo generate_plates.py
```

## 🔧 Solución de Problemas

### Error: "No module named 'tkinter'"
**Solución:** Instalar tkinter según sistema operativo:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (con Homebrew)
brew install python-tk
```

### Error: "Permission denied" al guardar datos
**Solución:** Verificar permisos de escritura:
```bash
# Crear directorio data manualmente
mkdir data
chmod 755 data
```

### Error: Archivo .flu no carga correctamente
**Verificar:**
- Archivo tiene al menos 6 valores (controles)
- Valores son numéricos
- No hay caracteres no imprimibles

### La aplicación no responde al cargar muchos archivos
**Nota:** La carga masiva utiliza hilos separados; esperar a que termine el procesamiento. El progreso se muestra en ventana emergente.

## 🤝 Contribución

### Reportar Issues
1. Verificar si el issue ya existe
2. Incluir mensaje de error completo
3. Adjuntar archivo `.flu` de ejemplo (si aplica)

### Pull Requests
1. Fork el repositorio
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abrir Pull Request

### Estilo de Código
- Seguir PEP 8
- Documentar funciones con docstrings
- Incluir type hints cuando sea posible

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Contacto y Soporte

- **Issues**: [GitHub Issues](https://github.com/AudaxCorvus/umelisa-hcv/issues)
- **Documentación**: [Wiki del Proyecto](https://github.com/AudaxCorvus/umelisa-hcv/docs)

---

## 📚 Referencias Técnicas

- **UMELISA**: Sistema inmunoenzimático UMELISA, Centro de Inmunoensayo, Cuba
- **Curvas ROC**: Fawcett, T. (2006). An introduction to ROC analysis. Pattern recognition letters, 27(8), 861-874.
- **Validación SUMA**: Procedimientos estándar para control de calidad en ensayos UMELISA

---

*Desarrollado para laboratorios de diagnóstico clínico que utilizan tecnología UMELISA HCV.*
```

Este README incluye:

1. **Estructura completa** con todas las secciones necesarias para un repositorio profesional
2. **Instalación detallada** paso a paso con comandos para diferentes sistemas operativos
3. **Explicación técnica** de todos los procesos: controles, validación, cálculos y ROC
4. **Guía de uso** con todos los menús y opciones disponibles
5. **Formato de archivos** con ejemplos concretos
6. **Solución de problemas** para errores comunes
7. **Contribución** y estándares de código
8. **Tablas y diagramas** para mejor comprensión

El archivo está listo para copiar y pegar directamente en tu repositorio.