document.getElementById('openDesktop').addEventListener('click', () => {
  chrome.tabs.create({ url: 'https://www.classcard.net/Login' });
});

document.getElementById('openMobile').addEventListener('click', () => {
  chrome.tabs.create({ url: 'https://www.classcard.net/Login' });
});

document.getElementById('openDocs').addEventListener('click', () => {
  chrome.tabs.create({ url: 'README.md' });
});
