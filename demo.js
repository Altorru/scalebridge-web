(() => {
  const buttons = [...document.querySelectorAll('[data-demo-step]')];
  const panels = [...document.querySelectorAll('[data-demo-panel]')];
  const progress = document.querySelector('[data-demo-progress]');
  if (!buttons.length || !panels.length || !progress) return;
  const titles = ['Lire le fichier fictif', 'Vérifier les lignes', 'Comparer les exports'];
  const select = (index) => {
    buttons.forEach((button, i) => {
      button.setAttribute('aria-pressed', String(i === index));
      if (i === index) button.setAttribute('aria-current', 'step');
      else button.removeAttribute('aria-current');
    });
    panels.forEach((panel, i) => { panel.hidden = i !== index; });
    progress.textContent = `Étape ${index + 1} sur 3 : ${titles[index]}`;
  };
  buttons.forEach((button, index) => button.addEventListener('click', () => select(index)));
  select(0);
})();
