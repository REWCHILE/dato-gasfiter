/**
 * DATO GASFITER - JAVASCRIPT PRINCIPAL
 * Optimizado para Nginx - Carga ultrarrápida sin dependencias
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileDrawer();
  initFaqAccordion();
  initComunasTabs();
  initHeaderScroll();
  initQuickQuote();
  initScrollToTop();
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
    drawerCloseBtn.addEventListener('click', closeDrawer);
  }

  drawerOverlay.addEventListener('click', closeDrawer);

  // Cerrar al hacer clic en enlaces del drawer
  drawerLinks.forEach(link => {
    link.addEventListener('click', closeDrawer);
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
 * 4. HEADER TRANSIENT ON SCROLL
 */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }, { passive: true });
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
 * 6. BOTÓN VOLVER ARRIBA (SCROLL TO TOP)
 */
function initScrollToTop() {
  const btn = document.getElementById('backToTopBtn');
  if (!btn) return;

  const toggleVisibility = () => {
    // Aparece cuando el usuario scrollea hacia abajo (más de 300px)
    if (window.scrollY > 300) {
      btn.classList.add('is-visible');
    } else {
      btn.classList.remove('is-visible');
    }
  };

  window.addEventListener('scroll', toggleVisibility, { passive: true });
  toggleVisibility();

  btn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
} else {
      btn.classList.remove('is-visible');
    }
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

