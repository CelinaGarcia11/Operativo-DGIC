/* Operativo DDCP — interacción.
   Sin JavaScript la página ya se ve: índice + las 57 fichas seguidas.
   Con JavaScript pasa a modo "una ficha por vez" con buscador y navegación. */
(function () {
  var root = document.documentElement;
  root.className += ' js';

  var chips  = [].slice.call(document.querySelectorAll('.chip'));
  var fichas = [].slice.call(document.querySelectorAll('.ficha'));
  var nums   = fichas.map(function (f) { return +f.getAttribute('data-n'); });
  var actual = nums[0];

  function pintar(n, mover) {
    actual = n;
    chips.forEach(function (c) {
      c.classList.toggle('sel', +c.getAttribute('data-n') === n);
    });
    fichas.forEach(function (f) {
      f.classList.toggle('activa', +f.getAttribute('data-n') === n);
    });
    var i = nums.indexOf(n);
    fichas.forEach(function (f) {
      var prev = f.querySelector('.navbtn[data-dir="-1"]');
      var next = f.querySelector('.navbtn[data-dir="1"]');
      if (prev) prev.disabled = i <= 0;
      if (next) next.disabled = i >= nums.length - 1;
    });
    try { history.replaceState(null, '', '#alfa' + n); } catch (e) {}
    if (mover) {
      var a = document.querySelector('.ficha.activa');
      if (a && window.matchMedia('(max-width: 900px)').matches) {
        a.scrollIntoView({ block: 'start' });
      }
    }
  }

  chips.forEach(function (c) {
    c.addEventListener('click', function (ev) {
      ev.preventDefault();
      pintar(+c.getAttribute('data-n'), true);
    });
  });

  document.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('.navbtn');
    if (!b) return;
    var i = nums.indexOf(actual) + (+b.getAttribute('data-dir'));
    if (i >= 0 && i < nums.length) pintar(nums[i], true);
  });

  document.addEventListener('keydown', function (ev) {
    if (ev.target.tagName === 'INPUT') return;
    var d = ev.key === 'ArrowRight' ? 1 : ev.key === 'ArrowLeft' ? -1 : 0;
    if (!d) return;
    var i = nums.indexOf(actual) + d;
    if (i >= 0 && i < nums.length) pintar(nums[i], false);
  });

  var q = document.getElementById('q');
  if (q) {
    q.addEventListener('input', function () {
      var t = q.value.trim().toLowerCase();
      var primero = null;
      chips.forEach(function (c) {
        var n = +c.getAttribute('data-n');
        var f = document.getElementById('alfa' + n);
        var hay = !t || (f.textContent || '').toLowerCase().indexOf(t) >= 0;
        c.classList.toggle('dim', !hay);
        if (hay && primero === null) primero = n;
      });
      if (t && primero !== null) pintar(primero, false);
    });
  }

  window.addEventListener('hashchange', function () {
    var m = /^#alfa(\d{1,2})$/i.exec(location.hash || '');
    if (m && nums.indexOf(+m[1]) >= 0 && +m[1] !== actual) pintar(+m[1], true);
  });

  var m = /^#alfa(\d{1,2})$/i.exec(location.hash || '');
  pintar(m && nums.indexOf(m[1]) >= 0 ? m[1] : nums[0], false);
})();
