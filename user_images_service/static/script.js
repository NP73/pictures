const headers = {
  "Content-Type": "application/json",
};
const inputElement = document.getElementById("inputGroupFile03");

let auth = false

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
async function uploadImage() {
  if (localStorage.getItem('google_id')) {
    if (fileList && fileList[0]) {
      let alerts = document.getElementById('succes_upload')
      let formData = new FormData();
      formData.append("image", fileList[0], fileList[0].name);
      document.querySelector('.send-load').classList.add('send-load-true')
      document.querySelector('.send').classList.add('send-text')

      fetch(`http://localhost:8000/api/v1/pictures/uploadimages/${localStorage.getItem('google_id')}`, {
        method: 'post',
        body: formData,

      }).then(function (response) {
        return response.json();
      }).then(function (data) {
        if (data.message) {
          alerts.classList.add("succes_upload-true");
          document.querySelector('.send-load').classList.remove('send-load-true')
          document.querySelector('.send').classList.remove('send-text')
          setTimeout(() => {
            alerts.classList.remove("succes_upload-true");
          }, 2000);

          inputElement.value = ""
          output.src = ""
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
  fetch('http://localhost:8000/api/v1/users/', {
    method: 'post',
    body: JSON.stringify(data),
    headers: headers
  }).then(function (responce) {
    return responce.json();
  }).then(function (data) {
    document.querySelector('.count-images').innerHTML = `
    загружено за 24 часа  ${data.spent_day_limit}/5
    ` 
    localStorage.setItem('google_id', data.id_google_client);
    document.querySelector('.true-auth').classList.add('succes_upload-true')
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
