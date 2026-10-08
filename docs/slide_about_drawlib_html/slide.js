/**
 * Drawlib Presentation Deck Engine (Vanilla JS)
 * Includes interactive <canvas> APNG / Animated WebP player with frame-level pause control.
 */

(function () {
  'use strict';

  const STAGE_WIDTH = 1920;
  const STAGE_HEIGHT = 1080;

  const urlParams = new URLSearchParams(window.location.search);
  const isPresenterMode = urlParams.get('presenter') === '1';

  let currentSlide = 1;
  let totalSlides = 0;
  let isOverviewOpen = false;
  let presenterWindow = null;
  let notesFontSizeRem = 1.15;

  const stage = document.querySelector('.presentation-stage');
  const slides = document.querySelectorAll('.slide');
  totalSlides = slides.length;

  // Map of slide index (1-based) -> array of AnimPlayer instances on that slide
  const slideAnimPlayers = new Map();

  // =========================================================================
  // Cross-Window Synchronization (BroadcastChannel + postMessage fallback)
  // =========================================================================
  const SYNC_CHANNEL_NAME = 'drawlib_slide_sync';
  const syncChannel = typeof window.BroadcastChannel === 'function'
    ? new window.BroadcastChannel(SYNC_CHANNEL_NAME)
    : null;
  const processedMsgIds = new Set();

  function sendSyncMessage(payload) {
    const msg = Object.assign({}, payload, {
      _drawlibSync: true,
      _msgId: `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
    });
    processedMsgIds.add(msg._msgId);

    if (syncChannel) {
      try {
        syncChannel.postMessage(msg);
      } catch (_err) {
        // Ignore BroadcastChannel errors
      }
    }

    try {
      if (isPresenterMode && window.opener && !window.opener.closed) {
        window.opener.postMessage(msg, '*');
      } else if (!isPresenterMode && presenterWindow && !presenterWindow.closed) {
        presenterWindow.postMessage(msg, '*');
      }
    } catch (_err) {
      // Ignore cross-origin / closed window errors
    }
  }

  function handleSyncMessage(data) {
    if (!data || !data._drawlibSync) return;
    if (data._msgId) {
      if (processedMsgIds.has(data._msgId)) return;
      processedMsgIds.add(data._msgId);
    }

    if (data.type === 'slide_change' && typeof data.slide === 'number') {
      if (data.slide !== currentSlide) {
        goToSlide(data.slide, true);
      }
    } else if (data.type === 'anim_trigger' && typeof data.slide === 'number') {
      if (data.slide !== currentSlide) {
        goToSlide(data.slide, true);
      }
      const players = slideAnimPlayers.get(data.slide);
      if (players && players.length > 0) {
        if (typeof data.playerIdx === 'number' && data.playerIdx >= 0 && players[data.playerIdx]) {
          players[data.playerIdx].handleClick(null, true);
        } else {
          players.forEach(p => p.handleClick(null, true));
        }
      }
    } else if (data.type === 'presenter_ready') {
      sendSyncMessage({ type: 'slide_change', slide: currentSlide });
    }
  }

  if (syncChannel) {
    syncChannel.addEventListener('message', (e) => handleSyncMessage(e.data));
  }
  window.addEventListener('message', (e) => handleSyncMessage(e.data));

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
   * Decode all frames from an APNG or Animated WebP asset (via inline Base64 or URL).
   */
  async function decodeAnimationFrames(src, base64Data) {
    const lower = src.toLowerCase();
    const mimeType = lower.endsWith('.webp') ? 'image/webp' : 'image/png';

    let buffer = null;
    if (base64Data) {
      try {
        const binStr = window.atob(base64Data);
        const bytes = new Uint8Array(binStr.length);
        for (let i = 0; i < binStr.length; i++) {
          bytes[i] = binStr.charCodeAt(i);
        }
        buffer = bytes.buffer;
      } catch (_b64Err) {
        buffer = null;
      }
    }

    if (!buffer) {
      try {
        const response = await fetch(src);
        if (!response.ok) {
          return await loadStaticImageFrame(src);
        }
        buffer = await response.arrayBuffer();
      } catch (_err) {
        // Fallback for file:// protocol when data-base64 is absent
        return await loadStaticImageFrame(src);
      }
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
  function createAnimPlayer(container, slideIdx, playerIdx) {
    const canvas = container.querySelector('.drawlib-anim-canvas');
    const badge = container.querySelector('.anim-play-badge');
    if (!canvas) return null;

    const ctx = canvas.getContext('2d');
    const src = canvas.getAttribute('data-src') || '';
    const base64Data = canvas.getAttribute('data-base64') || '';
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
      if (isPresenterMode && slideIdx === currentSlide) {
        updatePresenterAnimButton();
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

    function handleClick(e, skipSync) {
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

      if (!skipSync) {
        sendSyncMessage({
          type: 'anim_trigger',
          slide: slideIdx,
          playerIdx: playerIdx
        });
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

    container.addEventListener('click', (e) => handleClick(e, false));

    const readyPromise = decodeAnimationFrames(src, base64Data).then(decoded => {
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

  function cloneSlideIntoThumb(thumb, origSlide, idSuffix) {
    if (!origSlide) return;
    const slideBody = origSlide.querySelector('.slide-body');
    if (!slideBody) return;

    const thumbStage = document.createElement('div');
    thumbStage.className = 'overview-thumb-stage';

    const bodyClone = slideBody.cloneNode(true);
    bodyClone.querySelectorAll('canvas.drawlib-anim-canvas[data-base64]').forEach(el => {
      el.removeAttribute('data-base64');
    });
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
  }

  function syncThumbCanvases(selector) {
    const thumbs = document.querySelectorAll(selector);
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

  function syncOverviewCanvases() {
    syncThumbCanvases('.overview-modal .overview-thumb');
    if (isPresenterMode) {
      syncThumbCanvases('.presenter-thumb-preview');
    }
  }

  function updateThumbListScale(selector) {
    const thumbs = document.querySelectorAll(selector);
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

  function updateOverviewScale() {
    updateThumbListScale('.overview-modal .overview-thumb');
  }

  function initOverviewThumbs() {
    const thumbs = document.querySelectorAll('.overview-modal .overview-thumb');
    thumbs.forEach((thumb, idx) => {
      cloneSlideIntoThumb(thumb, slides[idx], `-ov-${idx + 1}`);
    });
  }

  function initAllAnimPlayers() {
    const readyPromises = [];
    slides.forEach((slide, idx) => {
      const slideIdx = idx + 1;
      const containers = slide.querySelectorAll('.drawlib-anim-container');
      const players = [];
      containers.forEach((container, pIdx) => {
        const player = createAnimPlayer(container, slideIdx, pIdx);
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
      if (isPresenterMode) {
        updatePresenterAnimButton();
      }
    });
  }

  // =========================================================================
  // Presenter View Mode (?presenter=1)
  // =========================================================================
  function openPresenterView() {
    if (isPresenterMode) return;
    if (presenterWindow && !presenterWindow.closed) {
      presenterWindow.focus();
      return;
    }
    const url = new URL(window.location.href);
    url.searchParams.set('presenter', '1');
    url.hash = `#${currentSlide}`;
    presenterWindow = window.open(
      url.toString(),
      'drawlib_presenter_view',
      'width=1360,height=860,menubar=no,toolbar=no,location=no,status=no'
    );
  }

  function updatePresenterAnimButton() {
    if (!isPresenterMode) return;
    const btnAnim = document.getElementById('pv-btn-anim');
    if (!btnAnim) return;

    const players = slideAnimPlayers.get(currentSlide);
    if (!players || players.length === 0) {
      btnAnim.disabled = true;
      btnAnim.classList.add('disabled');
      btnAnim.classList.remove('ready', 'playing', 'paused', 'ended');
      btnAnim.innerHTML = '<span class="pv-anim-icon">▶</span><span class="pv-anim-label">Animation</span>';
      btnAnim.setAttribute('title', 'No animations on this slide');
      return;
    }

    btnAnim.disabled = false;
    btnAnim.classList.remove('disabled', 'ready', 'playing', 'paused', 'ended');
    const st = players[0].getState();
    if (st === 'PLAYING') {
      btnAnim.classList.add('playing');
      btnAnim.innerHTML = '<span class="pv-anim-icon">⏸</span><span class="pv-anim-label">Pause Animation</span>';
      btnAnim.setAttribute('title', 'Pause animation on both screens (A)');
    } else if (st === 'PAUSED') {
      btnAnim.classList.add('paused');
      btnAnim.innerHTML = '<span class="pv-anim-icon">▶</span><span class="pv-anim-label">Resume Animation</span>';
      btnAnim.setAttribute('title', 'Resume animation on both screens (A)');
    } else if (st === 'ENDED') {
      btnAnim.classList.add('ended');
      btnAnim.innerHTML = '<span class="pv-anim-icon">↻</span><span class="pv-anim-label">Replay Animation</span>';
      btnAnim.setAttribute('title', 'Replay animation from beginning (A)');
    } else {
      btnAnim.classList.add('ready');
      btnAnim.innerHTML = '<span class="pv-anim-icon">▶</span><span class="pv-anim-label">Play Animation</span>';
      btnAnim.setAttribute('title', 'Play animation on both screens (A)');
    }
  }

  function triggerCurrentSlideAnimations() {
    const players = slideAnimPlayers.get(currentSlide);
    if (!players || players.length === 0) return;
    players.forEach(p => p.handleClick(null, true));
    sendSyncMessage({
      type: 'anim_trigger',
      slide: currentSlide,
      playerIdx: -1
    });
  }

  function updatePresenterView() {
    if (!isPresenterMode) return;

    // 1. Update page indicator & prev/next button states
    const indicator = document.getElementById('pv-page-indicator');
    if (indicator) {
      indicator.textContent = `${currentSlide} / ${totalSlides}`;
    }
    const btnPrev = document.getElementById('pv-btn-prev');
    const btnNext = document.getElementById('pv-btn-next');
    if (btnPrev) btnPrev.disabled = currentSlide <= 1;
    if (btnNext) btnNext.disabled = currentSlide >= totalSlides;

    // 2. Update animation button
    updatePresenterAnimButton();

    // 3. Update speaker notes content
    const notesContent = document.getElementById('pv-notes-content');
    if (notesContent) {
      const activeSlideEl = slides[currentSlide - 1];
      const notesEl = activeSlideEl ? activeSlideEl.querySelector('.slide-notes') : null;
      const html = notesEl ? notesEl.innerHTML.trim() : '';
      if (html) {
        notesContent.innerHTML = html;
        notesContent.classList.remove('empty');
      } else {
        notesContent.innerHTML = '<p class="presenter-notes-empty">No speaker notes for this slide.</p>';
        notesContent.classList.add('empty');
      }
      notesContent.scrollTop = 0;
    }

    // 4. Update sidebar active highlight & auto-scroll
    const items = document.querySelectorAll('.presenter-thumb-item');
    items.forEach((item, idx) => {
      if (idx + 1 === currentSlide) {
        item.classList.add('active');
        item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      } else {
        item.classList.remove('active');
      }
    });
  }

  function initPresenterView() {
    if (!isPresenterMode || !stage) return;

    document.body.classList.add('presenter-mode');
    document.title = `Presenter View — ${document.title}`;

    // Build 2-column Presenter Layout with horizontal resizer
    const layout = document.createElement('div');
    layout.className = 'presenter-layout';

    // Left column: vertical slide list
    const sidebar = document.createElement('aside');
    sidebar.className = 'presenter-sidebar';
    const sidebarHeader = document.createElement('div');
    sidebarHeader.className = 'presenter-sidebar-header';
    sidebarHeader.textContent = `Slides (${totalSlides})`;
    const thumbList = document.createElement('div');
    thumbList.className = 'presenter-thumb-list';

    slides.forEach((slideEl, idx) => {
      const slideNum = idx + 1;
      const item = document.createElement('div');
      item.className = 'presenter-thumb-item';
      item.setAttribute('data-target', String(slideNum));

      const labelEl = document.createElement('div');
      labelEl.className = 'presenter-thumb-label';
      const headingEl = slideEl.querySelector('.slide-body h1, .slide-body h2, .slide-body h3');
      const headingText = headingEl && headingEl.textContent ? headingEl.textContent.trim() : '';
      labelEl.textContent = headingText ? `${slideNum}. ${headingText}` : `Slide ${slideNum}`;

      const previewBox = document.createElement('div');
      previewBox.className = 'overview-thumb presenter-thumb-preview';
      cloneSlideIntoThumb(previewBox, slideEl, `-pv-${slideNum}`);

      item.appendChild(labelEl);
      item.appendChild(previewBox);
      item.addEventListener('click', () => {
        goToSlide(slideNum);
      });
      thumbList.appendChild(item);
    });

    sidebar.appendChild(sidebarHeader);
    sidebar.appendChild(thumbList);

    // Horizontal splitter between left sidebar and right main area
    const resizerCol = document.createElement('div');
    resizerCol.id = 'pv-resizer-col';
    resizerCol.className = 'presenter-resizer-col';
    resizerCol.setAttribute('title', 'Drag left/right to resize slide list');

    // Right column: Top = Current Slide Preview, Middle = Control Bar, Resizer, Bottom = Speaker Notes
    const mainCol = document.createElement('main');
    mainCol.className = 'presenter-main';

    // Right Top: Current Slide Preview
    const previewPane = document.createElement('section');
    previewPane.className = 'presenter-preview-pane';
    const previewStageWrap = document.createElement('div');
    previewStageWrap.className = 'presenter-preview-stage-wrap';
    previewStageWrap.id = 'pv-stage-wrap';
    previewStageWrap.appendChild(stage);
    previewPane.appendChild(previewStageWrap);

    // Right Middle: Control Bar
    const toolbar = document.createElement('div');
    toolbar.className = 'presenter-toolbar';
    toolbar.innerHTML = `
      <div class="pv-nav-group">
        <button id="pv-btn-prev" class="pv-btn" title="Previous Slide (←)">◀ Prev</button>
        <span id="pv-page-indicator" class="pv-page-indicator">1 / ${totalSlides}</span>
        <button id="pv-btn-next" class="pv-btn" title="Next Slide (→)">Next ▶</button>
      </div>
      <div class="pv-anim-group">
        <button id="pv-btn-anim" class="pv-btn pv-btn-anim disabled" disabled title="No animations on this slide">
          <span class="pv-anim-icon">▶</span><span class="pv-anim-label">Animation</span>
        </button>
      </div>
      <div class="pv-timer-group">
        <span id="pv-timer-display" class="pv-timer-display" title="Elapsed presentation time">00:00</span>
        <button id="pv-btn-timer-reset" class="pv-btn pv-btn-icon" title="Reset Timer">↺</button>
      </div>
    `;

    // Vertical splitter above Speaker Notes
    const resizerRow = document.createElement('div');
    resizerRow.id = 'pv-resizer-row';
    resizerRow.className = 'presenter-resizer-row';
    resizerRow.setAttribute('title', 'Drag up/down to resize speaker notes');

    // Right Bottom: Speaker Notes
    const notesPane = document.createElement('section');
    notesPane.className = 'presenter-notes-pane';
    notesPane.innerHTML = `
      <div id="pv-notes-header" class="presenter-notes-header" title="Drag up/down to resize speaker notes">
        <span class="presenter-notes-title">Speaker Notes</span>
        <div class="presenter-notes-tools">
          <button id="pv-notes-font-dec" class="pv-btn pv-btn-sm" title="Decrease font size">A-</button>
          <button id="pv-notes-font-inc" class="pv-btn pv-btn-sm" title="Increase font size">A+</button>
        </div>
      </div>
      <div id="pv-notes-content" class="presenter-notes-content"></div>
    `;

    mainCol.appendChild(previewPane);
    mainCol.appendChild(toolbar);
    mainCol.appendChild(resizerRow);
    mainCol.appendChild(notesPane);

    layout.appendChild(sidebar);
    layout.appendChild(resizerCol);
    layout.appendChild(mainCol);
    document.body.insertBefore(layout, document.body.firstChild);

    // Bind horizontal resizer (left sidebar width)
    function startColResize(e) {
      e.preventDefault();
      const startX = e.clientX;
      const startWidth = sidebar.getBoundingClientRect().width;
      document.body.classList.add('is-resizing-col');
      resizerCol.classList.add('active');

      function onMouseMove(moveEvent) {
        const minW = 160;
        const maxW = Math.max(minW, window.innerWidth - 400);
        const newW = Math.max(minW, Math.min(maxW, Math.round(startWidth + (moveEvent.clientX - startX))));
        layout.style.setProperty('--pv-sidebar-width', `${newW}px`);
        updateScale();
      }

      function onMouseUp() {
        document.body.classList.remove('is-resizing-col');
        resizerCol.classList.remove('active');
        window.removeEventListener('mousemove', onMouseMove);
        window.removeEventListener('mouseup', onMouseUp);
      }

      window.addEventListener('mousemove', onMouseMove);
      window.addEventListener('mouseup', onMouseUp);
    }
    resizerCol.addEventListener('mousedown', startColResize);

    // Bind vertical resizer (speaker notes height)
    function startRowResize(e) {
      if (e.target && e.target.closest('button')) {
        return;
      }
      e.preventDefault();
      const startY = e.clientY;
      const startHeight = notesPane.getBoundingClientRect().height;
      document.body.classList.add('is-resizing-row');
      resizerRow.classList.add('active');

      function onMouseMove(moveEvent) {
        const minH = 100;
        const maxH = Math.max(minH, window.innerHeight - 220);
        const newH = Math.max(minH, Math.min(maxH, Math.round(startHeight - (moveEvent.clientY - startY))));
        mainCol.style.setProperty('--pv-notes-height', `${newH}px`);
        updateScale();
      }

      function onMouseUp() {
        document.body.classList.remove('is-resizing-row');
        resizerRow.classList.remove('active');
        window.removeEventListener('mousemove', onMouseMove);
        window.removeEventListener('mouseup', onMouseUp);
      }

      window.addEventListener('mousemove', onMouseMove);
      window.addEventListener('mouseup', onMouseUp);
    }
    resizerRow.addEventListener('mousedown', startRowResize);
    const notesHeader = document.getElementById('pv-notes-header');
    if (notesHeader) {
      notesHeader.addEventListener('mousedown', startRowResize);
    }

    // Bind Toolbar Controls
    const btnPrev = document.getElementById('pv-btn-prev');
    const btnNext = document.getElementById('pv-btn-next');
    const btnAnim = document.getElementById('pv-btn-anim');
    const btnTimerReset = document.getElementById('pv-btn-timer-reset');
    const timerDisplay = document.getElementById('pv-timer-display');
    const btnFontDec = document.getElementById('pv-notes-font-dec');
    const btnFontInc = document.getElementById('pv-notes-font-inc');
    const notesContent = document.getElementById('pv-notes-content');

    if (btnPrev) btnPrev.addEventListener('click', prevSlide);
    if (btnNext) btnNext.addEventListener('click', nextSlide);
    if (btnAnim) btnAnim.addEventListener('click', triggerCurrentSlideAnimations);

    // Elapsed timer
    let startTime = Date.now();
    function updateTimer() {
      if (!timerDisplay) return;
      const elapsedSec = Math.floor((Date.now() - startTime) / 1000);
      const mins = String(Math.floor(elapsedSec / 60)).padStart(2, '0');
      const secs = String(elapsedSec % 60).padStart(2, '0');
      timerDisplay.textContent = `${mins}:${secs}`;
    }
    setInterval(updateTimer, 1000);
    if (btnTimerReset) {
      btnTimerReset.addEventListener('click', () => {
        startTime = Date.now();
        updateTimer();
      });
    }

    // Speaker notes font size adjustment
    function applyNotesFontSize() {
      if (notesContent) {
        notesContent.style.fontSize = `${notesFontSizeRem.toFixed(2)}rem`;
      }
    }
    applyNotesFontSize();
    if (btnFontDec) {
      btnFontDec.addEventListener('click', () => {
        notesFontSizeRem = Math.max(0.85, notesFontSizeRem - 0.12);
        applyNotesFontSize();
      });
    }
    if (btnFontInc) {
      btnFontInc.addEventListener('click', () => {
        notesFontSizeRem = Math.min(2.2, notesFontSizeRem + 0.12);
        applyNotesFontSize();
      });
    }

    // Observe resize of preview pane & sidebar so scaling stays crisp
    if (typeof window.ResizeObserver === 'function') {
      const ro = new window.ResizeObserver(() => {
        updateScale();
      });
      ro.observe(previewStageWrap);
      ro.observe(sidebar);
    }

    // Notify main window that presenter view is ready
    sendSyncMessage({ type: 'presenter_ready' });
  }

  /**
   * Automatically calculate scaling factor to fit viewport while maintaining 16:9 aspect ratio.
   */
  function updateScale() {
    if (!stage) return;

    if (isPresenterMode) {
      const wrap = document.getElementById('pv-stage-wrap');
      if (wrap) {
        const availW = Math.max(100, wrap.clientWidth - 24);
        const availH = Math.max(60, wrap.clientHeight - 24);
        const scale = Math.min(availW / STAGE_WIDTH, availH / STAGE_HEIGHT);
        stage.style.transform = `scale(${scale})`;
      }
      updateThumbListScale('.presenter-thumb-preview');
      if (isOverviewOpen) {
        updateOverviewScale();
      }
      return;
    }

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
  function goToSlide(index, skipSync) {
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

    // Update overview modal thumbs
    document.querySelectorAll('.overview-modal .overview-thumb').forEach((thumb, idx) => {
      if (idx + 1 === currentSlide) {
        thumb.classList.add('current');
      } else {
        thumb.classList.remove('current');
      }
    });

    if (isPresenterMode) {
      updatePresenterView();
    }

    if (!skipSync) {
      sendSyncMessage({ type: 'slide_change', slide: currentSlide });
    }
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
        case 'p':
        case 'P':
        case 's':
        case 'S':
          e.preventDefault();
          openPresenterView();
          break;
        case 'a':
        case 'A':
          e.preventDefault();
          triggerCurrentSlideAnimations();
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
    const controls = document.querySelector('.slide-controls');
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const btnOverview = document.getElementById('btn-overview');
    const btnPresenter = document.getElementById('btn-presenter');
    const btnFullscreen = document.getElementById('btn-fullscreen');

    if (btnPrev) btnPrev.addEventListener('click', prevSlide);
    if (btnNext) btnNext.addEventListener('click', nextSlide);
    if (btnOverview) btnOverview.addEventListener('click', toggleOverview);
    if (btnPresenter) btnPresenter.addEventListener('click', openPresenterView);
    if (btnFullscreen) btnFullscreen.addEventListener('click', toggleFullscreen);

    let controlsHideTimer = null;
    function showControlsTemporarily() {
      if (!controls || isPresenterMode) return;
      controls.classList.add('visible');
      if (controlsHideTimer) {
        clearTimeout(controlsHideTimer);
      }
      controlsHideTimer = setTimeout(() => {
        if (!controls.matches(':hover')) {
          controls.classList.remove('visible');
        }
      }, 1000);
    }

    if (!isPresenterMode) {
      window.addEventListener('mousemove', showControlsTemporarily, { passive: true });
      window.addEventListener('mousedown', showControlsTemporarily, { passive: true });
      window.addEventListener('touchstart', showControlsTemporarily, { passive: true });
      if (controls) {
        controls.addEventListener('mouseleave', showControlsTemporarily);
      }
    }

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
    document.querySelectorAll('.overview-modal .overview-thumb').forEach((thumb, idx) => {
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
    goToSlide(currentSlide, true);
  }

  // Lifecycle initialization
  window.addEventListener('resize', updateScale);
  window.addEventListener('hashchange', initFromHash);
  window.addEventListener('DOMContentLoaded', () => {
    initOverviewThumbs();
    if (isPresenterMode) {
      initPresenterView();
    }
    initAllAnimPlayers();
    setupKeyboard();
    setupControls();
    initFromHash();
    updateScale();
  });

  // Re-scale immediately
  updateScale();
})();
