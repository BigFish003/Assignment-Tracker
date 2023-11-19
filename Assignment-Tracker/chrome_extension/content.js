// Check if the URL has already been clicked and sent
function isUrlAlreadySent(url) {
  const clickedUrls = JSON.parse(localStorage.getItem('clickedUrls')) || [];
  return clickedUrls.includes(url);
}
// Mark the URL as sent
function markUrlAsSent(url) {
  const clickedUrls = JSON.parse(localStorage.getItem('clickedUrls')) || [];
  clickedUrls.push(url);
  console.log(clickedUrls);
  localStorage.setItem('clickedUrls', JSON.stringify(clickedUrls));
}
function send() {
  const url = "http://127.0.0.1:5000/api";
  const duedat = document.querySelector('.display_date');
  const dat = duedat ? duedat.textContent : "No Due Date";
  const fincont = document.querySelector('.description.user_content');
  const cont = fincont ? fincont.textContent : "No Content";
  const dict = {
    dd: dat,
    at: document.title,
	c: cont,
    url: curl
  };
  // Check if the URL has already been sent
  localStorage.clear();
  if (!isUrlAlreadySent(curl)) {
    fetch(url, {
      method: "POST",
      body: JSON.stringify({ message: dict }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.response);
        // Mark the URL as sent after successfully sending
        markUrlAsSent(curl);
      })
      .catch(error => {
        console.error("Error:", error);
      });
  }
}
const curl = window.location.href;
const turl = "aisdblend.instructure.com/courses";
if (curl.includes(turl) && curl.includes("assignments")) {
  send();
  console.log(document.title);
}
