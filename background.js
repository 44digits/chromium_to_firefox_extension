// Adds an "Open link in Firefox" context-menu action.
// When selected, the link URL is sent to the local relay server.
// Date: 2026-10-13
// User: 44digits
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "openInFirefox",
    title: "Open link in Firefox",
    contexts: ["link"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "openInFirefox" && info.linkUrl) {
    fetch('http://localhost:18080/open', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: info.linkUrl })
    })
    .then(response => console.log('Link sent to server:', response.status))
    .catch(error => console.error('Error sending link to server:', error));
  }
});