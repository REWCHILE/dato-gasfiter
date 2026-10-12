/**
 * DATO GASFITER - JAVASCRIPT PRINCIPAL
 * Optimizado para Nginx - Carga ultrarrápida sin dependencias
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Tarea Crítica Inmediata: Drawer móvil (< 10ms)
  initMobileDrawer();

  // 2. Programador de tareas diferidas para mantener el hilo principal siempre libre (< 50ms)
  const scheduleTask = typeof window.requestIdleCallback === 'function'
    ? (cb) => window.requestIdleCallback(cb, { timeout: 1500 })
    : (cb) => setTimeout(cb, 16);

  // Tarea diferida 1: Manejador de scroll eficiente
  scheduleTask(() => {
    initScrollEffects();
  });

  // Tarea diferida 2: Componentes interactivos bajo el pliegue (Acordeón, Tabs, Formularios)
  scheduleTask(() => {
    initFaqAccordion();
    initComunasTabs();
    initQuickQuote();
  });
});


/**
 * 1. NAVEGACIÓN MÓVIL (DRAWER DESLIZABLE DE IZQUIERDA A DERECHA)
 * Desliza de izquierda a derecha al abrir; colapsa de derecha a izquierda al cerrar.
 */
function initMobileDrawer() {
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerOverlay = document.getElementById('drawerOverlay');
  const drawerCloseBtn = document.getElementById('drawerCloseBtn');
  const drawerLinks = document.querySelectorAll('.drawer-nav-link, .drawer-sublink');

  if (!hamburgerBtn || !mobileDrawer || !drawerOverlay) return;

  function openDrawer() {
    mobileDrawer.classList.add('is-open');
    drawerOverlay.classList.add('is-active');
    hamburgerBtn.classList.add('is-active');
    hamburgerBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden'; // Evita scroll de fondo
  }

  function closeDrawer() {
    mobileDrawer.classList.remove('is-open');
    drawerOverlay.classList.remove('is-active');
    hamburgerBtn.classList.remove('is-active');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  hamburgerBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (mobileDrawer.classList.contains('is-open')) {
      closeDrawer();
    } else {
      openDrawer();
    }
  });

  if (drawerCloseBtn) {
    drawerCloseBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      closeDrawer();
    });
  }

  drawerOverlay.addEventListener('click', (e) => {
    e.stopPropagation();
    closeDrawer();
  });

  // Evita que clics dentro del drawer se propaguen accidentalmente al overlay
  mobileDrawer.addEventListener('click', (e) => {
    e.stopPropagation();
  });

  // Cerrar al hacer clic en enlaces del drawer
  drawerLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (href) {
        const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
        const linkPath = href.split('#')[0].replace(/\/$/, '') || '/';
        if (linkPath === currentPath && !href.includes('#')) {
          e.preventDefault();
          closeDrawer();
          return;
        }
      }
      closeDrawer();
    });
  });

  // Cerrar con tecla Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileDrawer.classList.contains('is-open')) {
      closeDrawer();
    }
  });
}

/**
 * 2. ACORDEÓN DE PREGUNTAS FRECUENTES (FAQ)
 */
function initFaqAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');

    if (!questionBtn || !answer) return;

    questionBtn.addEventListener('click', () => {
      const isOpen = item.classList.contains('is-open');

      // Opcional: cerrar los demás
      faqItems.forEach(other => {
        if (other !== item && other.classList.contains('is-open')) {
          other.classList.remove('is-open');
          const otherBtn = other.querySelector('.faq-question');
          const otherAns = other.querySelector('.faq-answer');
          if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
          if (otherAns) otherAns.style.maxHeight = null;
        }
      });

      if (isOpen) {
        item.classList.remove('is-open');
        questionBtn.setAttribute('aria-expanded', 'false');
        answer.style.maxHeight = null;
      } else {
        item.classList.add('is-open');
        questionBtn.setAttribute('aria-expanded', 'true');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });
}

/**
 * 3. TABS FILTRADORAS DE COMUNAS / ZONAS
 */
function initComunasTabs() {
  const tabBtns = document.querySelectorAll('.comuna-tab-btn');
  const comunaCards = document.querySelectorAll('.comuna-card');

  if (!tabBtns.length || !comunaCards.length) return;

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => {
        b.classList.remove('is-active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('is-active');
      btn.setAttribute('aria-selected', 'true');

      const filter = btn.getAttribute('data-filter');

      comunaCards.forEach(card => {
        const zone = card.getAttribute('data-zone');
        if (filter === 'all' || zone === filter) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/**
 * 4. GESTIÓN EFICIENTE DE SCROLL (HEADER STICKY + BOTÓN VOLVER ARRIBA)
 * Optimizado contra Forced Reflow y Tareas Largas (0 layout thrashing)
 */
function initScrollEffects() {
  const header = document.querySelector('.site-header');
  const backToTopBtn = document.getElementById('backToTopBtn');
  if (!header && !backToTopBtn) return;

  let isHeaderScrolled = false;
  let isBackToTopVisible = false;
  let ticking = false;

  function updateScrollState() {
    const scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;

    // Header sticky styling
    if (header) {
      const shouldBeScrolled = scrollY > 20;
      if (shouldBeScrolled !== isHeaderScrolled) {
        isHeaderScrolled = shouldBeScrolled;
        if (shouldBeScrolled) {
          header.classList.add('scrolled');
        } else {
          header.classList.remove('scrolled');
        }
      }
    }

    // Botón volver arriba
    if (backToTopBtn) {
      const shouldShowBtn = scrollY > 250;
      if (shouldShowBtn !== isBackToTopVisible) {
        isBackToTopVisible = shouldShowBtn;
        if (shouldShowBtn) {
          backToTopBtn.classList.add('is-visible');
        } else {
          backToTopBtn.classList.remove('is-visible');
        }
      }
    }

    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(updateScrollState);
      ticking = true;
    }
  }

  // Listener pasivo para máxima fluidez a 60/120 fps
  window.addEventListener('scroll', onScroll, { passive: true });

  // Solo sincroniza si la página se carga con scroll previo, tras completarse la carga
  window.addEventListener('load', () => {
    if ((window.pageYOffset || document.documentElement.scrollTop || 0) > 20) {
      window.requestAnimationFrame(updateScrollState);
    }
  }, { passive: true });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
}

/**
 * 5. COTIZADOR RÁPIDO VÍA WHATSAPP
 */
function initQuickQuote() {
  const forms = document.querySelectorAll('.quick-quote-form');

  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const service = form.querySelector('[name="service"]')?.value || 'Servicio General';
      const zone = form.querySelector('[name="zone"]')?.value || 'Santiago';
      const name = form.querySelector('[name="name"]')?.value || 'Cliente';
      const detail = form.querySelector('[name="detail"]')?.value || 'Necesito asistencia urgente.';

      const text = `Hola *DATO GASFITER*, necesito cotización urgente:
- *Servicio:* ${service}
- *Comuna/Ciudad:* ${zone}
- *Nombre:* ${name}
- *Detalle:* ${detail}

¿Tienen disponibilidad de visita técnica?`;

      const encoded = encodeURIComponent(text);
      const url = `https://wa.me/56932237072?text=${encoded}`;

      window.open(url, '_blank', 'noopener,noreferrer');
    });
  });
}

/**
 * 6. PROTOCOLO WEBMCP (WEB MODEL CONTEXT PROTOCOL) & NAVEGACIÓN AGÉNTICA (4/4)
 * Registra herramientas programáticas para agentes de IA (Google Gemini, OpenAI Operator, Claude Computer Use)
 */
function initWebMCP() {
  const modelContext = (typeof document !== 'undefined' && document.modelContext) ||
                       (typeof navigator !== 'undefined' && navigator.modelContext);

  if (modelContext && typeof modelContext.registerTool === 'function') {
    try {
      // Herramienta 1: Cotizar y solicitar gasfiter
      modelContext.registerTool({
        name: 'solicitar_gasfiter',
        title: 'Solicitud y Cotización de Gasfiter Certificado SEC',
        description: 'Permite a agentes de IA solicitar asistencia o cotización de gasfitería autorizada SEC a domicilio en Santiago y Viña del Mar.',
        inputSchema: {
          type: 'object',
          properties: {
            servicio: {
              type: 'string',
              description: 'Tipo de servicio requerido: reparacion-calefont, deteccion-fugas, destape-alcantarillado, gas-sec, informe-tecnico o emergencia.'
            },
            comuna: {
              type: 'string',
              description: 'Comuna o ciudad del cliente en Chile (ej. Santiago Centro, Providencia, Las Condes, Vitacura, Viña del Mar).'
            },
            nombre: {
              type: 'string',
              description: 'Nombre del cliente solicitante.'
            },
            detalle: {
              type: 'string',
              description: 'Detalle o descripción de la falla técnica o urgencia.'
            }
          },
          required: ['servicio', 'comuna'],
          additionalProperties: false
        },
        async execute(params) {
          const s = (params && params.servicio) || 'Gasfitería General';
          const c = (params && params.comuna) || 'Santiago';
          const n = (params && params.nombre) || 'Cliente';
          const d = (params && params.detalle) || 'Asistencia técnica solicitada vía IA.';
          const waUrl = `https://wa.me/56932237072?text=${encodeURIComponent('Hola DATO GASFITER, necesito asistencia: ' + s + ' en ' + c + ' (' + n + '): ' + d)}`;
          return {
            status: 'success',
            proveedor: 'DATO GASFITER',
            certificacion: 'Instalador Certificado SEC Clase 3 / Gas y Agua',
            telefono_contacto: '+56932237072',
            tiempo_llegada_estimado: '30 a 45 minutos',
            enlace_contacto_inmediato: waUrl,
            cobertura: ['Santiago Centro', 'Providencia', 'Las Condes', 'Vitacura', 'Ñuñoa', 'La Reina', 'Lo Barnechea', 'San Miguel', 'La Florida', 'Maipú', 'Puente Alto', 'Viña del Mar']
          };
        }
      });

      // Herramienta 2: Información institucional y cobertura
      modelContext.registerTool({
        name: 'obtener_cobertura_gasfiter',
        title: 'Obtener Zonas de Cobertura y Horarios de Urgencia',
        description: 'Consulta las comunas atendidas y disponibilidad de atención técnica de DATO GASFITER.',
        inputSchema: {
          type: 'object',
          properties: {},
          additionalProperties: false
        },
        async execute() {
          return {
            status: 'success',
            empresa: 'DATO GASFITER',
            telefono_urgencias: '+56932237072',
            horario: 'Lunes a Domingo • Turnos de Emergencia Activos',
            tiempo_promedio_llegada: '30 a 45 minutos',
            ciudades: ['Santiago (Todas las comunas)', 'Viña del Mar', 'Valparaíso', 'Concón']
          };
        }
      });
    } catch (e) {
      // Manejo seguro en entornos donde la API aún es experimental
    }
  }
}

// Registro inmediato y reintento en DOMContentLoaded para máxima compatibilidad con Lighthouse
initWebMCP();
document.addEventListener('DOMContentLoaded', initWebMCP);



