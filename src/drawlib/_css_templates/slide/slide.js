/**
 * Drawlib Presentation Deck Engine (Vanilla JS)
 */

(function () {
  'use strict';

  const STAGE_WIDTH = 1920;
  const STAGE_HEIGHT = 1080;

  let currentSlide = 1;
  let totalSlides = 0;
  let isOverviewOpen = false;

  const stage = document.querySelector('.presentation-stage');
  const slides = document.querySelectorAll('.slide');
  totalSlides = slides.length;

  /**
   * Automatically calculate scaling factor to fit viewport while maintaining 16:9 aspect ratio.
   */
  function updateScale() {
    if (!stage) return;
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    const scaleX = windowWidth / STAGE_WIDTH;
    const scaleY = windowHeight / STAGE_HEIGHT;
    const scale = Math.min(scaleX, scaleY);

    stage.style.transform = `scale(${scale})`;
  }

  /**
   * Switch to specified slide index (1-based).
   */
  function goToSlide(index) {
    if (index < 1) index = 1;
    if (index > totalSlides) index = totalSlides;

    currentSlide = index;
    slides.forEach((slide, idx) => {
      if (idx + 1 === currentSlide) {
        slide.classList.add('active');
      } else {
        slide.classList.remove('active');
      }
    });

    // Update URL hash
    history.replaceState(null, '', `#${currentSlide}`);

    // Update overview thumbs
    document.querySelectorAll('.overview-thumb').forEach((thumb, idx) => {
      if (idx + 1 === currentSlide) {
        thumb.classList.add('current');
      } else {
        thumb.classList.remove('current');
      }
    });
  }

  function nextSlide() {
    if (currentSlide < totalSlides) {
      goToSlide(currentSlide + 1);
    }
  }

  function prevSlide() {
    if (currentSlide > 1) {
      goToSlide(currentSlide - 1);
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.warn(`Fullscreen error: ${err.message}`);
      });
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  }

  function toggleOverview() {
    const modal = document.querySelector('.overview-modal');
    if (!modal) return;
    isOverviewOpen = !isOverviewOpen;
    if (isOverviewOpen) {
      modal.classList.add('active');
    } else {
      modal.classList.remove('active');
    }
  }

  function setupKeyboard() {
    window.addEventListener('keydown', (e) => {
      if (isOverviewOpen) {
        if (e.key === 'Escape' || e.key === 'o' || e.key === 'O') {
          toggleOverview();
        }
        return;
      }

      switch (e.key) {
        case 'ArrowRight':
        case 'ArrowDown':
        case ' ':
        case 'PageDown':
          e.preventDefault();
          nextSlide();
          break;
        case 'ArrowLeft':
        case 'ArrowUp':
        case 'PageUp':
        case 'Backspace':
          e.preventDefault();
          prevSlide();
          break;
        case 'Home':
          e.preventDefault();
          goToSlide(1);
          break;
        case 'End':
          e.preventDefault();
          goToSlide(totalSlides);
          break;
        case 'f':
        case 'F':
          e.preventDefault();
          toggleFullscreen();
          break;
        case 'o':
        case 'O':
        case 'Escape':
          e.preventDefault();
          toggleOverview();
          break;
      }
    });
  }

  function setupControls() {
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const btnOverview = document.getElementById('btn-overview');
    const btnFullscreen = document.getElementById('btn-fullscreen');

    if (btnPrev) btnPrev.addEventListener('click', prevSlide);
    if (btnNext) btnNext.addEventListener('click', nextSlide);
    if (btnOverview) btnOverview.addEventListener('click', toggleOverview);
    if (btnFullscreen) btnFullscreen.addEventListener('click', toggleFullscreen);

    // Close overview on click outside
    const modal = document.querySelector('.overview-modal');
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          toggleOverview();
        }
      });
    }

    // Overview thumbs click
    document.querySelectorAll('.overview-thumb').forEach((thumb, idx) => {
      thumb.addEventListener('click', () => {
        goToSlide(idx + 1);
        toggleOverview();
      });
    });
  }

  function initFromHash() {
    const hash = window.location.hash;
    if (hash && hash.startsWith('#')) {
      const parsed = parseInt(hash.substring(1), 10);
      if (!isNaN(parsed) && parsed >= 1 && parsed <= totalSlides) {
        currentSlide = parsed;
      }
    }
    goToSlide(currentSlide);
  }

  // Lifecycle initialization
  window.addEventListener('resize', updateScale);
  window.addEventListener('DOMContentLoaded', () => {
    updateScale();
    setupKeyboard();
    setupControls();
    initFromHash();
  });

  // Re-scale immediately
  updateScale();
})();
