

function form_handler(event) {
    event.preventDefault();
}

function onSubmit(){
    document.querySelector('form').addEventListener('submit', form_handler);

   //send & recieve data to predict
    var fd = new FormData(document.querySelector('form'));
    console.log(fd)

    var xhr  = new XMLHttpRequest()
    
    xhr.open("POST",'/index',true)

    xhr.onreadystatechange = function(){
        if (xhr.readyState == 4 && xhr.status ==200){
            console.log("success")
        }
    };
    xhr.onload = function(){};
    xhr.send(fd)
}

