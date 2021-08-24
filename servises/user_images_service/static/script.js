const headers = {
    "Content-Type": "application/json",
  };
const inputElement = document.getElementById("inputGroupFile03");

let output = document.getElementById('output');

inputElement.addEventListener("change", handleFiles, false);

let fileList

// Функция загружает изображение в предосмотр
function handleFiles() {
    fileList = this.files;
  try {
    output.src = URL.createObjectURL(this.files[0]);
  } catch (error) {
      console.log(undefined);
  }
  
}

// Функция загружает отправляет  изображение на сервер
async function uploadImage(){
    let alerts = document.getElementById('succes_upload')
    let formData = new FormData();
    formData.append("image", fileList[0], fileList[0].name);

    document.querySelector('.send-load').classList.add('send-load-true')
    document.querySelector('.send').classList.add('send-text')

     fetch('http://localhost:8000/api/v1/pictures/uploadimages/', {
        method: 'post',
        body: formData,
        
        }).then(function(response) {
            
            

            setTimeout(() => {
                alerts.classList.add("succes_upload-true");
                setTimeout(() => {
                    alerts.classList.remove("succes_upload-true");
                }, 2000);
               

                document.querySelector('.send-load').classList.remove('send-load-true')
                document.querySelector('.send').classList.remove('send-text')
                inputElement.value = ""
                output.src = ""
            }, 2000);

   
            return response.json();

        }).then(function(data) {
        console.log(data);
        });
    }