// background.js

// Clear local storage when the extension is first loaded
chrome.runtime.onInstalled.addListener(function () {
  chrome.storage.local.clear();
});
