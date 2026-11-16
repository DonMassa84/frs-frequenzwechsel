(() => {
  const view = document.currentScript.dataset.view;
  const supportedHosts = ['donmassa84.github.io', 'frs-frequenzwechsel.derboss.chatgpt.site'];
  if (!supportedHosts.includes(location.hostname)) return;
  if (navigator.globalPrivacyControl || navigator.doNotTrack === '1') return;

  const endpoint = 'https://frs-frequenzwechsel.derboss.chatgpt.site/api/metrics';
  function count(event) {
    fetch(endpoint, {
      method: 'POST',
      body: event,
      credentials: 'omit',
      referrerPolicy: 'no-referrer',
      keepalive: true,
    }).catch(() => {});
  }

  function countVisibleView() {
    if (document.visibilityState !== 'visible') return;
    document.removeEventListener('visibilitychange', countVisibleView);
    count(view);
  }

  if (document.visibilityState === 'visible') countVisibleView();
  else document.addEventListener('visibilitychange', countVisibleView);

  document.addEventListener('click', event => {
    const link = event.target.closest('a[data-metric]');
    if (link) count(link.dataset.metric);
  });
})();
