function set_vote_percentage(){
    const options = document.querySelectorAll(".option input[type = hidden]");
    const option_ratings = document.querySelectorAll(".option-rating div");
    for(let i = 0; i < options.length; i++){
        option = options[i]
        option_ratings[i].style.width= `${option.value}%`;
    }
}

/// runs for the checkbox inputs
if(document.querySelectorAll(".option input[type = checkbox]").length > 0){
    set_vote_percentage()
}

// runs for the radio inputs
if (document.querySelectorAll(".option input[type = radio]").length > 0){
    set_vote_percentage()
}
