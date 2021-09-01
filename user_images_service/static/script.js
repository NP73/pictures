let ws
//
// const debug_path = 'localhost:8000'

const debug_path  = 'api-booking.ru'
let count_etap
function onwssocket() {
  ws = new WebSocket(`wss://${debug_path}/ws/${localStorage.getItem('google_id')}`);
  ws.onmessage = (event) => {
    let result = JSON.parse(event.data)
    if (result.close_result) {

      let result_count = document.querySelector('.text-result_count')
      result_count.classList.add('send-rescount')
      result_count.innerHTML = `обработка завершена`
      document.querySelector('.status').innerHTML = `Статус обработки: Завершена`
      upload = 0

    }
    else {

      console.log('линк добавлен', result.result_image);

      let result_count = document.querySelector('.text-result_count')
      result_count.classList.add('send-rescount')
      count_etap = result.count_res_image
      document.querySelector('.count_etap ').innerHTML = `Обработано: ${count_etap} из 10`
      result_count.innerHTML = `Обработано ${result.count_res_image}/10 часть изображения`
      output.classList.add('not-output')
      setTimeout(() => {
        output.classList.remove('not-output')
      }, 1000);
      output.src = result.result_image
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

      fetch(`https://${debug_path}/api/v1/pictures/uploadimages/${localStorage.getItem('google_id')}`, {
        method: 'post',
        body: formData,

      }).then(function (response) {
        return response.json();
      }).then(function (data) {
        document.querySelector('.text-al').innerHTML = `${data.message}`
        document.querySelector('.true-auth').classList.add('succes_upload-true')
        document.querySelector('.count-images').innerHTML = `загружено за 24 часа  ${data.user_data.spent_day_limit}/${data.user_data.day_limit}`
        if (!data.status) {
          if (upload === 0) {
            output.src = ""
            inputElement.value = ""
          }
          else {
            inputElement.value = ""
          }
          document.querySelector('.send-load').classList.remove('send-load-true')
          document.querySelector('.send').classList.remove('send-text')
        }
        else {
          upload = 1
          document.querySelector('.send-load').classList.remove('send-load-true')
          document.querySelector('.send').classList.remove('send-text')
          let result_count = document.querySelector('.text-result_count')
          result_count.innerHTML = `Обработано 0/10 часть изображения`
          result_count.classList.add('send-rescount')
        }
        setTimeout(() => {
          document.querySelector('.true-auth').classList.remove('succes_upload-true')
        }, 2000);

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
  fetch(`https://${debug_path}/api/v1/users/`, {
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
    localStorage.removeItem('access_token');

    document.querySelector('.g-signin2').classList.remove('g-signintrue')
    document.querySelector('.exit-google').classList.remove('exit-googlesign')
  });
}

function predImage() {
  let st
  let headers2 = {
    "Content-Type": "application/json",
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
  fetch(`https://${debug_path}/api/v1/pictures/status-image-process/pred`, {
    method: 'get',
    headers: headers2
  }).then(function (responce) {

    st = responce.status
    return responce.json();
  }).then(function (data) {
    if (st === 200) {
      console.log(data[0].id);
      let status
      if (data[0].status) {
        status = 'Завершен'
      }
      else {
        if (data[0].settings === data[0].result_dict) {
          status = 'Завершено'
        }
        else {
          status = 'В процессе'

        }

      }
      count_etap = data[0].result_dict.a
      document.querySelector('.status').innerHTML = `Статус обработки: ${status}`
      document.querySelector('.count_etap ').innerHTML = `Обработано: ${count_etap} из 10`
      document.querySelector('#upl-image').classList.add('upl-image')
      document.querySelector('.pred-image').classList.add('pred2')
    }
    else {
      document.querySelector('.true-auth').classList.add('succes_upload-true')
      document.querySelector('.text-al').innerHTML = `${data.detail}`
      setTimeout(() => {
        document.querySelector('.true-auth').classList.remove('succes_upload-true')
      }, 2000);
    }

  });


}

function onhome() {
  document.querySelector('#upl-image').classList.remove('upl-image')
  document.querySelector('.pred-image').classList.remove('pred2')
}