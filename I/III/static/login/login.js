let goAdmin = document.querySelector("#admin-button")
let adminimg = document.querySelector("#admin-img")
let normalimg = document.querySelector("#normal-img")

let state = false

goAdmin.addEventListener("click", () => {
    document.body.classList.toggle("dark")
    if (state) {
        normalimg.classList.remove("hide-normal")
        normalimg.classList.add("show-normal")
        adminimg.classList.remove("show-admin")
        adminimg.classList.add("hide-admin")
    } else {
        adminimg.classList.remove("hide-admin")
        adminimg.classList.add("show-admin")
        normalimg.classList.remove("show-normal")
        normalimg.classList.add("hide-normal")

    }
    state = !state
});

$(document).ready(function() {
    $('form').on('submit', function(e) {
        e.preventDefault();
        username = $('#username').val()
        password = $('#password').val()
        if (username == "" || password == "") {
            return alert("Lütfen tüm alanları doldurunuz.")
        }
        $.ajax({
                data: {
                    username: username,
                    password: password
                },
                type: 'POST',
                url: '/login'
            })
            .done(function(data) {
                if (data.message) {
                    alert(data.message)
                } else {
                    window.location.href = data.redirect;
                }
            });
    });
});