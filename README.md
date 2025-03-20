# Login con Next.js y FastAPI

Este repositorio contiene una estructura de login basada en **Next.js (frontend)** y **FastAPI (backend)**, utilizando **autenticación con sesiones y cookies HTTP-only** para mayor seguridad.

## 📂 Estructura del Proyecto

```
login/
├── login-next/      # Frontend con Next.js
├── login-python/    # Backend con FastAPI
└── README.md        # Documentación del proyecto
```

---

## 🚀 Tecnologías Utilizadas

### **Frontend (Next.js 14 + App Router)**
- TypeScript
- TailwindCSS
- Zustand (manejo de estado)
- Cookies HTTP-only (para autenticación segura)
- API Routes para integración con el backend
- ShadCN + Sonner para UI y notificaciones

### **Backend (FastAPI + PostgreSQL)**
- FastAPI
- SQLAlchemy + Alembic (ORM y migraciones)
- Autenticación con sesiones
- Gestión de usuarios (registro, login, logout, perfil)
- Reset de contraseña con envío de correo

---

## ⚡ Instalación y Configuración

### **1️⃣ Clonar el repositorio**
```bash
git clone https://github.com/ivargasm/login-template.git
cd login
```

### **2️⃣ Configurar el Backend (FastAPI)**
```bash
cd login-python
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
#### **Configurar variables de entorno**
Crear un archivo `.env` en `login-python/` con:
```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/db_name
SECRET_KEY=supersecreto
SESSION_EXPIRE_MINUTES=60
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña
MAIL_FROM=tu_correo@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

#### **Ejecutar migraciones y levantar el servidor**
```bash
alembic upgrade head
uvicorn main:app --reload
```

---

### **3️⃣ Configurar el Frontend (Next.js)**
```bash
cd ../login-next
npm install
```
#### **Configurar variables de entorno**
Crear un archivo `.env.local` en `login-next/` con:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```
#### **Levantar el frontend**
```bash
npm run dev
```

---

## 🔑 Funcionalidades Implementadas
✅ Registro de usuarios con validaciones
✅ Inicio y cierre de sesión con cookies HTTP-only
✅ Protección de rutas (solo accesibles si el usuario está autenticado)
✅ Recuperación de contraseña con envío de email
✅ Redirección automática si el usuario ya está autenticado

---

## 🔐 Seguridad Implementada
- Uso de **cookies HTTP-only** para evitar ataques XSS
- **CSRF Token** incluido en las solicitudes de autenticación
- **Hash de contraseñas** con `bcrypt`
- **Sesiones en base de datos** en lugar de JWT

---

## 📌 Mejoras Futuras
- Agregar autenticación con OAuth (Google, GitHub, etc.)
- Implementar un panel de administración
- Enviar correos con un servicio como SendGrid en lugar de SMTP local

---



👨‍💻 **Desarrollado por:** Ismael Vargas Martinez

