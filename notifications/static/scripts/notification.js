const unread_container = document.querySelector(".unread-notification-wrapper");
const unread_notifications = document.querySelectorAll(".unread");

const read_container = document.querySelector(".read-notification-wrapper");
const read_notifications = document.querySelectorAll(".read");

const no_notification = document.getElementById("no-notification-btn");

// hides the unread notification container, if there are no unread notifications
if (unread_notifications.length === 0){
    unread_container.style.display = "none";
}
if (read_notifications.length === 0){
    read_container.style.display = "none";
}
if(unread_notifications.length === 0 && read_notifications.length === 0){
    no_notification.style.display = "block"
}else{
    no_notification.style.display = "none"
}