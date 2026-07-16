# Login con Next.js y FastAPI (Enterprise Boilerplate) 🚀

Este repositorio contiene una estructura de inicio (boilerplate) robusta y lista para producción basada en **Next.js 14 (App Router)** y **FastAPI**, utilizando autenticación segura, validaciones avanzadas, rate limiting y despliegue rápido con Docker.

## 📂 Estructura del Proyecto

```
login-template/
├── login-next/      # Frontend con Next.js (React Hook Form, Zod, Zustand)
├── login-python/    # Backend con FastAPI (SQLAlchemy, Alembic, SlowAPI)
├── docker-compose.yml # Orquestación de contenedores para desarrollo
├── .env             # Variables de entorno globales
└── README.md        # Documentación del proyecto
```

---

## 🚀 Tecnologías Utilizadas

### **Frontend (Next.js 14 + App Router)**
- **TypeScript**
- **TailwindCSS** + **ShadCN** + **Lucide Icons**
- **React Hook Form + Zod** (Validación de formularios tipada y segura)
- **Zustand** (Manejo de estado global)
- **Cookies HTTP-only** (Almacenamiento seguro de sesión)
- **Skeletons/Loaders** (Para transiciones y cargas de UX premium)

### **Backend (FastAPI + PostgreSQL)**
- **FastAPI**
- **SQLAlchemy + Alembic** (ORM y migraciones automáticas)
- **SlowAPI** (Rate Limiting para evitar ataques de fuerza bruta)
- **JWT** (Validación de sesión y refresh tokens en cookies)
- **Resend** (Envío de emails para recuperación de contraseña)
- Scripts de auto-inicialización de esquemas y sembrado de roles.

### **Infraestructura**
- **Docker & Docker Compose** (Entorno de desarrollo idéntico y portable con Hot-Reloading)

---

## ⚡ Instalación y Configuración (Modo Docker 🐳)

¡La forma más rápida de empezar a programar!

### **1️⃣ Clonar el repositorio**
```bash
git clone https://github.com/ivargasm/login-template.git
cd login-template
```

### **2️⃣ Configurar las variables de entorno**
El proyecto usa un único archivo `.env` en la raíz que alimenta tanto a la base de datos como al backend.

Renombra el archivo de ejemplo o crea uno en la raíz (`.env`):
```env
# /login-template/.env

DB_HOST=db
DB_USER=postgres
DB_PORT=5432
DB_NAME=login_db
DB_PASSWORD=tu_contraseña_secreta

SCHEMA=public
SECRET_KEY=supersecreto_generado_con_openssl
SESSION_EXPIRE_MINUTES=60

# Configuración de Resend (Email)
RESEND_API_KEY=tu_api_key
RESEND_MAIL_FROM=no-reply@tudominio.com
URL_FRONT=http://localhost:3000
```

### **3️⃣ Levantar el ecosistema completo**
```bash
docker compose up --build
```
*Docker descargará las imágenes, creará la base de datos, ejecutará las migraciones, sembrará los roles (`admin`, `user`) y levantará tanto el frontend en el puerto `3000` como el backend en el `8000`. ¡Cualquier cambio que hagas en el código se reflejará en tiempo real!*

Para apagar el entorno:
```bash
docker compose stop
```

---

## 🔑 Funcionalidades Implementadas

✅ **Validación de Formularios Avanzada:** Formularios de registro y login completamente validados en tiempo real con *React Hook Form* y *Zod*.
✅ **Rate Limiting:** Los endpoints críticos (`/login`, `/register`) están protegidos contra ataques de fuerza bruta (Límite de 5 peticiones/minuto).
✅ **Seguridad de Sesión:** Tokens JWT almacenados estrictamente en **Cookies HTTP-only**, previniendo ataques XSS.
✅ **UX Premium:** Implementación de *Skeletons* mientras la sesión se valida en segundo plano, evitando parpadeos bruscos en la interfaz.
✅ **Auto-sembrado de Base de Datos:** Scripts automatizados (`pre_start.py`, `seed_roles.py`) que aseguran que la base de datos y sus roles básicos siempre estén presentes al arrancar.
✅ **Recuperación de contraseña** integrada mediante correos electrónicos asíncronos con *Resend*.

---

## 📌 Mejoras Futuras
- Agregar autenticación con OAuth (Google, GitHub, etc.)
- Implementar un panel de administración para gestión de usuarios.

---

👨‍💻 **Desarrollado por:** Ismael Vargas Martinez
