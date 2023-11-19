document.addEventListener('DOMContentLoaded', function () {
  chrome.identity.getProfileUserInfo(function(userInfo) {
    if (!chrome.runtime.lastError && userInfo.id) {
      const userId = userInfo.id;
      document.getElementById('userInfo').textContent = `User ID: ${userId}`;
    } else {
      console.error("Error getting user info:", chrome.runtime.lastError);
      document.getElementById('userInfo').textContent = 'Error retrieving user info';
    }
  });
});
