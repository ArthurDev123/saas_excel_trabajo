# JobHunter - SaaS para Gestión de Búsqueda de Empleo

## 1. Project Overview

- **Nombre**: JobHunter
- **Tipo**: WebApp SaaS
- **Funcionalidad**: Organizar y rastrear las solicitudes de empleo enviadas por el usuario, con seguimiento de estado
- **Usuario objetivo**: Personas en búsqueda activa de empleo que necesitan organizar múltiples postulaciones

## 2. UI/UX Specification

### Layout Structure
- **Navbar**: Fijo en la parte superior, contiene logo y dos opciones de menú
- **Main Content**: Área central con padding, contiene las vistas
- **Responsive**: Diseño adaptativo para móvil y desktop

### Visual Design
- **Paleta de colores**:
  - Primary: `#1e3a5f` (azul profesional)
  - Secondary: `#3d5a80` (azul claro)
  - Accent: `#ee6c4d` (naranja vibrante)
  - Background: `#f8f9fa` (gris muy claro)
  - Card Background: `#ffffff`
  - Text: `#293241`
  
- **Estados de oferta**:
  - En espera: `#ffc107` (amarillo)
  - Primera entrevista: `#17a2b8` (azul claro)
  - Aceptada: `#28a745` (verde)
  - Rechazada: `#dc3545` (rojo)

- **Tipografía**:
  - Font principal: 'Segoe UI', system-ui, sans-serif
  - Headings: 600 weight
  - Body: 400 weight

- **Spacing**: 8px base unit

- **Efectos**: Sombras sutiles en cards, transiciones hover

### Components
- **Navbar**: Logo + Links de navegación (Ofertas Aplicadas, Buscar Trabajo)
- **Card de oferta**: Empresa, título, fecha, tipo, estado con badge
- **Dropdown estado**: Selector para cambiar estado
- **Formulario nueva oferta**: Campos para empresa, título, fecha, tipo, observaciones
- **Tabla/Listado**: Vista de todas las ofertas aplicadas

## 3. Functionality Specification

### Core Features
1. **Agregar nueva oferta aplicada**
   - Empresa (required)
   - Título del puesto (required)
   - Fecha de aplicación (required)
   - Tipo de empleo (Full-time, Part-time, Remoto, Contrato)
   - Salario (opcional)
   - Observaciones (opcional)

2. **Listar ofertas aplicadas**
   - Mostrar todas las ofertas en cards o tabla
   - Mostrar estado actual con color/-badge
   - Ordenar por fecha (más recientes primero)

3. **Cambiar estado de oferta**
   - Dropdown en cada oferta
   - Estados: En espera, Primera entrevista, Rechazada, Aceptada
   - Actualización inmediata

4. **Buscar trabajo** (vista simple por ahora)
   - Placeholder con enlaces a portales populares

5. **Persistencia de datos**
   - Usar SQLite para almacenar las ofertas
   - Los datos persisten entre sesiones

### User Flows
1. Usuario entra → Ve navbar con opciones
2. Click en "Ofertas Aplicadas" → Ve listado o formulario vacío
3. Click en "Agregar" → Completa formulario → Guarda → Aparece en listado
4. Usuario cambia estado → Se actualiza inmediatamente
5. Click en "Buscar Trabajo" → Ve recursos externos

## 4. Acceptance Criteria

- [ ] Navbar con dos opciones funcionales
- [ ] Formulario para agregar nuevas ofertas
- [ ] Listado de todas las ofertas aplicadas
- [ ] Dropdown funcional para cambiar estado
- [ ] Colores correctos según estado
- [ ] Datos persisten en SQLite
- [ ] Diseño responsive
- [ ] Sin errores al cargar la página
