# Registro de visitantes Holcim Costa Rica

Proyecto simple (Flask + HTML) para registro de visitantes.

**Estructura**
- backend/: aplicación Flask
- frontend/: páginas estáticas (login + formulario)
- deploy/: archivo de ejemplo para Render
- .gitignore

**Credenciales iniciales**
- Usuario: `CoordinadorHolcim`
- Contraseña: `123`

**Instalación y ejecución (entorno local)**
1. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # unix
   venv\Scripts\activate   # windows
   ```
2. Instalar dependencias:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Ejecutar:
   ```bash
   cd backend
   python app.py
   ```
4. Abrir en el navegador: http://127.0.0.1:5000

**Notas**
- La base de datos SQLite se crea automáticamente en `backend/data/visitors.db`.
- Este proyecto es una plantilla básica para comenzar. Recomendado: mejorar la seguridad antes de producción (HTTPS, gestión de contraseñas, protección CSRF).
