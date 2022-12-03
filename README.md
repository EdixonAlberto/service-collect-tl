# Service Collect TL

## Inicio
Instalar el administrador de entornos en Python `pipenv` y configuarar las variables de entorno usando el archivo [.env.template](./.env.template) como plantilla.
```bash
pip install pipenv
cp .env.template .env
```

## Desarrollo
Para desarrollar en el codigo primero se debe iniciar el entorno con `pipenv`, instalar todas las dependencias y por último arrancar el servidor con el script `dev` creado en el archivo [Pipfile](./Pipfile)

```bash
# Iniciar entorno
pipenv shell

# Instalar dependencias
pipenv install

# Inicar app en modo desarrollo
pipenv run dev
```
## Despliegue

Para desplegar se debe instalar primero las depedencias a travez del archivo [requirements.txt](./requirements.txt) y luego arancar el servidor usando la libreria `uvicorn`

```bash
# Build
pip install -r requirements.txt

# Start
uvicorn main:app --host 0.0.0.0 --port $PORT
```
