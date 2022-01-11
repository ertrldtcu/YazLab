var tabs = document.querySelectorAll("[data-tab-target]")
var tabContents = document.querySelectorAll("[data-tab-content]")

tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        var target = document.querySelector(tab.dataset.tabTarget)
        tabContents.forEach(tabContent => {
            tabContent.classList.remove("active")
        })
        tabs.forEach(tab => {
            tab.classList.remove("active")
        })
        tab.classList.add("active")
        target.classList.add("active")
    })
})


function expand(event) {
    event.target.parentNode.classList.toggle("expand")
    event.target.classList.toggle("expand")
}

var username = document.querySelector("#usernames")
var student = document.querySelector("#student")
var lesson = document.querySelector("#lesson")
var title = document.querySelector("#title")
var keywords = document.querySelector("#keywords")
var period = document.querySelector("#period")

var filelist = document.querySelector("#filelist")
var fileitems = filelist.getElementsByClassName("fileitem")

function filter(event) {

    var show = new Array(fileitems.length).fill(true);

    for (var i = 0; i < fileitems.length; i = i + 1) {
        if (fileitems[i].querySelector(".usernameitemli").innerHTML.search(username.value) == -1) {
            show[i] = false
        }
        if (fileitems[i].querySelector(".student").innerHTML.search(student.value) == -1) {
            show[i] = false
        }
        if (fileitems[i].querySelector(".lesson").innerHTML.search(lesson.value) == -1) {
            show[i] = false
        }
        if (fileitems[i].querySelector(".title").innerHTML.search(title.value) == -1) {
            show[i] = false
        }
        if (fileitems[i].querySelector(".keywords").innerHTML.search(keywords.value) == -1) {
            show[i] = false
        }
        if (fileitems[i].querySelector(".period").innerHTML.search(period.value) == -1) {
            show[i] = false
        }
    }

    for (var i = 0; i < fileitems.length; i = i + 1) {
        fileitems[i].style.display = "none";
        if (show[i]) {
            fileitems[i].style.display = "";
        }
    }
}