const intro_texts = document.querySelectorAll(".auth-intro-text");

function reveal_intro_text(){
    for(let i = 0; i < intro_texts.length; i++){
        intro_texts[i].classList.remove("text-invisible");
        intro_texts[i].classList.add("auth-intro-text");
    }
}
window.addEventListener("load",() => {
    reveal_intro_text()
})