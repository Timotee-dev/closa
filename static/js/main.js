// Copy the referral link
document.querySelectorAll("[data-copy]").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var input = document.querySelector(btn.dataset.copy);
    input.select();
    var done = function () {
      var old = btn.textContent;
      btn.textContent = "Copied";
      setTimeout(function () { btn.textContent = old; }, 1500);
    };
    if (navigator.clipboard) navigator.clipboard.writeText(input.value).then(done);
    else { document.execCommand("copy"); done(); }
  });
});

// If the form came back with errors, jump to it
if (document.querySelector(".form .errorlist")) {
  document.getElementById("join").scrollIntoView();
}
