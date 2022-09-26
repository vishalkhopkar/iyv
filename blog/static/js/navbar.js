var username = null;
function init(p_username){
    username = p_username;
}

$(document).ready(function(){


    $("#faqButton").click(function(){

        window.location.href = "/faq";
    });
    $("#connectButton").click(function(){
        currLoc = window.location.href;
        var newLoc = "";
        if(currLoc.includes("#")){
            newLoc = currLoc.split("#")[0];

        }
        else{
            newLoc = currLoc;
        }
        window.location.href = newLoc + "#connectFooter";
    });
    $("#readButton").click(function(){

        window.location.href = "/write";
    });
    $("#writeButton").click(function(){
        console.log(username);
        if(username == null || username == "None"){
            console.log("USERNAME IS NULL");
            swal("Please login first");
            $("#loginModal").modal();
        }
        else{
            window.location.href = "/write";
        }

    });



});