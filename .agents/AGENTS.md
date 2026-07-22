# Reglas del Boilerplate (Next.js 14 + FastAPI)

Este documento define las reglas arquitectónicas y las directrices obligatorias para cualquier agente o desarrollador que trabaje en este proyecto o en cualquiera que se haya clonado a partir de este boilerplate. 

**LEER SIEMPRE ESTAS REGLAS ANTES DE MODIFICAR O AGREGAR CÓDIGO.**

## 1. Zonas Horarias y Fechas (Backend)
- **Regla Estricta:** Toda la base de datos (PostgreSQL) y los modelos de SQLAlchemy DEBEN manejar fechas y horas exclusivamente en **UTC**.
- Nunca uses la hora local del servidor.
- Al definir campos de fecha en SQLAlchemy, usa siempre `DateTime(timezone=True)`.
- Al generar la fecha actual en Python, usa siempre `datetime.now(timezone.utc)`.
- El motor de la base de datos debe ser instanciado forzando el timezone: `connect_args={"options": "-c timezone=gmt-6"}` (o UTC según aplique en el ecosistema).

## 2. Autenticación y Seguridad (Fullstack)
- **Cookies HTTP-Only:** La autenticación se basa en Tokens JWT, pero los tokens JAMÁS deben ser enviados al cliente para ser guardados en LocalStorage o SessionStorage.
- FastAPI siempre debe adjuntar el JWT en una cookie `HttpOnly`, `Secure` y `SameSite="Lax"` (o `None` según el entorno).
- El endpoint de logout debe eliminar la cookie explícitamente replicando los mismos atributos de seguridad con los que se creó.

## 3. Manejo de Formularios y Validación (Frontend)
- Para validación en el cliente, está estrictamente prohibido manejar estados manualmente con `useState` masivos.
- **Regla Estricta:** Todo formulario nuevo debe usar **React Hook Form** integrado con **Zod** (`@hookform/resolvers/zod`).
- Muestra mensajes de error al usuario provenientes de Zod o de los códigos HTTP del backend.

## 4. Rutas Protegidas (Frontend)
- Las rutas que requieran autenticación en Next.js deben ser manejadas a través de la lógica de estado de sesión.
- Cualquier página privada debe estar envuelta por el flujo que verifica `userAuth` e `isLoading` desde el store global de Zustand (`useAuthStore`).
- Si se requiere hacer `redirect` tras un cierre de sesión provocado por el cliente (fuera de un componente de servidor), utiliza `window.location.href = "/auth/login"` en lugar del router nativo para evitar conflictos con Server Actions.

## 5. Prevención de Abusos (Rate Limiting)
- Los endpoints sensibles del backend (como login, registro o reseteo de contraseñas) deben estar protegidos con **SlowAPI**.
- Inyecta el parámetro `request: Request` en el endpoint de FastAPI y usa el decorador `@limiter.limit("X/minute")`.
- El frontend debe capturar siempre el error HTTP `429 (Too Many Requests)` y mostrar un mensaje amigable al usuario indicando el tiempo de espera.

## 6. Configuración de Entornos y Docker
- **Variables Centralizadas:** El archivo `.env` reside única y exclusivamente en la RAÍZ del proyecto.
- Los contenedores de Docker (backend, frontend y db) consumen las variables de este `.env` maestro inyectadas a través de `docker-compose.yml`.
- Nunca agregues archivos `.env` sueltos dentro de las subcarpetas `login-python/` ni expongas secretos en imágenes de Docker. 

*(Estas reglas aseguran que el proyecto mantenga su estándar Enterprise, maximizando la seguridad, legibilidad y el rendimiento de la aplicación).*
