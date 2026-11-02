// Copy only the citation text selected by the reader. No network or analytics.
document.addEventListener('click', async (event) => {
  const button = event.target.closest('[data-copy-citation]');
  if (!button) return;
  const code = document.getElementById(button.dataset.copyCitation);
  const status = button.parentElement.querySelector('[role="status"]');
  if (!code || !status) return;
  try {
    await navigator.clipboard.writeText(code.textContent);
    status.textContent = 'BibTeX copied.';
  } catch {
    status.textContent = 'Select the BibTeX below to copy, or download the .bib file.';
  }
});
