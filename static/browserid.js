function setCookie(c_name, value, exdays) {
  var exdate = new Date();
  exdate.setDate(exdate.getDate() + exdays);
  var c_value = escape(value) + 
    ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
  document.cookie = c_name + "=" + c_value;
}

function browserid_login_callback(assertion){
  setCookie('browserid_assertion', assertion, 90);
  window.location.reload();
}
function browserid_login(){
  navigator.id.getVerifiedEmail(browserid_login_callback);
}
function browserid_logout(){
  setCookie('browserid_assertion', 'x', -30);
  window.location.reload()
}
