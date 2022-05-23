const menu_btn = document.querySelector(".menu-btn");
const menu = document.querySelector(".menu");
const nav_links = document.querySelectorAll(".nav-links");

function navbar_toggle(){
    if (menu.style.right == "0%"){
        menu.style.right = "-100%";
        menu.style.display = "none";
    }
    else{
        menu.style.right = "0%";
        menu.style.display = "block";
    }
}

function current_page(link){
    link.classList.add("current-page");
    link.style.color = "white";
}


for(let i = 0; i < nav_links.length; i++){
    if(window.location.pathname == "/settings/"){
        current_page(nav_links[6])
    }
    else if(window.location.pathname == "/notifications/"){
        current_page(nav_links[5])
    }
    else if(window.location.pathname == "/my-account/"){
        current_page(nav_links[4])
    }
    else if(window.location.pathname == "/polls/"){
        current_page(nav_links[1])
    }
    else if(window.location.pathname == "/polls/my-polls/"){
        current_page(nav_links[2])
    }
}
menu_btn.addEventListener("click",navbar_toggle);

