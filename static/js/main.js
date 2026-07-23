// Bio Leaf Exports — small progressive enhancements

document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss flash messages after a few seconds
  var flashes = document.querySelectorAll('.flash');
  flashes.forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity 0.4s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.style.display = 'none'; }, 400);
    }, 6000);
  });
});
