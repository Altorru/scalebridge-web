(() => {
  const key = 'scalebridge-theme';
  const valid = value => ['light', 'dark', 'system'].includes(value);
  const apply = value => {
    if (!valid(value) || value === 'system') delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = value;
  };
  let saved = 'system';
  try { const value = localStorage.getItem(key); if (valid(value)) saved = value; } catch (_) {}
  apply(saved);
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-theme-control]').forEach(control => {
      control.value = saved;
      control.addEventListener('change', () => {
        saved = valid(control.value) ? control.value : 'system';
        apply(saved);
        document.querySelectorAll('[data-theme-control]').forEach(other => { other.value = saved; });
        try { localStorage.setItem(key, saved); } catch (_) {}
      });
    });
  });
})();
