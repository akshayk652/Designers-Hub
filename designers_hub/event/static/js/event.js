document.addEventListener('DOMContentLoaded', (e) => {

    let countDownDate = new Date();
    let newdate = countDownDate.setMinutes(countDownDate.getMinutes() + 5);
    console.log(newdate)
    let x = setInterval(() => {

        let now = new Date().getTime();

        let distance = newdate - now;

        let days = Math.floor(distance / (1000 * 60 * 60 * 24));
        let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.querySelector(".timer span").innerHTML = minutes + "m " + seconds + "s ";


        if (distance < 0) {
            clearInterval(x);
            document.querySelector(".timer span").innerHTML = "EXPIRED";
            document.querySelector(".slide .hide-me").style.display = "none";
        }
    }, 1000);
})