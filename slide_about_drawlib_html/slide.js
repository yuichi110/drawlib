/**
 * Drawlib Presentation Deck Engine (Vanilla JS)
 * Includes interactive <canvas> APNG / Animated WebP player with frame-level pause control.
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

  // Map of slide index (1-based) -> array of AnimPlayer instances on that slide
  const slideAnimPlayers = new Map();

  // =========================================================================
  // CRC32 Table & Helper for Vanilla JS APNG Fallback Decoder
  // =========================================================================
  const CRC_TABLE = (function () {
    const table = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) {
        c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
      }
      table[n] = c >>> 0;
    }
    return table;
  })();

  function crc32(bytes, start, length) {
    let c = 0xffffffff;
    const end = start + length;
    for (let i = start; i < end; i++) {
      c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
    }
    return (c ^ 0xffffffff) >>> 0;
  }

  function makeChunk(typeStr, dataBytes) {
    const len = dataBytes.length;
    const out = new Uint8Array(12 + len);
    const dv = new DataView(out.buffer);
    dv.setUint32(0, len, false);
    for (let i = 0; i < 4; i++) {
      out[4 + i] = typeStr.charCodeAt(i);
    }
    out.set(dataBytes, 8);
    const crc = crc32(out, 4, 4 + len);
    dv.setUint32(8 + len, crc, false);
    return out;
  }

  /**
   * Parse APNG binary buffer in pure JS when ImageDecoder is unavailable.
   */
  async function parseApngBuffer(buffer) {
    const bytes = new Uint8Array(buffer);
    const dv = new DataView(buffer);
    const PNG_SIG = new Uint8Array([137, 80, 78, 71, 13, 10, 26, 10]);

    let offset = 8;
    let canvasWidth = 0;
    let canvasHeight = 0;
    let ihdrData = null;
    const preIdatChunks = [];
    const postIdatChunks = [];
    const rawFrames = [];
    let currentFcTL = null;
    let seenIDAT = false;
    let isAnimated = false;

    while (offset + 8 <= bytes.length) {
      const length = dv.getUint32(offset, false);
      const type = String.fromCharCode(
        bytes[offset + 4],
        bytes[offset + 5],
        bytes[offset + 6],
        bytes[offset + 7]
      );
      const dataStart = offset + 8;
      const dataEnd = dataStart + length;
      if (dataEnd + 4 > bytes.length) break;
      const chunkData = bytes.subarray(dataStart, dataEnd);
      const fullChunk = bytes.subarray(offset, dataEnd + 4);

      if (type === 'IHDR') {
        canvasWidth = dv.getUint32(dataStart, false);
        canvasHeight = dv.getUint32(dataStart + 4, false);
        ihdrData = new Uint8Array(chunkData);
      } else if (type === 'acTL') {
        isAnimated = true;
      } else if (type === 'fcTL') {
        const fWidth = dv.getUint32(dataStart + 4, false);
        const fHeight = dv.getUint32(dataStart + 8, false);
        const xOffset = dv.getUint32(dataStart + 12, false);
        const yOffset = dv.getUint32(dataStart + 16, false);
        const delayNum = dv.getUint16(dataStart + 20, false);
        let delayDen = dv.getUint16(dataStart + 22, false);
        if (delayDen === 0) delayDen = 100;
        const disposeOp = bytes[dataStart + 24];
        const blendOp = bytes[dataStart + 25];
        const durationMs = Math.max(10, Math.round((delayNum / delayDen) * 1000));
        currentFcTL = {
          width: fWidth,
          height: fHeight,
          x: xOffset,
          y: yOffset,
          duration: durationMs,
          disposeOp: disposeOp,
          blendOp: blendOp,
          dataParts: []
        };
        rawFrames.push(currentFcTL);
      } else if (type === 'IDAT') {
        seenIDAT = true;
        if (currentFcTL) {
          currentFcTL.dataParts.push(chunkData);
        }
      } else if (type === 'fdAT') {
        if (currentFcTL && length > 4) {
          currentFcTL.dataParts.push(chunkData.subarray(4));
        }
      } else if (type === 'IEND') {
        break;
      } else {
        if (!seenIDAT) {
          preIdatChunks.push(fullChunk);
        } else {
          postIdatChunks.push(fullChunk);
        }
      }
      offset = dataEnd + 4;
    }

    if (!isAnimated || rawFrames.length === 0 || !ihdrData) {
      const blob = new Blob([buffer], { type: 'image/png' });
      const bmp = await createImageBitmap(blob);
      return [{ bitmap: bmp, duration: 100, width: bmp.width, height: bmp.height }];
    }

    const iendChunk = makeChunk('IEND', new Uint8Array(0));
    const compCanvas = document.createElement('canvas');
    compCanvas.width = canvasWidth;
    compCanvas.height = canvasHeight;
    const compCtx = compCanvas.getContext('2d');

    const decodedFrames = [];
    for (let i = 0; i < rawFrames.length; i++) {
      const rf = rawFrames[i];
      if (rf.dataParts.length === 0) continue;

      const fIhdr = new Uint8Array(ihdrData);
      const fIhdrDv = new DataView(fIhdr.buffer);
      fIhdrDv.setUint32(0, rf.width, false);
      fIhdrDv.setUint32(4, rf.height, false);
      const ihdrChunk = makeChunk('IHDR', fIhdr);
      const idatChunks = rf.dataParts.map(part => makeChunk('IDAT', part));

      let totalLen = PNG_SIG.length + ihdrChunk.length + iendChunk.length;
      preIdatChunks.forEach(c => { totalLen += c.length; });
      idatChunks.forEach(c => { totalLen += c.length; });
      postIdatChunks.forEach(c => { totalLen += c.length; });

      const framePng = new Uint8Array(totalLen);
      let pos = 0;
      framePng.set(PNG_SIG, pos); pos += PNG_SIG.length;
      framePng.set(ihdrChunk, pos); pos += ihdrChunk.length;
      preIdatChunks.forEach(c => { framePng.set(c, pos); pos += c.length; });
      idatChunks.forEach(c => { framePng.set(c, pos); pos += c.length; });
      postIdatChunks.forEach(c => { framePng.set(c, pos); pos += c.length; });
      framePng.set(iendChunk, pos);

      const blob = new Blob([framePng], { type: 'image/png' });
      const subBmp = await createImageBitmap(blob);

      let prevImageData = null;
      if (rf.disposeOp === 2) {
        prevImageData = compCtx.getImageData(rf.x, rf.y, rf.width, rf.height);
      }

      if (rf.blendOp === 0) {
        compCtx.clearRect(rf.x, rf.y, rf.width, rf.height);
      }
      compCtx.drawImage(subBmp, rf.x, rf.y);
      subBmp.close();

      const fullBmp = await createImageBitmap(compCanvas);
      decodedFrames.push({
        bitmap: fullBmp,
        duration: rf.duration,
        width: canvasWidth,
        height: canvasHeight
      });

      if (rf.disposeOp === 1) {
        compCtx.clearRect(rf.x, rf.y, rf.width, rf.height);
      } else if (rf.disposeOp === 2 && prevImageData) {
        compCtx.putImageData(prevImageData, rf.x, rf.y);
      }
    }

    return decodedFrames;
  }

  /**
   * Load static first frame via <img> when fetch() is blocked (e.g., file:// protocol).
   */
  function loadStaticImageFrame(src) {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => {
        resolve([{
          bitmap: img,
          duration: 100,
          width: img.naturalWidth || img.width || 800,
          height: img.naturalHeight || img.height || 600
        }]);
      };
      img.onerror = () => {
        resolve([]);
      };
      img.src = src;
    });
  }

  /**
   * Decode all frames from an APNG or Animated WebP asset URL.
   */
  async function decodeAnimationFrames(src) {
    const lower = src.toLowerCase();
    const mimeType = lower.endsWith('.webp') ? 'image/webp' : 'image/png';

    let buffer;
    try {
      const response = await fetch(src);
      if (!response.ok) {
        return await loadStaticImageFrame(src);
      }
      buffer = await response.arrayBuffer();
    } catch (_err) {
      // Fallback for file:// protocol (e.g., headless PDF export)
      return await loadStaticImageFrame(src);
    }

    // 1. Primary path: WebCodecs ImageDecoder API (Chrome, Edge, Firefox)
    if (typeof window.ImageDecoder === 'function') {
      try {
        const decoder = new window.ImageDecoder({ data: buffer, type: mimeType });
        await decoder.tracks.ready;
        const track = decoder.tracks.selectedTrack;
        const frameCount = track ? track.frameCount : 1;
        const frames = [];

        for (let i = 0; i < frameCount; i++) {
          const result = await decoder.decode({ frameIndex: i });
          const vf = result.image;
          // VideoFrame.duration is in microseconds; convert to milliseconds
          const durationMs = vf.duration ? Math.max(10, Math.round(vf.duration / 1000)) : 100;
          const bmp = await createImageBitmap(vf);
          vf.close();
          frames.push({
            bitmap: bmp,
            duration: durationMs,
            width: bmp.width,
            height: bmp.height
          });
        }
        decoder.close();
        if (frames.length > 0) {
          return frames;
        }
      } catch (_decodeErr) {
        // Fall through to pure JS APNG parser or static image
      }
    }

    // 2. Secondary path: Pure JS APNG parser
    if (mimeType === 'image/png') {
      try {
        return await parseApngBuffer(buffer);
      } catch (_apngErr) {
        return await loadStaticImageFrame(src);
      }
    }

    return await loadStaticImageFrame(src);
  }

  // =========================================================================
  // Interactive <canvas> Animation Player State Machine
  // =========================================================================
  function createAnimPlayer(container) {
    const canvas = container.querySelector('.drawlib-anim-canvas');
    const badge = container.querySelector('.anim-play-badge');
    if (!canvas) return null;

    const ctx = canvas.getContext('2d');
    const src = canvas.getAttribute('data-src') || '';
    const trigger = (container.getAttribute('data-anim-trigger') || 'auto').toLowerCase();
    const loopMode = (container.getAttribute('data-anim-loop') || 'infinite').toLowerCase();
    const rawPause = container.getAttribute('data-anim-pause') || '';
    const pauseFrames = new Set(
      rawPause
        .split(',')
        .map(s => parseInt(s.trim(), 10))
        .filter(n => !isNaN(n) && n >= 0)
    );

    let frames = [];
    let currentFrame = 0;
    let state = 'READY'; // 'READY' | 'PLAYING' | 'PAUSED' | 'ENDED'
    let timerId = null;

    function clearTimer() {
      if (timerId !== null) {
        clearTimeout(timerId);
        timerId = null;
      }
    }

    function setState(newState) {
      state = newState;
      container.classList.remove('playing', 'paused', 'ended');
      if (newState === 'PLAYING') {
        container.classList.add('playing');
        if (badge) badge.setAttribute('title', 'Click to pause animation');
      } else if (newState === 'PAUSED') {
        container.classList.add('paused');
        if (badge) badge.setAttribute('title', `Paused at frame ${currentFrame} — click to continue`);
      } else if (newState === 'ENDED') {
        container.classList.add('ended');
        if (badge) badge.setAttribute('title', 'Click to replay animation');
      } else {
        if (badge) badge.setAttribute('title', 'Click to play animation');
      }
    }

    function drawFrame(index) {
      if (!frames.length) return;
      const clamped = Math.max(0, Math.min(index, frames.length - 1));
      currentFrame = clamped;
      const f = frames[clamped];
      if (canvas.width !== f.width || canvas.height !== f.height) {
        canvas.width = f.width;
        canvas.height = f.height;
      }
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(f.bitmap, 0, 0);
    }

    function stepToFrame(nextIndex) {
      clearTimer();
      if (!frames.length) return;

      drawFrame(nextIndex);
      const isLastFrame = currentFrame >= frames.length - 1;

      // Check if we reached the final frame in 'once' mode
      if (isLastFrame && loopMode === 'once') {
        setState('ENDED');
        return;
      }

      // Check if this frame is a designated pause point
      if (pauseFrames.has(currentFrame)) {
        setState('PAUSED');
        return;
      }

      // Otherwise schedule the next frame after current frame's duration
      const delay = frames[currentFrame].duration || 100;
      timerId = setTimeout(() => {
        if (state !== 'PLAYING') return;
        const upcoming = isLastFrame ? 0 : currentFrame + 1;
        stepToFrame(upcoming);
      }, delay);
    }

    function startFromBeginning() {
      clearTimer();
      if (!frames.length) return;
      setState('PLAYING');
      stepToFrame(0);
    }

    function advanceFromWait() {
      clearTimer();
      if (!frames.length) return;
      if (frames.length === 1) {
        drawFrame(0);
        if (loopMode === 'once') {
          setState('ENDED');
        }
        return;
      }
      setState('PLAYING');
      const nextIdx = (currentFrame + 1) < frames.length ? (currentFrame + 1) : 0;
      stepToFrame(nextIdx);
    }

    function handleClick(e) {
      if (e) {
        e.stopPropagation();
      }
      if (!frames.length) return;

      if (state === 'READY') {
        // Frame 0 is already displayed; advance immediately to Frame 1
        advanceFromWait();
      } else if (state === 'PAUSED') {
        // Resume from the frame after the paused frame
        advanceFromWait();
      } else if (state === 'ENDED') {
        // Replay from Frame 0
        startFromBeginning();
      } else if (state === 'PLAYING') {
        // Allow manual pause on click while playing
        clearTimer();
        setState('PAUSED');
      }
    }

    function onSlideEnter() {
      clearTimer();
      if (!frames.length) return;
      drawFrame(0);
      if (trigger === 'auto') {
        startFromBeginning();
      } else {
        setState('READY');
      }
    }

    function onSlideLeave() {
      clearTimer();
      if (!frames.length) return;
      drawFrame(0);
      setState('READY');
    }

    container.addEventListener('click', handleClick);

    const readyPromise = decodeAnimationFrames(src).then(decoded => {
      frames = decoded;
      if (frames.length > 0) {
        drawFrame(0);
        // If this container belongs to the currently active slide, apply enter state
        const parentSlide = container.closest('.slide');
        if (parentSlide && parentSlide.classList.contains('active')) {
          onSlideEnter();
        } else {
          setState('READY');
        }
      }
    });

    return {
      readyPromise,
      onSlideEnter,
      onSlideLeave,
      handleClick,
      getState: () => state
    };
  }

  function syncOverviewCanvases() {
    const thumbs = document.querySelectorAll('.overview-thumb');
    thumbs.forEach((thumb, idx) => {
      const origSlide = slides[idx];
      if (!origSlide) return;
      const origCanvases = origSlide.querySelectorAll('canvas.drawlib-anim-canvas');
      const cloneCanvases = thumb.querySelectorAll('canvas.drawlib-anim-canvas');
      origCanvases.forEach((origCanvas, cIdx) => {
        const cloneCanvas = cloneCanvases[cIdx];
        if (cloneCanvas && origCanvas.width > 0 && origCanvas.height > 0) {
          cloneCanvas.width = origCanvas.width;
          cloneCanvas.height = origCanvas.height;
          const ctx = cloneCanvas.getContext('2d');
          if (ctx) {
            ctx.clearRect(0, 0, cloneCanvas.width, cloneCanvas.height);
            ctx.drawImage(origCanvas, 0, 0);
          }
        }
      });
    });
  }

  function updateOverviewScale() {
    const thumbs = document.querySelectorAll('.overview-thumb');
    thumbs.forEach(thumb => {
      const thumbStage = thumb.querySelector('.overview-thumb-stage');
      if (!thumbStage) return;
      const w = thumb.clientWidth;
      if (w > 0) {
        const scale = w / STAGE_WIDTH;
        thumbStage.style.transform = `scale(${scale})`;
      }
    });
  }

  function initOverviewThumbs() {
    const thumbs = document.querySelectorAll('.overview-thumb');
    thumbs.forEach((thumb, idx) => {
      const origSlide = slides[idx];
      if (!origSlide) return;
      const slideBody = origSlide.querySelector('.slide-body');
      if (!slideBody) return;

      const thumbStage = document.createElement('div');
      thumbStage.className = 'overview-thumb-stage';

      const bodyClone = slideBody.cloneNode(true);
      const idSuffix = `-ov-${idx + 1}`;
      bodyClone.querySelectorAll('[id]').forEach(el => {
        const oldId = el.getAttribute('id');
        if (oldId) {
          el.setAttribute('id', oldId + idSuffix);
        }
      });
      bodyClone.querySelectorAll('*').forEach(el => {
        for (let i = 0; i < el.attributes.length; i++) {
          const attr = el.attributes[i];
          if (!attr.value) continue;
          if (attr.value.includes('url(#')) {
            attr.value = attr.value.replace(/url\(#([^)]+)\)/g, `url(#$1${idSuffix})`);
          } else if (
            (attr.name === 'href' || attr.name === 'xlink:href') &&
            attr.value.startsWith('#')
          ) {
            attr.value = attr.value + idSuffix;
          }
        }
      });

      thumbStage.appendChild(bodyClone);
      thumb.insertBefore(thumbStage, thumb.firstChild);
      thumb.classList.add('has-preview');
    });
  }

  function initAllAnimPlayers() {
    const readyPromises = [];
    slides.forEach((slide, idx) => {
      const slideIdx = idx + 1;
      const containers = slide.querySelectorAll('.drawlib-anim-container');
      const players = [];
      containers.forEach(container => {
        const player = createAnimPlayer(container);
        if (player) {
          players.push(player);
          readyPromises.push(player.readyPromise);
        }
      });
      if (players.length > 0) {
        slideAnimPlayers.set(slideIdx, players);
      }
    });
    window.__drawlibAnimReady = Promise.all(readyPromises).then(() => {
      syncOverviewCanvases();
    });
  }

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
    if (isOverviewOpen) {
      updateOverviewScale();
    }
  }

  /**
   * Switch to specified slide index (1-based).
   */
  function goToSlide(index) {
    if (index < 1) index = 1;
    if (index > totalSlides) index = totalSlides;

    const prevSlideIdx = currentSlide;
    currentSlide = index;

    if (prevSlideIdx !== currentSlide && slideAnimPlayers.has(prevSlideIdx)) {
      slideAnimPlayers.get(prevSlideIdx).forEach(p => p.onSlideLeave());
    }

    slides.forEach((slide, idx) => {
      if (idx + 1 === currentSlide) {
        slide.classList.add('active');
      } else {
        slide.classList.remove('active');
      }
    });

    if (slideAnimPlayers.has(currentSlide)) {
      slideAnimPlayers.get(currentSlide).forEach(p => p.onSlideEnter());
    }

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
      syncOverviewCanvases();
      updateOverviewScale();
    } else {
      modal.classList.remove('active');
    }
  }

  function setupKeyboard() {
    window.addEventListener('keydown', (e) => {
      // Do not intercept browser shortcuts (e.g. Cmd+F / Ctrl+F for Find, Cmd+R for Reload)
      if (e.metaKey || e.ctrlKey || e.altKey) {
        return;
      }

      // Do not intercept keys when typing in input or textarea elements
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
        return;
      }

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
    initOverviewThumbs();
    initAllAnimPlayers();
    setupKeyboard();
    setupControls();
    initFromHash();
  });

  // Re-scale immediately
  updateScale();
})();
