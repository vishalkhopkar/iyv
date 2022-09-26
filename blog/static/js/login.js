//var csrf_token = '3342';
function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var prevDoPasswordsMatch = false;
var prevHasMoreThanSixChars = false;
var prevHasNumeral = false;
var prevHasSpChar = false;

function passwordValidator(){
    var doPasswordsMatch = false;
    var hasMoreThanSixChars = false;
    var hasNumeral = false;
    var hasSpChar = false;

    password = $("#id_password").val();

    confirm_password = $("#id_confirm_password").val();

    if(password != confirm_password){
        doPasswordsMatch = false;
    }
    else{

        doPasswordsMatch = true;
    }
    if(password.length < 6 || /^[A-Za-z0-9&!@#%$]+/.test(password) == false){
        hasMoreThanSixChars = false;
    }
    else{
        hasMoreThanSixChars = true;
    }

    if(!password.match(/[0-9]/)){
        hasNumeral = false;
    }
    else{
        hasNumeral = true;
    }
    if(!password.match(/[&!@#%$]/)){
        hasSpChar = false;
    }
    else{
        hasSpChar = true;
    }

    if(prevDoPasswordsMatch != doPasswordsMatch){
        if(doPasswordsMatch){
            $("#matchSpan").attr("class", "glyphicon glyphicon-ok");
            $("#matchH").attr("class", "green-label");
        }
        else{
            $("#matchSpan").attr("class", "glyphicon glyphicon-remove");
            $("#matchH").attr("class", "red-label");
        }
        prevDoPasswordsMatch = doPasswordsMatch;
    }


    //check 6 or more chars
    if(prevHasMoreThanSixChars != hasMoreThanSixChars){
        if(hasMoreThanSixChars){
            console.log("OK");
            $("#sixMoreSpan").attr("class", "glyphicon glyphicon-ok");
            $("#sixMoreH").attr("class", "green-label");
        }
        else{
            $("#sixMoreSpan").attr("class", "glyphicon glyphicon-remove");
            $("#sixMoreH").attr("class", "red-label");
        }
        prevHasMoreThanSixChars = hasMoreThanSixChars;
    }

    if(prevHasNumeral != hasNumeral){
        if(hasNumeral){
            $("#numeralSpan").attr("class", "glyphicon glyphicon-ok");
            $("#numeralH").attr("class", "green-label");
        }
        else{
            $("#numeralSpan").attr("class", "glyphicon glyphicon-remove");
            $("#numeralH").attr("class", "red-label");
        }
        prevHasNumeral = hasNumeral;
    }

    if(prevHasSpChar != hasSpChar){
        if(hasSpChar){
            $("#spCharSpan").attr("class", "glyphicon glyphicon-ok");
            $("#spCharH").attr("class", "green-label");
        }
        else{
            $("#spCharSpan").attr("class", "glyphicon glyphicon-remove");
            $("#spCharH").attr("class", "red-label");
        }
        prevHasSpChar = hasSpChar;
    }
}
var csrfToken = getCookie('csrftoken');
$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            console.log("BEFORE SEND METHOD");
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
});
$(document).ready(function(){


    var referrer =  document.referrer;
    $(document).on("submit", "#login-form", function(e){
        //alert("REFERRER "+referrer);
        e.preventDefault();
        console.log("JS is working");
        data1 = {username: $("#username_lgn").val(), password: $("#password_lgn").val()}

        //var data1 = $("#login-form").serialize();
        console.log(data1);
        console.log(csrfToken)
        $.ajax({
              url: "/login.do",
              type: "POST",
              data: data1,
              success : function(response){
                    console.log(response);
                    if(response.result == "OK"){
                        console.log("NACH BALIYE");
                        window.location.href=referrer
                    }
              }
        });
    });

    $(document).on("click", "#logout-btn", function(e){
        e.preventDefault();
        console.log("LOGOUT");
        var data = {"username": "vishal"};
        $.ajax({
            url: "logout.do",
            type: "POST",

            data: data,
            success : function(response){
                console.log(response);
                if(response.result == "OK"){
                        console.log("NACH BALIYE");
                        //window.location.href=referrer
                }
            }
        });
    });


    $("#registerAreaLink").click(function(){

        $('#registerArea').show();
        $('#loginArea').hide();
        $("#loginLi").attr("class","");
        $("#registerLi").attr("class","active");
    });

    $("#loginAreaLink").click(function(){
        $('#registerArea').hide();
        $('#loginArea').show();
        $("#registerLi").attr("class","");
        $("#loginLi").attr("class","active");
    });

    $("#id_password").keyup(passwordValidator);
    $("#id_confirm_password").keyup(passwordValidator);

    $("#registerForm").submit(function(e){
        e.preventDefault();

        data = $("#registerForm").serialize();
        $.ajax({
            method: "POST",
            url: "/register",
            data: data,
            success: function(response){
                console.log(response);
                location.reload();
            },
            error: function(response){
                console.log(response);
            }
        });
    });

    $("#loginForm").submit(function(e){
        e.preventDefault();

        data = $("#loginForm").serialize();
        $.ajax({
            method: "POST",
            url: "/login",
            data: data,
            success: function(response){
                console.log(response);
                location.reload();
            },
            error: function(response){
                console.log(response);
            }
        });
    });
});

