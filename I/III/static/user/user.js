let selectFileButton = document.querySelector("#selectFile")
let selectedFileSpan = document.querySelector("#selectedFile")
let selectFileInput = document.querySelector("#uploadfile")

selectFileButton.addEventListener("click", () => {
    selectFileInput.click()
})

selectFileInput.addEventListener("change", () => {
    if (selectFileInput.value)
        selectedFileSpan.innerHTML = selectFileInput.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1]
    else
        selectedFileSpan.innerHTML = "henüz dosya seçilmedi.."
})

function expand(event) {
    event.target.parentNode.classList.toggle("expand")
    event.target.classList.toggle("expand")
}

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