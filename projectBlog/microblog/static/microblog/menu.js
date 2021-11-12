window.onload = function () {
    let burgerSymbol = document.getElementById("burger-symbol");
    burgerSymbol.onclick = function () {
        Array.from(document.getElementsByClassName("menu")).forEach(menu => {
            let delay = 0;
            Array.from(menu.getElementsByTagName("li")).forEach(li => {
                setTimeout(function () {
                    if (li.style.display === "block") {
                        li.style.display = "inline-block";
                        document.getElementById("menu-heading").style.display = "none";
                    } else {
                        document.getElementById("menu-heading").style.display = "block";
                        li.style.display = "block";
                    }
                }, delay);
                delay += 50;
            })
        });
    }
}