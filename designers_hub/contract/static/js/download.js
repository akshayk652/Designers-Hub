document.addEventListener('DOMContentLoaded', function() {
    var elem = document.querySelector('.download');
    const modal = document.querySelector(".main-modal");
    clicked = false
    elem.addEventListener("click", (e) => {
      if(!clicked) {
        clicked = true
        modal.classList.remove("hide")
        modal.classList.add("animate")
      }else {
        clicked = false
        modal.classList.add("hide")
        modal.classList.add("animate")
      }
    })
  });