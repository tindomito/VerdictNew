#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar documentación PDF del proyecto VerdictMMA
Usando ReportLab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

# Registrar fuente Unicode
try:
    pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
    DEFAULT_FONT = 'DejaVu'
    BOLD_FONT = 'DejaVuBold'
except:
    DEFAULT_FONT = 'Helvetica'
    BOLD_FONT = 'Helvetica-Bold'

def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='MainTitle',
        fontName=BOLD_FONT,
        fontSize=28,
        textColor=colors.HexColor('#4F46E5'),
        alignment=TA_CENTER,
        spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        name='SubTitle',
        fontName=DEFAULT_FONT,
        fontSize=14,
        textColor=colors.HexColor('#6B7280'),
        alignment=TA_CENTER,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='ChapterTitle',
        fontName=BOLD_FONT,
        fontSize=16,
        textColor=colors.HexColor('#4F46E5'),
        spaceBefore=20,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontName=BOLD_FONT,
        fontSize=12,
        textColor=colors.HexColor('#374151'),
        spaceBefore=15,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name='CustomBody',
        fontName=DEFAULT_FONT,
        fontSize=10,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=5,
        leading=14
    ))

    styles.add(ParagraphStyle(
        name='BulletText',
        fontName=DEFAULT_FONT,
        fontSize=10,
        textColor=colors.HexColor('#4B5563'),
        leftIndent=15,
        spaceAfter=3,
        leading=13
    ))

    styles.add(ParagraphStyle(
        name='CodeText',
        fontName=DEFAULT_FONT,
        fontSize=9,
        textColor=colors.HexColor('#1E40AF'),
        leftIndent=10,
        spaceAfter=3,
        leading=12
    ))

    return styles

def generate_pdf():
    output_path = '/home/user/VerdictNew/VerdictMMA_Documentacion.pdf'
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)

    styles = create_styles()
    story = []

    # ========== PORTADA ==========
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph('VerdictMMA', styles['MainTitle']))
    story.append(Paragraph('Documentacion Tecnica del Proyecto', styles['SubTitle']))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', styles['SubTitle']))
    story.append(Paragraph('Stack: Vue 3 + Vite + Supabase + Tailwind CSS', styles['SubTitle']))
    story.append(PageBreak())

    # ========== INDICE ==========
    story.append(Paragraph('INDICE DE CONTENIDOS', styles['ChapterTitle']))
    story.append(Spacer(1, 0.5*cm))

    indice = [
        '1. Informacion General del Proyecto',
        '2. Stack Tecnologico',
        '3. Estructura de Directorios',
        '4. Componentes (src/components/)',
        '5. Paginas (src/pages/)',
        '6. Servicios (src/services/)',
        '7. Composables (src/composables/)',
        '8. Router y Rutas',
        '9. Estructura de Datos',
        '10. Caracteristicas Principales'
    ]

    for item in indice:
        story.append(Paragraph(item, styles['CustomBody']))

    story.append(PageBreak())

    # ========== 1. INFORMACION GENERAL ==========
    story.append(Paragraph('1. INFORMACION GENERAL DEL PROYECTO', styles['ChapterTitle']))

    story.append(Paragraph('Descripcion', styles['SectionTitle']))
    story.append(Paragraph('VerdictMMA es una aplicacion web social enfocada en la comunidad de artes marciales mixtas (MMA). Permite a los usuarios crear publicaciones, interactuar mediante comentarios, chatear publicamente y de forma privada, y gestionar sus perfiles con un sistema de rangos.', styles['CustomBody']))

    story.append(Paragraph('Datos del Proyecto', styles['SectionTitle']))
    story.append(Paragraph('* Nombre: VerdictMMA', styles['BulletText']))
    story.append(Paragraph('* Tipo: Single Page Application (SPA)', styles['BulletText']))
    story.append(Paragraph('* Idioma: Espanol', styles['BulletText']))
    story.append(Paragraph('* Total de archivos en src: 35', styles['BulletText']))
    story.append(Paragraph('* Lineas de codigo aprox: 7,846', styles['BulletText']))
    story.append(Paragraph('* Tamano total src: 336 KB', styles['BulletText']))

    story.append(PageBreak())

    # ========== 2. STACK TECNOLOGICO ==========
    story.append(Paragraph('2. STACK TECNOLOGICO', styles['ChapterTitle']))

    story.append(Paragraph('Frontend', styles['SectionTitle']))
    story.append(Paragraph('* Vue.js 3.5.18 - Framework reactivo progresivo', styles['BulletText']))
    story.append(Paragraph('* Vue Router 4.5.1 - Sistema de enrutamiento SPA', styles['BulletText']))
    story.append(Paragraph('* Vite 7.1.2 - Build tool y dev server', styles['BulletText']))
    story.append(Paragraph('* Tailwind CSS 4.1.12 - Framework CSS utilities-first', styles['BulletText']))

    story.append(Paragraph('Backend (BaaS)', styles['SectionTitle']))
    story.append(Paragraph('* Supabase 2.57.4 - Backend as a Service', styles['BulletText']))
    story.append(Paragraph('  - Autenticacion de usuarios', styles['BulletText']))
    story.append(Paragraph('  - Base de datos PostgreSQL', styles['BulletText']))
    story.append(Paragraph('  - Storage para archivos', styles['BulletText']))
    story.append(Paragraph('  - Real-time subscriptions', styles['BulletText']))

    story.append(PageBreak())

    # ========== 3. ESTRUCTURA ==========
    story.append(Paragraph('3. ESTRUCTURA DE DIRECTORIOS', styles['ChapterTitle']))

    estructura = """
/VerdictNew/
  public/                 - Archivos estaticos publicos
  src/                    - Codigo fuente principal
    main.js              - Punto de entrada
    App.vue              - Componente raiz
    style.css            - Estilos globales (Tailwind)
    components/          - 12 componentes reutilizables
    pages/               - 9 vistas/paginas
    services/            - 7 servicios de logica
    composables/         - 3 composables Vue 3
    router/              - Configuracion de rutas
  index.html             - HTML principal
  package.json           - Dependencias npm
  vite.config.js         - Configuracion Vite
"""
    for line in estructura.strip().split('\n'):
        story.append(Paragraph(line, styles['CodeText']))

    story.append(PageBreak())

    # ========== 4. COMPONENTES ==========
    story.append(Paragraph('4. COMPONENTES (src/components/)', styles['ChapterTitle']))

    # darkNavbar.vue
    story.append(Paragraph('darkNavbar.vue (24.3 KB)', styles['SectionTitle']))
    story.append(Paragraph('Barra de navegacion principal con tema oscuro.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Menu de navegacion responsivo', styles['BulletText']))
    story.append(Paragraph('* Busqueda de usuarios con autocompletado', styles['BulletText']))
    story.append(Paragraph('* Menu de usuario autenticado', styles['BulletText']))
    story.append(Paragraph('* Toggle de menu movil', styles['BulletText']))
    story.append(Paragraph('* Integracion con sistema de autenticacion', styles['BulletText']))

    # PublicationCard.vue
    story.append(Paragraph('PublicationCard.vue (16.4 KB)', styles['SectionTitle']))
    story.append(Paragraph('Card para mostrar publicaciones individuales.', styles['CustomBody']))
    story.append(Paragraph('Props: publication, currentUserId', styles['CustomBody']))
    story.append(Paragraph('Eventos: edit, delete', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Muestra titulo, contenido, categoria e imagen', styles['BulletText']))
    story.append(Paragraph('* Botones de editar/eliminar para el autor', styles['BulletText']))
    story.append(Paragraph('* Badge de categoria con icono', styles['BulletText']))
    story.append(Paragraph('* Link al perfil del autor', styles['BulletText']))
    story.append(Paragraph('* Formateo de fechas', styles['BulletText']))

    # EditPublication.vue
    story.append(Paragraph('EditPublication.vue (14.7 KB)', styles['SectionTitle']))
    story.append(Paragraph('Modal para editar publicaciones existentes.', styles['CustomBody']))
    story.append(Paragraph('Props: show, publication', styles['CustomBody']))
    story.append(Paragraph('Eventos: close, updated', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Formulario de edicion completo', styles['BulletText']))
    story.append(Paragraph('* Cambio de imagen', styles['BulletText']))
    story.append(Paragraph('* Selector de categoria', styles['BulletText']))
    story.append(Paragraph('* Validacion de campos', styles['BulletText']))

    # CreatePublication.vue
    story.append(Paragraph('CreatePublication.vue (13.2 KB)', styles['SectionTitle']))
    story.append(Paragraph('Modal para crear nuevas publicaciones.', styles['CustomBody']))
    story.append(Paragraph('Props: show', styles['CustomBody']))
    story.append(Paragraph('Eventos: close, created', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Formulario de creacion', styles['BulletText']))
    story.append(Paragraph('* Subida de imagen opcional', styles['BulletText']))
    story.append(Paragraph('* Selector de 7 categorias', styles['BulletText']))
    story.append(Paragraph('* Validacion de titulo y contenido', styles['BulletText']))

    story.append(PageBreak())

    # CommentsList.vue
    story.append(Paragraph('CommentsList.vue (10.2 KB)', styles['SectionTitle']))
    story.append(Paragraph('Lista de comentarios de una publicacion.', styles['CustomBody']))
    story.append(Paragraph('Props: publicationId', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Carga y muestra comentarios', styles['BulletText']))
    story.append(Paragraph('* Formulario para nuevo comentario', styles['BulletText']))
    story.append(Paragraph('* Paginacion/carga infinita', styles['BulletText']))
    story.append(Paragraph('* Edicion y eliminacion de propios', styles['BulletText']))

    # ProfileHeader.vue
    story.append(Paragraph('ProfileHeader.vue (6.2 KB)', styles['SectionTitle']))
    story.append(Paragraph('Encabezado de perfil con informacion principal.', styles['CustomBody']))
    story.append(Paragraph('Props: profile', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Avatar grande del usuario', styles['BulletText']))
    story.append(Paragraph('* Nombre y rango', styles['BulletText']))
    story.append(Paragraph('* Badge PRO si aplica', styles['BulletText']))
    story.append(Paragraph('* Biografia', styles['BulletText']))

    # ProfileCard.vue
    story.append(Paragraph('ProfileCard.vue (6.4 KB)', styles['SectionTitle']))
    story.append(Paragraph('Card compacta de perfil para listas.', styles['CustomBody']))
    story.append(Paragraph('Props: profile', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Avatar pequeno', styles['BulletText']))
    story.append(Paragraph('* Nombre con link', styles['BulletText']))
    story.append(Paragraph('* Indicador de rango', styles['BulletText']))

    # CommentCard.vue
    story.append(Paragraph('CommentCard.vue', styles['SectionTitle']))
    story.append(Paragraph('Card individual de comentario.', styles['CustomBody']))
    story.append(Paragraph('Props: comment, currentUserId', styles['CustomBody']))
    story.append(Paragraph('Eventos: edit, delete', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Muestra autor, fecha y contenido', styles['BulletText']))
    story.append(Paragraph('* Opciones de editar/eliminar', styles['BulletText']))

    # ToastNotification.vue
    story.append(Paragraph('ToastNotification.vue (4.2 KB)', styles['SectionTitle']))
    story.append(Paragraph('Sistema de notificaciones emergentes.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Tipos: success, error, info, warning', styles['BulletText']))
    story.append(Paragraph('* Auto-dismiss configurable', styles['BulletText']))
    story.append(Paragraph('* Posicionamiento flexible', styles['BulletText']))
    story.append(Paragraph('* Animaciones de entrada/salida', styles['BulletText']))

    # RankBadge.vue
    story.append(Paragraph('RankBadge.vue (3.9 KB)', styles['SectionTitle']))
    story.append(Paragraph('Badge que muestra el rango del usuario.', styles['CustomBody']))
    story.append(Paragraph('Props: rango, showProgress', styles['CustomBody']))
    story.append(Paragraph('Rangos: Novato, Aprendiz, Luchador, Guerrero, Veterano, Experto, Maestro, Leyenda, Campeon, Hall of Fame', styles['CustomBody']))

    # AppH1.vue y myFooter.vue
    story.append(Paragraph('AppH1.vue (168 B)', styles['SectionTitle']))
    story.append(Paragraph('Componente simple de titulo H1 estilizado.', styles['CustomBody']))

    story.append(Paragraph('myFooter.vue (159 B)', styles['SectionTitle']))
    story.append(Paragraph('Pie de pagina minimalista.', styles['CustomBody']))

    story.append(PageBreak())

    # ========== 5. PAGINAS ==========
    story.append(Paragraph('5. PAGINAS (src/pages/)', styles['ChapterTitle']))

    # Home.vue
    story.append(Paragraph('Home.vue (14.0 KB) - Ruta: /', styles['SectionTitle']))
    story.append(Paragraph('Pagina de inicio/landing page.', styles['CustomBody']))
    story.append(Paragraph('No requiere autenticacion.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Hero section con gradientes', styles['BulletText']))
    story.append(Paragraph('* Call-to-action para registro/login', styles['BulletText']))
    story.append(Paragraph('* Informacion sobre la plataforma', styles['BulletText']))
    story.append(Paragraph('* Secciones de caracteristicas', styles['BulletText']))

    # Login.vue
    story.append(Paragraph('Login.vue (7.9 KB) - Ruta: /login', styles['SectionTitle']))
    story.append(Paragraph('Formulario de inicio de sesion.', styles['CustomBody']))
    story.append(Paragraph('No requiere autenticacion.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Campo de email', styles['BulletText']))
    story.append(Paragraph('* Campo de contrasena', styles['BulletText']))
    story.append(Paragraph('* Validacion de formulario', styles['BulletText']))
    story.append(Paragraph('* Redireccion post-login', styles['BulletText']))
    story.append(Paragraph('* Link a registro', styles['BulletText']))

    # Register.vue
    story.append(Paragraph('Register.vue (11.3 KB) - Ruta: /register', styles['SectionTitle']))
    story.append(Paragraph('Formulario de registro de usuarios.', styles['CustomBody']))
    story.append(Paragraph('No requiere autenticacion.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Campos: email, contrasena, nombre de usuario', styles['BulletText']))
    story.append(Paragraph('* Validacion de campos', styles['BulletText']))
    story.append(Paragraph('* Verificacion de contrasena', styles['BulletText']))
    story.append(Paragraph('* Creacion de perfil automatica', styles['BulletText']))

    # Publications.vue
    story.append(Paragraph('Publications.vue (14.8 KB) - Ruta: /publicaciones', styles['SectionTitle']))
    story.append(Paragraph('Feed principal de publicaciones.', styles['CustomBody']))
    story.append(Paragraph('Requiere autenticacion.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Lista de publicaciones paginadas', styles['BulletText']))
    story.append(Paragraph('* Filtro por categoria', styles['BulletText']))
    story.append(Paragraph('* Boton crear publicacion', styles['BulletText']))
    story.append(Paragraph('* Carga infinita o paginacion', styles['BulletText']))

    story.append(PageBreak())

    # Profile.vue
    story.append(Paragraph('Profile.vue (21.0 KB) - Ruta: /profile/:id?', styles['SectionTitle']))
    story.append(Paragraph('Pagina de perfil de usuario.', styles['CustomBody']))
    story.append(Paragraph('Autenticacion opcional (publico).', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Muestra perfil propio o de otros', styles['BulletText']))
    story.append(Paragraph('* Lista de publicaciones del usuario', styles['BulletText']))
    story.append(Paragraph('* Estadisticas del perfil', styles['BulletText']))
    story.append(Paragraph('* Informacion de rango', styles['BulletText']))
    story.append(Paragraph('* Boton de chat privado (si no es propio)', styles['BulletText']))

    # Settings.vue
    story.append(Paragraph('Settings.vue (32.4 KB) - Ruta: /settings', styles['SectionTitle']))
    story.append(Paragraph('Configuracion completa de cuenta.', styles['CustomBody']))
    story.append(Paragraph('Requiere autenticacion.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Cambio de avatar', styles['BulletText']))
    story.append(Paragraph('* Edicion de nombre de usuario', styles['BulletText']))
    story.append(Paragraph('* Edicion de biografia', styles['BulletText']))
    story.append(Paragraph('* Cambio de contrasena', styles['BulletText']))
    story.append(Paragraph('* Vista previa de perfil', styles['BulletText']))
    story.append(Paragraph('* Informacion de rango', styles['BulletText']))

    # PublicChat.vue
    story.append(Paragraph('PublicChat.vue (16.8 KB) - Ruta: /chat', styles['SectionTitle']))
    story.append(Paragraph('Chat publico en tiempo real.', styles['CustomBody']))
    story.append(Paragraph('No requiere autenticacion para ver.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Mensajes en tiempo real', styles['BulletText']))
    story.append(Paragraph('* Lista de usuarios conectados', styles['BulletText']))
    story.append(Paragraph('* Envio de mensajes', styles['BulletText']))
    story.append(Paragraph('* Scroll automatico', styles['BulletText']))

    # PrivateChat.vue
    story.append(Paragraph('PrivateChat.vue (10.8 KB) - Ruta: /chat/:displayName', styles['SectionTitle']))
    story.append(Paragraph('Chat privado entre dos usuarios.', styles['CustomBody']))
    story.append(Paragraph('Requiere autenticacion.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Conversacion 1 a 1', styles['BulletText']))
    story.append(Paragraph('* Historial de mensajes', styles['BulletText']))
    story.append(Paragraph('* Envio de mensajes', styles['BulletText']))
    story.append(Paragraph('* Marcado como leido', styles['BulletText']))

    # MessagesView.vue
    story.append(Paragraph('MessagesView.vue (6.3 KB) - Ruta: /messages', styles['SectionTitle']))
    story.append(Paragraph('Vista de bandeja de mensajes.', styles['CustomBody']))
    story.append(Paragraph('Requiere autenticacion.', styles['CustomBody']))
    story.append(Paragraph('Funcionalidades:', styles['CustomBody']))
    story.append(Paragraph('* Lista de conversaciones', styles['BulletText']))
    story.append(Paragraph('* Ultimo mensaje de cada conversacion', styles['BulletText']))
    story.append(Paragraph('* Indicador de no leidos', styles['BulletText']))
    story.append(Paragraph('* Busqueda de conversaciones', styles['BulletText']))

    story.append(PageBreak())

    # ========== 6. SERVICIOS ==========
    story.append(Paragraph('6. SERVICIOS (src/services/)', styles['ChapterTitle']))

    # supabase.js
    story.append(Paragraph('supabase.js', styles['SectionTitle']))
    story.append(Paragraph('Inicializacion del cliente Supabase.', styles['CustomBody']))
    story.append(Paragraph('Exporta: supabase (cliente)', styles['CustomBody']))
    story.append(Paragraph('Configuracion de URL y clave API publica.', styles['CustomBody']))

    # auth.js
    story.append(Paragraph('auth.js (3.2 KB)', styles['SectionTitle']))
    story.append(Paragraph('Servicios de autenticacion.', styles['CustomBody']))
    story.append(Paragraph('Funciones exportadas:', styles['CustomBody']))
    story.append(Paragraph('* register(email, password, displayName) - Registra nuevo usuario', styles['BulletText']))
    story.append(Paragraph('* login(email, password) - Inicia sesion', styles['BulletText']))
    story.append(Paragraph('* logout() - Cierra sesion', styles['BulletText']))
    story.append(Paragraph('* getCurrentUser() - Obtiene usuario actual', styles['BulletText']))
    story.append(Paragraph('* updateProfile(updates) - Actualiza metadata', styles['BulletText']))
    story.append(Paragraph('* subscribeToAuthChanges(callback) - Escucha cambios de auth', styles['BulletText']))

    # profiles.js
    story.append(Paragraph('profiles.js (10.4 KB)', styles['SectionTitle']))
    story.append(Paragraph('Gestion de perfiles de usuarios.', styles['CustomBody']))
    story.append(Paragraph('Constantes: RANGOS [Novato -> Hall of Fame]', styles['CustomBody']))
    story.append(Paragraph('Funciones exportadas:', styles['CustomBody']))
    story.append(Paragraph('* getProfile(userId) - Obtiene perfil por ID', styles['BulletText']))
    story.append(Paragraph('* getProfileByIdentifier(identifier) - Busca por ID o slug', styles['BulletText']))
    story.append(Paragraph('* getCurrentProfile() - Perfil del usuario actual', styles['BulletText']))
    story.append(Paragraph('* updateProfile(updates) - Actualiza perfil propio', styles['BulletText']))
    story.append(Paragraph('* createProfile(userId, profileData) - Crea nuevo perfil', styles['BulletText']))
    story.append(Paragraph('* searchProfiles(searchTerm, limit) - Busqueda', styles['BulletText']))
    story.append(Paragraph('* getProfiles(page, pageSize) - Lista paginada', styles['BulletText']))
    story.append(Paragraph('* getProfileStats(userId) - Estadisticas', styles['BulletText']))
    story.append(Paragraph('* createSlugFromDisplayName(name) - Genera slug', styles['BulletText']))
    story.append(Paragraph('* getRangoIndex(rango) - Indice del rango', styles['BulletText']))
    story.append(Paragraph('* getRangoByIndex(index) - Rango por indice', styles['BulletText']))

    story.append(PageBreak())

    # publications.js
    story.append(Paragraph('publications.js (8.6 KB)', styles['SectionTitle']))
    story.append(Paragraph('Gestion de publicaciones/posts.', styles['CustomBody']))
    story.append(Paragraph('Categorias: Articulo, Tutorial, Opinion, Review, Guia, Entrevista, Historia', styles['CustomBody']))
    story.append(Paragraph('Funciones exportadas:', styles['CustomBody']))
    story.append(Paragraph('* createPublication(data) - Crea publicacion', styles['BulletText']))
    story.append(Paragraph('* getPublications(page, pageSize, category) - Lista con filtros', styles['BulletText']))
    story.append(Paragraph('* getPublication(id) - Una publicacion', styles['BulletText']))
    story.append(Paragraph('* getPublicationsByUser(userId) - Por usuario', styles['BulletText']))
    story.append(Paragraph('* updatePublication(id, updates) - Actualiza', styles['BulletText']))
    story.append(Paragraph('* deletePublication(id) - Elimina', styles['BulletText']))
    story.append(Paragraph('* subscribeToPublicationsChanges() - Real-time', styles['BulletText']))
    story.append(Paragraph('* getPublicationCategoryName(key) - Nombre categoria', styles['BulletText']))
    story.append(Paragraph('* getPublicationCategoryIcon(key) - Icono categoria', styles['BulletText']))

    # comments.js
    story.append(Paragraph('comments.js (6.2 KB)', styles['SectionTitle']))
    story.append(Paragraph('Gestion de comentarios en publicaciones.', styles['CustomBody']))
    story.append(Paragraph('Funciones exportadas:', styles['CustomBody']))
    story.append(Paragraph('* createComment(publicationId, content) - Crea comentario', styles['BulletText']))
    story.append(Paragraph('* getComments(publicationId, page, pageSize) - Lista', styles['BulletText']))
    story.append(Paragraph('* updateComment(commentId, content) - Actualiza', styles['BulletText']))
    story.append(Paragraph('* deleteComment(commentId) - Elimina', styles['BulletText']))
    story.append(Paragraph('* getCommentsCount(publicationId) - Cuenta total', styles['BulletText']))

    # private-chat.js
    story.append(Paragraph('private-chat.js (11.5 KB)', styles['SectionTitle']))
    story.append(Paragraph('Servicios de mensajeria privada.', styles['CustomBody']))
    story.append(Paragraph('Funciones exportadas:', styles['CustomBody']))
    story.append(Paragraph('* getConversations() - Lista conversaciones', styles['BulletText']))
    story.append(Paragraph('* getMessages(conversationId) - Mensajes de conversacion', styles['BulletText']))
    story.append(Paragraph('* sendMessage(recipientId, content) - Envia mensaje', styles['BulletText']))
    story.append(Paragraph('* markAsRead(conversationId) - Marca como leido', styles['BulletText']))
    story.append(Paragraph('* getUnreadCount() - Cuenta no leidos', styles['BulletText']))
    story.append(Paragraph('* findConversation(userId) - Busca conversacion', styles['BulletText']))
    story.append(Paragraph('* subscribeToMessages(callback) - Real-time', styles['BulletText']))

    # storage.js
    story.append(Paragraph('storage.js (10.9 KB)', styles['SectionTitle']))
    story.append(Paragraph('Gestion de archivos en Supabase Storage.', styles['CustomBody']))
    story.append(Paragraph('Funciones exportadas:', styles['CustomBody']))
    story.append(Paragraph('* uploadAvatar(file, userId) - Sube avatar', styles['BulletText']))
    story.append(Paragraph('* uploadPublicationImage(file, publicationId) - Sube imagen', styles['BulletText']))
    story.append(Paragraph('* deleteFile(bucket, path) - Elimina archivo', styles['BulletText']))
    story.append(Paragraph('* getPublicUrl(bucket, path) - URL publica', styles['BulletText']))
    story.append(Paragraph('* getAvatarUrl(userId) - URL de avatar', styles['BulletText']))

    story.append(PageBreak())

    # ========== 7. COMPOSABLES ==========
    story.append(Paragraph('7. COMPOSABLES (src/composables/)', styles['ChapterTitle']))

    # useAuth.js
    story.append(Paragraph('useAuth.js (2.5 KB)', styles['SectionTitle']))
    story.append(Paragraph('Composable global para autenticacion reactiva.', styles['CustomBody']))
    story.append(Paragraph('Estado reactivo (refs):', styles['CustomBody']))
    story.append(Paragraph('* user - Usuario autenticado actual', styles['BulletText']))
    story.append(Paragraph('* loading - Estado de carga', styles['BulletText']))
    story.append(Paragraph('* initialized - Flag de inicializacion', styles['BulletText']))
    story.append(Paragraph('Propiedades computadas:', styles['CustomBody']))
    story.append(Paragraph('* isAuthenticated - Boolean de autenticacion', styles['BulletText']))
    story.append(Paragraph('* userEmail - Email del usuario', styles['BulletText']))
    story.append(Paragraph('* userDisplayName - Nombre para mostrar', styles['BulletText']))
    story.append(Paragraph('* userId - ID unico del usuario', styles['BulletText']))
    story.append(Paragraph('Metodos:', styles['CustomBody']))
    story.append(Paragraph('* initialize() - Inicializa estado de auth', styles['BulletText']))
    story.append(Paragraph('* refreshUser() - Refresca datos del usuario', styles['BulletText']))
    story.append(Paragraph('* clearUser() - Limpia estado al logout', styles['BulletText']))

    # useProfile.js
    story.append(Paragraph('useProfile.js (5.7 KB)', styles['SectionTitle']))
    story.append(Paragraph('Composable para gestion de perfiles.', styles['CustomBody']))
    story.append(Paragraph('useProfile() - Perfil del usuario actual:', styles['CustomBody']))
    story.append(Paragraph('* Estado: currentProfile, profileLoading', styles['BulletText']))
    story.append(Paragraph('* Datos: displayName, bio, avatarUrl, rango, isPro, profileId', styles['BulletText']))
    story.append(Paragraph('* Info rango: rangoIndex, rangoProgress', styles['BulletText']))
    story.append(Paragraph('* loadCurrentProfile() - Carga perfil actual', styles['BulletText']))
    story.append(Paragraph('* updateCurrentProfile(updates) - Actualiza', styles['BulletText']))
    story.append(Paragraph('* clearCurrentProfile() - Limpia', styles['BulletText']))
    story.append(Paragraph('useExternalProfile() - Perfiles de otros:', styles['CustomBody']))
    story.append(Paragraph('* Cache de perfiles cargados', styles['BulletText']))
    story.append(Paragraph('* loadProfile(userId) - Carga perfil externo', styles['BulletText']))
    story.append(Paragraph('* getCachedProfile(userId) - Obtiene del cache', styles['BulletText']))

    # useToast.js
    story.append(Paragraph('useToast.js (1.9 KB)', styles['SectionTitle']))
    story.append(Paragraph('Composable para sistema de notificaciones.', styles['CustomBody']))
    story.append(Paragraph('Estado:', styles['CustomBody']))
    story.append(Paragraph('* visible - Boolean de visibilidad', styles['BulletText']))
    story.append(Paragraph('* message - Mensaje a mostrar', styles['BulletText']))
    story.append(Paragraph('* type - Tipo: success, error, info, warning', styles['BulletText']))
    story.append(Paragraph('Metodos:', styles['CustomBody']))
    story.append(Paragraph('* showToast(message, type, duration) - Muestra toast', styles['BulletText']))
    story.append(Paragraph('* hideToast() - Oculta toast', styles['BulletText']))
    story.append(Paragraph('* showSuccess(message) - Toast de exito', styles['BulletText']))
    story.append(Paragraph('* showError(message) - Toast de error', styles['BulletText']))

    story.append(PageBreak())

    # ========== 8. ROUTER ==========
    story.append(Paragraph('8. ROUTER Y RUTAS (src/router/)', styles['ChapterTitle']))

    story.append(Paragraph('router.js (3.4 KB)', styles['SectionTitle']))
    story.append(Paragraph('Configuracion de Vue Router 4.', styles['CustomBody']))

    story.append(Paragraph('Rutas publicas:', styles['CustomBody']))
    story.append(Paragraph('* / -> Home.vue (Pagina de inicio)', styles['BulletText']))
    story.append(Paragraph('* /login -> Login.vue (Inicio de sesion)', styles['BulletText']))
    story.append(Paragraph('* /register -> Register.vue (Registro)', styles['BulletText']))
    story.append(Paragraph('* /chat -> PublicChat.vue (Chat publico)', styles['BulletText']))
    story.append(Paragraph('* /profile/:id? -> Profile.vue (Perfil publico)', styles['BulletText']))

    story.append(Paragraph('Rutas protegidas (requieren autenticacion):', styles['CustomBody']))
    story.append(Paragraph('* /publicaciones -> Publications.vue (Feed)', styles['BulletText']))
    story.append(Paragraph('* /settings -> Settings.vue (Configuracion)', styles['BulletText']))
    story.append(Paragraph('* /chat/:displayName -> PrivateChat.vue (Chat privado)', styles['BulletText']))
    story.append(Paragraph('* /messages -> MessagesView.vue (Bandeja)', styles['BulletText']))

    story.append(Paragraph('Navigation Guards:', styles['CustomBody']))
    story.append(Paragraph('* beforeEach - Verifica meta.requiresAuth', styles['BulletText']))
    story.append(Paragraph('* Redirige a /login si no autenticado', styles['BulletText']))
    story.append(Paragraph('* Redirige a perfil propio si /profile sin ID', styles['BulletText']))

    story.append(PageBreak())

    # ========== 9. ESTRUCTURA DE DATOS ==========
    story.append(Paragraph('9. ESTRUCTURA DE DATOS', styles['ChapterTitle']))

    story.append(Paragraph('User (Supabase Auth)', styles['SectionTitle']))
    user_struct = """
{
  id: UUID,
  email: string,
  user_metadata: {
    display_name: string
  }
}
"""
    for line in user_struct.strip().split('\n'):
        story.append(Paragraph(line, styles['CodeText']))

    story.append(Paragraph('Profile', styles['SectionTitle']))
    profile_struct = """
{
  id: UUID (same as auth user id),
  display_name: string,
  bio: string | null,
  avatar_url: string | null,
  rango: string (Novato...Hall of Fame),
  pro: boolean,
  created_at: timestamp
}
"""
    for line in profile_struct.strip().split('\n'):
        story.append(Paragraph(line, styles['CodeText']))

    story.append(Paragraph('Publication', styles['SectionTitle']))
    pub_struct = """
{
  id: UUID,
  user_id: UUID,
  title: string,
  content: string,
  category: string,
  image_url: string | null,
  created_at: timestamp,
  updated_at: timestamp
}
"""
    for line in pub_struct.strip().split('\n'):
        story.append(Paragraph(line, styles['CodeText']))

    story.append(Paragraph('Comment', styles['SectionTitle']))
    comment_struct = """
{
  id: UUID,
  publication_id: UUID,
  user_id: UUID,
  content: string,
  created_at: timestamp,
  updated_at: timestamp
}
"""
    for line in comment_struct.strip().split('\n'):
        story.append(Paragraph(line, styles['CodeText']))

    story.append(Paragraph('Message (Chat Privado)', styles['SectionTitle']))
    msg_struct = """
{
  id: UUID,
  sender_id: UUID,
  recipient_id: UUID,
  content: string,
  read: boolean,
  created_at: timestamp
}
"""
    for line in msg_struct.strip().split('\n'):
        story.append(Paragraph(line, styles['CodeText']))

    story.append(PageBreak())

    # ========== 10. CARACTERISTICAS ==========
    story.append(Paragraph('10. CARACTERISTICAS PRINCIPALES', styles['ChapterTitle']))

    story.append(Paragraph('Autenticacion', styles['SectionTitle']))
    story.append(Paragraph('* Registro con email/contrasena', styles['BulletText']))
    story.append(Paragraph('* Login/logout', styles['BulletText']))
    story.append(Paragraph('* Sesion persistente', styles['BulletText']))
    story.append(Paragraph('* Guards de rutas protegidas', styles['BulletText']))

    story.append(Paragraph('Sistema de Perfiles', styles['SectionTitle']))
    story.append(Paragraph('* 10 niveles de rango: Novato -> Hall of Fame', styles['BulletText']))
    story.append(Paragraph('* Avatar personalizado', styles['BulletText']))
    story.append(Paragraph('* Biografia editable', styles['BulletText']))
    story.append(Paragraph('* Estado PRO', styles['BulletText']))
    story.append(Paragraph('* Busqueda de usuarios', styles['BulletText']))

    story.append(Paragraph('Publicaciones', styles['SectionTitle']))
    story.append(Paragraph('* CRUD completo', styles['BulletText']))
    story.append(Paragraph('* 7 categorias de contenido', styles['BulletText']))
    story.append(Paragraph('* Soporte de imagenes', styles['BulletText']))
    story.append(Paragraph('* Paginacion y filtros', styles['BulletText']))

    story.append(Paragraph('Comentarios', styles['SectionTitle']))
    story.append(Paragraph('* Sistema completo de comentarios', styles['BulletText']))
    story.append(Paragraph('* Edicion y eliminacion', styles['BulletText']))
    story.append(Paragraph('* Control de permisos', styles['BulletText']))

    story.append(Paragraph('Mensajeria', styles['SectionTitle']))
    story.append(Paragraph('* Chat publico en tiempo real', styles['BulletText']))
    story.append(Paragraph('* Chat privado 1 a 1', styles['BulletText']))
    story.append(Paragraph('* Historial persistente', styles['BulletText']))
    story.append(Paragraph('* Indicadores de no leidos', styles['BulletText']))

    story.append(Paragraph('UI/UX', styles['SectionTitle']))
    story.append(Paragraph('* Tema oscuro por defecto', styles['BulletText']))
    story.append(Paragraph('* Diseno responsivo', styles['BulletText']))
    story.append(Paragraph('* Notificaciones toast', styles['BulletText']))
    story.append(Paragraph('* Tailwind CSS utilities', styles['BulletText']))

    # Construir PDF
    doc.build(story)
    print(f"PDF generado exitosamente: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_pdf()
