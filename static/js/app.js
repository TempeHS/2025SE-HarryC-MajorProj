if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("static/js/serviceWorker.js")
      .then((res) => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}

// This script toggles the active class and aria-current attribute on the nav links
document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll(".nav-link");
  const currentUrl = window.location.pathname;

  navLinks.forEach((link) => {
    const linkUrl = link.getAttribute("href");
    if (linkUrl === currentUrl) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  });
});

function confirmAction(message, formId) {
  if (confirm(message)) {
    document.getElementById(formId).submit();
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const logoutButton = document.getElementById("logoutButton");

  if (logoutButton) {
    logoutButton.addEventListener("click", function () {
      confirmAction("Are you sure you want to logout?", "logoutForm");
    });
  }
});

tinymce.init({
  selector: "#blog_content",
  plugins:
    "advlist autolink lists link charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table paste code help wordcount",
  toolbar:
    "undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help",
  menubar: false,
  height: 300,
  setup: function (editor) {
    editor.on("change", function () {
      editor.save();
    });
  },
});
