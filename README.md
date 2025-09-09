# USS_AV_202515_INGO0002_4276
Solemne II Taller de programacion

# Dólar SBIF -- Consulta mensual con Streamlit + Matplotlib

Aplicación simple en **Python** que consulta la **API SBIF** para
obtener el valor del **dólar observado** por año/mes, muestra los datos
en una tabla y los **grafica con Matplotlib**.\
La UI está hecha con **Streamlit** y la lógica está separada por capas.

## 📁 Estructura del proyecto

    sbif-usd-app/
    ├─ app.py
    ├─ models/
    │  ├─ __init__.py
    │  └─ quote.py
    └─ services/
       ├─ __init__.py
       └─ sbif_client.py

-   `models/quote.py`: dataclass `DollarQuote` (fecha, valor, valor
    crudo).
-   `services/sbif_client.py`: cliente HTTP y parsing de respuesta SBIF.
-   `app.py`: UI de Streamlit + gráfico Matplotlib.

------------------------------------------------------------------------

## ✅ Requisitos

-   Python 3.10+ (recomendado 3.11).
-   Dependencias Python:
    -   `streamlit`
    -   `requests`
    -   `matplotlib`

Puedes instalarlas con `pip` (ver más abajo).

------------------------------------------------------------------------

## 🐍 Instalación de Python y pip

### Windows / macOS / Linux

1.  Descarga e instala [Python](https://www.python.org/downloads/).\
    Asegúrate de marcar la opción **"Add Python to PATH"** en Windows.

2.  Verifica la instalación:

    ``` bash
    python --version
    ```

3.  Si `pip` no está instalado, puedes instalarlo con:

    ``` bash
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    ```

4.  Confirma que `pip` quedó disponible:

    ``` bash
    pip --version
    ```

------------------------------------------------------------------------

## 🚀 Inicio rápido

### 1) Clonar el repo

``` bash
git clone https://github.com/jparadagt/USS_AV_202515_INGO0002_4276.git
cd USS_AV_202515_INGO0002_4276
```

### 2) (Opcional pero recomendado) Crear entorno virtual

**Windows (PowerShell):**

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Instalar dependencias

Con `requirements.txt`:

``` bash
pip install -r requirements.txt
```

> Si no tienes `requirements.txt`, instala manualmente:
>
> ``` bash
> pip install streamlit requests matplotlib
> ```

### 4) Configurar la API Key (SBIF)

**Opción A --- Usar `secrets.toml` (recomendado):**

Crea el archivo `.streamlit/secrets.toml` en la raíz del proyecto:

``` toml
SBIF_API_KEY = "TU_API_KEY_AQUI"
```

**Opción B --- Variable de entorno:**

``` bash
# Windows (PowerShell)
$env:SBIF_API_KEY="TU_API_KEY_AQUI"

# macOS / Linux (bash/zsh)
export SBIF_API_KEY="TU_API_KEY_AQUI"
```

> También puedes pegar tu API Key directamente en el campo de la app (no
> recomendado en producción).

### 5) Ejecutar la app

``` bash
streamlit run app.py
```

La app se abrirá en tu navegador (por defecto en
`http://localhost:8501`).

------------------------------------------------------------------------

## 🧭 Uso

1.  Selecciona **Año** y **Mes**.
2.  Haz clic en **🔎 Consultar**.
3.  Verás una tabla con las cotizaciones del mes y el gráfico en
    Matplotlib.
4.  Abajo se muestra el **último valor** disponible del período.

> **Notas:** - No se requieren cookies para llamar a la API. - El parser
> soporta coma decimal chilena (ej. `1.234,56`) y varios formatos de
> fecha. - Si no hay datos para el período, la app te avisará.

------------------------------------------------------------------------

## 🧩 Configuración y código (resumen)

-   **models/quote.py**
    -   Define `DollarQuote` con `date: datetime`, `value: float`,
        `raw_value: str`.
-   **services/sbif_client.py**
    -   `fetch_dollar_month(year, month, api_key)` hace el `GET` a SBIF
        y devuelve `List[DollarQuote]` ordenado por fecha.
    -   Incluye utilidades privadas para parsear números y fechas.
-   **app.py**
    -   Construye la UI (selects de año/mes, input de API Key, botón) y
        llama a `fetch_dollar_month`.
    -   Renderiza tabla y gráfico Matplotlib (sin estilos
        personalizados).

------------------------------------------------------------------------

## 🧪 Comandos útiles

Actualizar dependencias:

``` bash
pip freeze > requirements.txt
```

Formatear (si usas `black`):

``` bash
pip install black
black .
```

------------------------------------------------------------------------

## 🛠️ Troubleshooting

**"Import `streamlit` could not be resolved" (VS Code):** - Asegúrate de
que el **intérprete** seleccionado en VS Code sea el del entorno virtual
donde instalaste las dependencias:\
`Ctrl+Shift+P` → *Python: Select Interpreter* → elige `.venv`. - Instala
Pylance (extensión de VS Code) para mejor análisis. - Reinstala
dependencias: `pip install -r requirements.txt`.

**403 / permisos al hacer `git push`:** - Si ves
`denied to <otro-usuario>`, estás autenticando con credenciales
equivocadas. - En Windows: Panel de control → *Administrador de
credenciales* → elimina entradas de `github.com`. - Vuelve a hacer push
e inicia sesión con tu usuario correcto, o usa **SSH**.

------------------------------------------------------------------------

## 🔐 Seguridad

-   No subas tu `secrets.toml` al repo.\
-   No hardcodees el API Key en el código; usa `st.secrets` o variables
    de entorno.

------------------------------------------------------------------------

## 📄 Licencia

MIT
