let ws

// const debug_path = 'localhost:8000'

const debug_path  = 'api-booking.ru:8000'

function onwssocket(){
  ws = new WebSocket(`ws://${debug_path}/ws/${localStorage.getItem('google_id')}`);
  ws.onmessage = (event) => {
    let result = JSON.parse(event.data)
    if (result.close_result) {
  
      let data = {
        "origin_img_id": Number(result.origin_img_id),
        "result_dict": String(result.result_dict),
        "status": true,
      }
  
      fetch(`http://${debug_path}/api/v1/users/change_status/${localStorage.getItem('google_id')}`, {
        method: 'post',
        headers: headers,
        body: JSON.stringify(data)
      }).then(function (responce) {
        return responce.json();
      }).then(function (data) {
        console.log('загрузка прошла успешно');
        let result_count = document.querySelector('.text-result_count')
        result_count.innerHTML = `обработка завершена`
        upload = 0
      })
    }
    else {
      let data_add_link = {
        'img_link': result.result_image
      }
      fetch(`http://${debug_path}/api/v1/pictures/add_link_img/${Number(result.origin_img_id)}`, {
        method: 'post',
        headers: headers,
        body: JSON.stringify(data_add_link)
      }).then(function (responce) {
        return responce.json();
      }).then(function (data) {
        console.log('линк добавлен', data);
        let result_count = document.querySelector('.text-result_count')
        result_count.innerHTML = `Обработано ${data.count_res_image}/10 часть изображения`
        output.classList.add('not-output')
        setTimeout(() => {
          output.classList.remove('not-output')
        }, 1000);
        output.src = data.result_imgs_link
      })
    }
  }
}



const headers = {
  "Content-Type": "application/json",
};
const inputElement = document.getElementById("inputGroupFile03");

let auth = false

let output = document.getElementById('output');

inputElement.addEventListener("change", handleFiles, false);

let fileList
let upload = 0
// Функция загружает изображение в предосмотр
function handleFiles() {

  try {
    fileList = this.files;

    if (upload === 0) {
      console.log(fileList[0]);
      if (fileList[0].size > 990000) {
        console.log('много');
        inputElement.value = ""
        document.querySelector('.big-image').classList.add('big-image_alert')
        document.querySelector('.al-imag ').innerHTML = 'Изображение не должно превышать 10 Mb !'
        setTimeout(() => {
          document.querySelector('.big-image').classList.remove('big-image_alert')
        }, 2000);
      }
      else if (!["image/jpeg", "image/jpg", "image/png"].includes(fileList[0].type)) {
        inputElement.value = ""
        document.querySelector('.big-image').classList.add('big-image_alert')
        document.querySelector('.al-imag ').innerHTML = 'Только форматы jpg, jpeg или png !'
        setTimeout(() => {
          document.querySelector('.big-image').classList.remove('big-image_alert')
        }, 2000);
      }
      else {
        console.log(2);
        output.src = URL.createObjectURL(this.files[0]);
        let result_count = document.querySelector('.text-result_count')
        result_count.classList.remove('send-rescount')
      }
    }

  } catch (error) {
    console.log('нет класаа');
  }


}

// Функция загружает отправляет  изображение на сервер
async function uploadImage() {
  if (localStorage.getItem('google_id')) {
    if (fileList && fileList[0]) {
      let alerts = document.getElementById('succes_upload')
      let formData = new FormData();
      formData.append("image", fileList[0], fileList[0].name);
      document.querySelector('.send-load').classList.add('send-load-true')
      document.querySelector('.send').classList.add('send-text')

      fetch(`http://${debug_path}/api/v1/pictures/uploadimages/${localStorage.getItem('google_id')}`, {
        method: 'post',
        body: formData,

      }).then(function (response) {
        return response.json();
      }).then(function (data) {
        if (data.asses) {
          if (data.message) {
            alerts.classList.add("succes_upload-true");
            document.querySelector('.send-load').classList.remove('send-load-true')
            document.querySelector('.send').classList.remove('send-text')
            setTimeout(() => {
              alerts.classList.remove("succes_upload-true");
            }, 2000);
            document
            inputElement.value = ""
            upload = 1
            let result_count = document.querySelector('.text-result_count')
            result_count.innerHTML = `Обработано 0/10 часть изображения`
            result_count.classList.add('send-rescount')
            // output.src = ""
          }
          else {
            document.querySelector('.send-load').classList.remove('send-load-true')
            document.querySelector('.send').classList.remove('send-text')
            alerts.classList.remove("succes_upload-true");
            inputElement.value = ""
            output.src = ""
            document.querySelector('.limit-images').classList.add('succes_upload-true')
            setTimeout(() => {
              document.querySelector('.limit-images').classList.remove('succes_upload-true')
            }, 3000);
          }
        }
        else {
          inputElement.value = ""
          if (upload = 0) {
            output.src = ""
          }
          document.querySelector('.send-load').classList.remove('send-load-true')
          document.querySelector('.send').classList.remove('send-text')
          document.querySelector('.asses-images').classList.add('succes_upload-true')
          setTimeout(() => {
            document.querySelector('.asses-images').classList.remove('succes_upload-true')
          }, 3000);
        }
        document.querySelector('.count-images').innerHTML = `загружено за 24 часа  ${data.limit}`
      });
    }
    else {
      document.querySelector('.not-image').classList.add('succes_upload-true')
      setTimeout(() => {
        document.querySelector('.not-image').classList.remove('succes_upload-true')
      }, 2000);
    }
  }
  else {
    document.querySelector('.not-auth').classList.add('succes_upload-true')
    setTimeout(() => {
      document.querySelector('.not-auth').classList.remove('succes_upload-true')
    }, 2000);
  }
}

// google auth  sign in

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  let data = {
    "id_google_client": profile.getId(),
    "email": profile.getEmail(),
    "password": "",
    "access": true,
    "spent_day_limit": 0
  }
  // отправка на сервер данных гугл
  fetch(`http://${debug_path}/api/v1/users/`, {
    method: 'post',
    body: JSON.stringify(data),
    headers: headers
  }).then(function (responce) {
    return responce.json();
  }).then(function (data) {
    document.querySelector('.count-images').innerHTML = `
    загружено за 24 часа  ${data.user_data.spent_day_limit}/5
    `
    localStorage.setItem('google_id', data.user_data.id_google_client);
    localStorage.setItem('access_token', data.access_token);
    document.querySelector('.true-auth').classList.add('succes_upload-true')
    onwssocket()

    document.querySelector('.text-al').innerHTML = `Привет,${profile.getName()}`
    setTimeout(() => {
      document.querySelector('.true-auth').classList.remove('succes_upload-true')
    }, 2000);
  });
  document.querySelector('.g-signin2').classList.add('g-signintrue')
  document.querySelector('.exit-google').classList.add('exit-googlesign')
}

// google sign out
function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
    localStorage.removeItem('google_id');
    document.querySelector('.g-signin2').classList.remove('g-signintrue')
    document.querySelector('.exit-google').classList.remove('exit-googlesign')
  });
}
