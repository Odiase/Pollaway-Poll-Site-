const personal_poll_btn = document.getElementById("personal-poll-btn");
const other_poll_btn = document.getElementById("other-poll-btn");
const personal_poll_container = document.querySelector(".personal-polls-container");
const other_poll_container = document.querySelector(".other-polls-container");

const intro_section = document.querySelector(".create-poll-intro-section");
const add_option_btn = document.getElementById("add-option-btn");
const remove_option_btn = document.getElementById("remove-option-btn");


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

// changes the polls options
function change_option(current_option,new_option,current_poll,new_poll){
    // change the look of the button
    current_option.classList.remove("selected-option");
    current_option.classList.add("not-selected-option");
    new_option.classList.remove("not-selected-option");
    new_option.classList.add("selected-option");

    // change the poll field
    current_poll.classList.add("non-active-poll");
    current_poll.classList.remove("active-poll");

    new_poll.classList.add("active-poll");
    new_poll.classList.remove("non-active-poll");
}
// checks to see if i can get a personal poll btn from the current document
if(personal_poll_btn){
    personal_poll_btn.addEventListener("click",() => {
        change_option(other_poll_btn,personal_poll_btn,other_poll_container,personal_poll_container)
    });

    other_poll_btn.addEventListener("click",() => {
        change_option(personal_poll_btn,other_poll_btn,personal_poll_container,other_poll_container)
    });
}



/****************************  create poll code section **********************/
if (intro_section){
    window.addEventListener("load",function(){
        intro_section.classList.add("show")
    })
}

if(add_option_btn){
    const options_container = document.querySelector(".options");
    
    function check_option_length(){
        if(document.querySelectorAll(".option").length <= 2){
            remove_option_btn.style.display = "none";
        }
        else{
            remove_option_btn.style.display = "block"
        }
    }

    function create_option(){
        const options = document.querySelectorAll(".option")
        if(options.length < 4){
            var input_tag = document.createElement("input");
            var label_tag = document.createElement("label");
            var option_wrapper = document.createElement("div")
            var option_name = document.createTextNode(`Option ${options.length + 1}:`)

            option_wrapper.classList.add("option");
            input_tag.classList.add("text-input");
            input_tag.name = "option"
            input_tag.type = "text"

            label_tag.appendChild(option_name)
            option_wrapper.appendChild(label_tag)
            option_wrapper.appendChild(input_tag)
            options_container.appendChild(option_wrapper)
        }
        check_option_length()
    }

    function remove_option(){
        check_option_length()
        const options = document.querySelectorAll(".option")
        options[options.length -1].remove()
        check_option_length()
    }

    
    check_option_length()
    add_option_btn.addEventListener("click", () => {
        create_option()
    })
    remove_option_btn.addEventListener("click", () => {
        remove_option()
    })
}


