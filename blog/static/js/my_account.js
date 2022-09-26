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
var noOfArticlePages = 0;
function setupArticlesPagination(){

    noOfArticlePages = Math.trunc(totalNoOfArticles/5);
    for(var i=1; i <= noOfArticlePages; i++){
        var elem = '<li><a class="clickable-link" onclick="articlesPaginationClick('+(i+1)+')" id="articlesPage'+(i+1)+'+">Page '+(i+1)+'</a></li>';
        $("#articlesPaginationUl").append(elem);
    }
}
var currentPage = 1;
function articlesPaginationClick(pageNo){

    $("#currentPage").html("Page "+pageNo+"&nbsp;<span class='caret'></span>");
    currentPage = pageNo;

    data = {
        user_id: $("#whomToFollow").text(),
        pageNo: pageNo
    };
    $.ajax({
        url: "/getArticlesOnPageNo",
        method: "GET",
        data: data,
        success: function(response){
            if(response.result == "OK"){
                console.log(response);
                articles = response.articles;
                $("#articlesList").html("");
                for(var i=0; i < articles.length; i++){
                    var elem =
                    '<li><div class="article-ref-outer-container"><div class="article-ref-first-container"><div class="article-ref-second-container" style="font-size: 120%;"><a href="/'+articles[i].name+'">'+articles[i].title+'</a><br/><small>'+articles[i].date_time+'</small></div></div></div></li>';
                    $("#articlesList").append(elem);
                }
            }
        },
        error: function(response){
            console.log(response);
        }

    });
}

var csrfToken = getCookie('csrftoken');
var totalNoOfArticles = 0;
var totalFollowers = 0;
var totalFollowing = 0;
var noOfFollowingPages = 1;
var noOfFollowerPages = 1;
// if myUserId is -1, it means not logged in
var myUserId = 0;
var thisUserId = 0;
var thisUserHasDp = false;
var thisUserSlug = "";
var imageBindUrl = "";
function passVariables(x, y, z, a, b, userSlug){

    totalFollowers = x;
    totalFollowing = y;
    totalNoOfArticles = z;
    myUserId = a;
    thisUserId = b;
    thisUserSlug = userSlug;
    imageBindUrl = '../static/img/user/'+thisUserSlug+'/dp.jpg';

    //thisUserHasDp = hasDp;
    //alert(myUserId+" "+thisUserId);
    setupArticlesPagination();
    noOfFollowingPages = Math.ceil(totalFollowing/3);
    noOfFollowerPages = Math.ceil(totalFollowers/3);
    setupFollPagination(noOfFollowingPages, 1);
    setupFollPagination(noOfFollowerPages, 2);

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

    password = $("#newPassword").val();

    confirm_password = $("#confirmNewPassword").val();

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
            $("#changeMatchSpan").attr("class", "glyphicon glyphicon-ok");
            $("#changeMatchH").attr("class", "green-label");
        }
        else{
            $("#changeMatchSpan").attr("class", "glyphicon glyphicon-remove");
            $("#changeMatchH").attr("class", "red-label");
        }
        prevDoPasswordsMatch = doPasswordsMatch;
    }


    //check 6 or more chars
    if(prevHasMoreThanSixChars != hasMoreThanSixChars){
        if(hasMoreThanSixChars){
            console.log("OK");
            $("#changeSixMoreSpan").attr("class", "glyphicon glyphicon-ok");
            $("#changeSixMoreH").attr("class", "green-label");
        }
        else{
            $("#changeSixMoreSpan").attr("class", "glyphicon glyphicon-remove");
            $("#changeSixMoreH").attr("class", "red-label");
        }
        prevHasMoreThanSixChars = hasMoreThanSixChars;
    }

    if(prevHasNumeral != hasNumeral){
        if(hasNumeral){
            $("#changeNumeralSpan").attr("class", "glyphicon glyphicon-ok");
            $("#changeNumeralH").attr("class", "green-label");
        }
        else{
            $("#changeNumeralSpan").attr("class", "glyphicon glyphicon-remove");
            $("#changeNumeralH").attr("class", "red-label");
        }
        prevHasNumeral = hasNumeral;
    }

    if(prevHasSpChar != hasSpChar){
        if(hasSpChar){
            $("#changeSpCharSpan").attr("class", "glyphicon glyphicon-ok");
            $("#changeSpCharH").attr("class", "green-label");
        }
        else{
            $("#changeSpCharSpan").attr("class", "glyphicon glyphicon-remove");
            $("#changeSpCharH").attr("class", "red-label");
        }
        prevHasSpChar = hasSpChar;
    }

    if(doPasswordsMatch && hasSpChar && hasNumeral && hasMoreThanSixChars){
        var currentPwd = $("#currentPassword").val();
        if(currentPwd.length > 0){
            $("#changePwdSubmit").removeAttr("disabled");
        }
    }
}
$("#newPassword").keyup(passwordValidator);
$("#confirmNewPassword").keyup(passwordValidator);

$("#logoutConfirm").click(function(){
    //logout function
    $.ajax({
        url : "/logout.do",
        method: "GET",
        success: function(){
            console.log("Logged out successfully");
            window.location.href = "/"
        },
        error: function(response){
            console.log(response);
        }
    });
});

$("#editProfileLink").click(function(){
    $("#editProfile").show();

    //hide all other divs
    $("#articles").hide();

    $("#followers").hide();
    $("#changePassword").hide();

    //link active
    $("#articlesLi").attr("class","nav-item");
    $("#editProfileLi").attr("class","nav-item active");
    $("#followersLi").attr("class","nav-item");
    $("#followingLi").attr("class","nav-item");
    $("#changePasswordLi").attr("class", "nav-item");

    $("#articlesLiMobile").attr("class","nav-item ");
    $("#editProfileLiMobile").attr("class","nav-item active");
    $("#followersLiMobile").attr("class","nav-item ");
    $("#followingLiMobile").attr("class","nav-item  ");
    $("#changePasswordLiMobile").attr("class", "nav-item");
});

$("#articlesLink").click(function(){
    $("#articles").show();

    //hide all other divs
    $("#editProfile").hide();

    $("#followers").hide();
    $("#changePassword").hide();

    //link active
    $("#articlesLi").attr("class","nav-item active");
    $("#editProfileLi").attr("class","nav-item");
    $("#followersLi").attr("class","nav-item");
    $("#followingLi").attr("class","nav-item");
    $("#changePasswordLi").attr("class", "nav-item");

    $("#articlesLiMobile").attr("class","nav-item active");
    $("#editProfileLiMobile").attr("class","nav-item ");
    $("#followersLiMobile").attr("class","nav-item ");
    $("#followingLiMobile").attr("class","nav-item  ");
    $("#changePasswordLiMobile").attr("class", "nav-item");
});

function renderToFoll(foll){
    // foll is an array
    $("#follUl").html("");

    for(var i= 0 ; i < foll.length; i++){
        var img_src = "";
        if(foll[i].dp == false){
            img_src = '../static/img/badge.png';
        }
        else{
            img_src = '../static/img/user/'+foll[i].slug+'/dp.jpg';
        }
        var elem =
        '<li class="foll-li"><div class="row"><div class="col-xs-4 col-sm-2 col-md-2 col-lg-2"><img src="'+img_src+'" width="60" height="60"/></div><div class="col-xs-8 col-sm-10 col-md-10 col-lg-10"><h5><a target="_blank" href="'+foll[i].slug+'">'+foll[i].name+'</a></h5><small>'+foll[i].followerCnt+' followers</small></div></div></li>';
        $("#follUl").append(elem);
    }
}
var currentFollPage = 1;
var currentActiveType = 0;
function follPaginationClick(pageNo, type){
    // type = 1 for following, type = 2 for follower
    $("#currentFollPage").html("Page "+pageNo+"&nbsp;<span class='caret'></span>");
    currentFollPage = pageNo;
    data = {
        pageNo: pageNo,
        type: type,
        user_id: thisUserId
    };
    $.ajax({
        url: "/getFollOnPageNo",
        method: "GET",
        data: data,
        success: function(response){
            if(response.result == "OK"){
                console.log(response);
                renderToFoll(response.foll);
            }

        },
        error: function(response){
            console.log(response);
        }
    })

}
function setupFollPagination(pages, type){
    for(var i=1; i <= pages; i++){
        var elem = '<li><a class="clickable-link" onclick="follPaginationClick('+i+','+type+')" id="follPage'+(i)+'+">Page '+(i)+'</a></li>';
        $("#follPaginationUl").append(elem);
    }
}
function followingLinkAction(){
    currentActiveType = 1;
    $("#follPagination").hide();

    $("#followers").show();
    $("#followingOrFollower").text("FOLLOWING "+totalFollowing);
    //hide all other divs
    $("#articles").hide();
    $("#editProfile").hide();

    $("#changePassword").hide();

    //link active
    $("#articlesLi").attr("class","nav-item");
    $("#editProfileLi").attr("class","nav-item");
    $("#followersLi").attr("class","nav-item");
    $("#followingLi").attr("class","nav-item   active");
    $("#changePasswordLi").attr("class", "nav-item");

    $("#articlesLiMobile").attr("class","nav-item");
    $("#editProfileLiMobile").attr("class","nav-item ");
    $("#followersLiMobile").attr("class","nav-item ");
    $("#followingLiMobile").attr("class","nav-item  active");
    $("#changePasswordLiMobile").attr("class", "nav-item");
    console.log("noOfFollowingPages "+noOfFollowingPages);
    // type = 1 for following
    if(noOfFollowingPages > 1){

        $("#follPagination").show();
    }

    follPaginationClick(1, 1);

}

function followersLinkAction(){
    currentActiveType = 2;
    $("#follPagination").hide();

    $("#followers").show();
    $("#followingOrFollower").text(totalFollowers+" FOLLOWERS");
    //hide all other divs
    $("#articles").hide();

    $("#editProfile").hide();
    $("#changePassword").hide();

    //link active
    $("#articlesLi").attr("class","nav-item");
    $("#editProfileLi").attr("class","nav-item");
    $("#followersLi").attr("class","nav-item  active");
    $("#followingLi").attr("class","nav-item");
    $("#changePasswordLi").attr("class", "nav-item");

    $("#articlesLiMobile").attr("class","nav-item");
    $("#editProfileLiMobile").attr("class","nav-item ");
    $("#followersLiMobile").attr("class","nav-item   active");
    $("#followingLiMobile").attr("class","nav-item");
    $("#changePasswordLiMobile").attr("class", "nav-item");

    console.log("noOfFollowerPages "+noOfFollowerPages);
    // type = 2 for follower
    if(noOfFollowerPages > 1){

        $("#follPagination").show();
    }

    follPaginationClick(1, 2);
}

$("#followingLink").click(function(){
    followingLinkAction();
});

$("#followersLink").click(function(){
    followersLinkAction();
});

$("#changePasswordLink").click(function(){
    $("#changePassword").show();

    //hide all other divs
    $("#articles").hide();

    $("#editProfile").hide();
    $("#followers").hide();

    //link active
    $("#articlesLi").attr("class","nav-item");
    $("#editProfileLi").attr("class","nav-item");
    $("#followersLi").attr("class","nav-item");
    $("#followingLi").attr("class","nav-item");
    $("#changePasswordLi").attr("class", "nav-item   active");

    $("#articlesLiMobile").attr("class","nav-item");
    $("#editProfileLiMobile").attr("class","nav-item ");
    $("#followersLiMobile").attr("class","nav-item");
    $("#followingLiMobile").attr("class","nav-item");
    $("#changePasswordLiMobile").attr("class", "nav-item   active");
});

// mobile links
$("#articlesLinkMobile").click(function(){
    $("#articles").show();
    $("#editProfile").hide();

    $("#followers").hide();
    $("#changePassword").hide();
    //link active
    $("#articlesLiMobile").attr("class","nav-item   active");
    $("#editProfileLiMobile").attr("class","nav-item");
    $("#followersLiMobile").attr("class","nav-item");
    $("#followingLiMobile").attr("class","nav-item");
    $("#changePasswordLiMobile").attr("class", "nav-item");

    $("#articlesLi").attr("class","nav-item    active");
    $("#editProfileLi").attr("class","nav-item");
    $("#followersLi").attr("class","nav-item");
    $("#followingLi").attr("class","nav-item");
    $("#changePasswordLi").attr("class", "nav-item");
});

$("#editProfileLinkMobile").click(function(){
    $("#articles").hide();

    //hide all other divs
    $("#editProfile").show();

    $("#followers").hide();
    $("#changePassword").hide();
    //link active
    $("#articlesLiMobile").attr("class","nav-item");
    $("#editProfileLiMobile").attr("class","nav-item  active");
    $("#followersLiMobile").attr("class","nav-item");
    $("#followingLiMobile").attr("class","nav-item");
    $("#changePasswordLiMobile").attr("class", "nav-item");

    $("#articlesLi").attr("class","nav-item");
    $("#editProfileLi").attr("class","nav-item   active");
    $("#followersLi").attr("class","nav-item");
    $("#followingLi").attr("class","nav-item");
    $("#changePasswordLi").attr("class", "nav-item");
});

$("#followingLinkMobile").click(function(){
    followingLinkAction();
});

$("#followersLinkMobile").click(function(){
    followersLinkAction();
});

$("#changePasswordLinkMobile").click(function(){
    $("#articles").hide();

    //hide all other divs
    $("#editProfile").hide();

    $("#followers").hide();
    $("#changePassword").show();
    //link active
    $("#articlesLiMobile").attr("class","nav-item");
    $("#editProfileLiMobile").attr("class","nav-item");
    $("#followersLiMobile").attr("class","nav-item");
    $("#followingLiMobile").attr("class","nav-item");
    $("#changePasswordLiMobile").attr("class", "nav-item   active");

    $("#articlesLi").attr("class","nav-item");
    $("#editProfileLi").attr("class","nav-item ");
    $("#followersLi").attr("class","nav-item");
    $("#followingLi").attr("class","nav-item");
    $("#changePasswordLi").attr("class", "nav-item  active");
});



var follow = function(){
    whomToFollow = $("#whomToFollow").text();
    data = {
        whomToFollow: whomToFollow
    };
    $.ajax({
        url : "/follow",
        method: "POST",
        data: data,
        success: function(response){
            console.log(response);
            if(response.result == "OK"){
                $("#followBtn").text("Unfollow");
                $("#followBtn").attr("class","btn btn-danger");

                // change badge numbers


                prevCnt = parseInt($("#followerCntBadge").text());
                $("#followerCntBadge").text(prevCnt + 1);
                totalFollowers++;



            }


        },
        error:function(response){
            console.log(response);
        }
    });
}

var unfollow = function(){
    whomToFollow = $("#whomToFollow").text();
    data = {
        whomToFollow: whomToFollow
    };
    $.ajax({
        url : "/unfollow",
        method: "POST",
        data: data,
        success: function(response){
            console.log(response);
            if(response.result == "OK"){
                $("#followBtn").text("Follow");
                $("#followBtn").attr("class","btn btn-success");
                //$("#unfollowBtn").attr("id","followBtn");

                prevCnt = parseInt($("#followerCntBadge").text());
                $("#followerCntBadge").text(prevCnt - 1);
            }

        },
        error:function(response){
            console.log(response);
        }
    });
}
$("#followBtn").click(function(){
    var button_txt = $(this).text();
    if(button_txt == "Follow"){
        follow();
    }
    else{
        unfollow();
    }

});

$("#aboutFollowing").click(function(){
    followingLinkAction();
});

$("#aboutFollowers").click(function(){
    followersLinkAction();
});

$("#articlesPrev").click(function(){
    // get current page
    //alert(currentPage);
    if(currentPage <= 1) return;
    articlesPaginationClick(currentPage - 1);
});

$("#articlesNext").click(function(){
    //last page
    //alert(currentPage+ " "+(noOfArticlePages + 1));
    if(currentPage >= noOfArticlePages + 1) return;
    articlesPaginationClick(currentPage + 1);
});

$("#follPrev").click(function(){
    if(currentFollPage <= 1) return;
    follPaginationClick(currentFollPage - 1, currentActiveType);
});

$("#follNext").click(function(){
    if(currentActiveType == 1 && currentFollPage >= noOfFollowingPages) return;
    if(currentActiveType == 2 && currentFollPage >= noOfFollowerPages) return;
    follPaginationClick(currentFollPage + 1, currentActiveType);
});

$("#editProfileSubmit").click(function(){
    var about = $("#about").val();
    var facebookUrl = $("#facebookProfileUrl").val();
    var linkedinUrl = $("#linkedinProfileUrl").val();
    var twitterUrl = $("#twitterProfileUrl").val();

    data = {
        about: about,
        facebookUrl: facebookUrl,
        linkedinUrl: linkedinUrl,
        twitterUrl: twitterUrl,
    };
    $.ajax({
        url: "/updateAdditionalInfo",
        method: "POST",
        data: data,
        success: function(response){
            if(response.result == "OK"){
                window.location.reload();
            }
        },
        error: function(){

        }

    });

});

$("#changePwdSubmit").click(function(){
    data = {
        currentPwd : $("#currentPassword").val(),
        newPwd : $("#newPassword").val(),
        confirmNewPwd : $("#confirmNewPassword").val()
    }
    $.ajax({
        url: "/updatePwd",
        method: "POST",
        data: data,
        success: function(response){

            if(response.result == "OK"){
                console.log(response);
            }
        }
    });
});


/*
basic.croppie('bind', {
	url: '../static/img/user/'+$("#userSlugDisplay").html()+'/dp_full.jpg'

});
*/


$('#editPhotoModal').on('shown.bs.modal', function(){
    basic.croppie('bind');

});

$("#editPhotoOk").click(function(){
    basic.croppie('result', {
				type: 'canvas',
				size: {
				    width: 100,
				    height: 100
				},
				resultSize: {
					width: 50,
					height: 50
				}
			}).then(function (resp) {
				sendDpToBackend(resp);
			});
});

function sendDpToBackend(image){
    data = {
        image_data_url : image
    }

    $.ajax({
        url: "/upload_img_data",
        method: "POST",
        data: data,
        success: function(response){
            //alert($("#profilePic").attr());
            $("#profilePic").attr("src", "../static/img/user/"+$('#userSlugDisplay').html()+"/dp.jpg");
            $("#editPhotoModal").modal("toggle");
            window.location.reload(true);
        },
        error: function(response){

        }
    })
}

$("#chooseFile").on("change", function(){
    file = $(this)[0].files[0];
    fd = new FormData();
    fd.append("file", file);
    fd.append("type", 1);
    data = {
        file: fd,
        type: 1
    };
    console.log(fd);
    $.ajax({
        url: "/upload_img",
        method: "POST",
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            basic = $('#cropper').croppie({
                viewport: {
                    width: 200,
                    height: 200,
                    type: 'circle'
                },
                boundary: {
                    width: 300,
                    height: 300
                }
            });
            basic.croppie('bind',{
                url: '../static/img/user/'+$("#userSlugDisplay").html()+'/dp_full.jpg'

            });
        }
    });
});




