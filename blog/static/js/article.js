var postId = -1;
var hasThisUserLiked = 0;
var userFullName = null;
var hasProfilePic = false;
var profilePicName = null;
var userSlug = null;
var commentsCnt = 0;

function init(p_postId, p_hasThisUserLiked, p_name, p_hasDp, p_dpName, p_userSlug, u_commentsCnt){
    postId = p_postId;
    hasThisUserLiked = p_hasThisUserLiked;
    userFullName = p_name;
    console.log("USER FULL NAME "+userFullName);
    if(p_hasDp == "True"){
        hasProfilePic = true;
        profilePicName = p_dpName;
    }
    userSlug = p_userSlug;
    commentsCnt = u_commentsCnt;
}
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
var csrfToken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
var csrfToken = getCookie('csrftoken');
$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            //console.log("BEFORE SEND METHOD");
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
});


$("#commentBtn").click(function(){

    cmt = $("#commentTextArea").val();
    /*
    new_elem = "<h4>Vishal Khopkar</h4><p>Recently, India inaugurated a road to Chinese border for Kailash Manasarovar pilgrims, passing through Lipulekh Pass, a territory disputed between India and Nepal which led to Nepal reissuing maps marking</p>"
    $("#comments").append(new_elem);
    */
    data = {
        postId: postId,
        comment: cmt
    }
    $.ajax({
        url: "/comment",
        method: "POST",
        data: data,
        success: function(response){
            if(response.result == "OK"){
                var imgPath = "static/img/badge.png";
                if(hasProfilePic){
                    imgPath = "static/img/user/"+userSlug+"/"+profilePicName;
                }
                commentsCnt++;
                new_elem = '<div id="commentAuthor'+response.id+'" class="comment-author"><img src="'+imgPath+'" width="30" height="30"/><h4 style="display: inline-block;">&nbsp;<a href="/user/'+userSlug+'" target="_blank">'+userFullName+'</a></h4><br/></div><div id="commentText'+response.id+'" class="comment-text"><p>'+cmt+'</p><h6><a onClick="editComment($(this), '+response.id+')" href="javascript:void(0);">Edit</a>&nbsp;&nbsp;<a onclick="deleteComment($(this), '+response.id+')" href="javascript:void(0);">Delete</a></h6><hr/></div>';
                $("#comments").append(new_elem);
                $("#commentTextArea").val("");
                $("#commentsCnt").html(commentsCnt);
                goToComment(response.id);
                $("#charCount").html("0");
            }
            else{
                alert("Comment length should be upto 500 characters");
            }

        }
    })
});

function goToComment(commentNo){
    currLoc = window.location.href;
    var newLoc = "";
    if(currLoc.includes("#")){
        newLoc = currLoc.split("#")[0];

    }
    else{
        newLoc = currLoc;
    }
    window.location.href = newLoc + "#commentAuthor"+commentNo;
}

function like(type){
    data = {
        postId: postId,
        type: type
    };
    var result;
    $.ajax({
        url: "/like",
        method: "POST",
        data: data,
        success: function(response){
            // here hasThisUserLiked holds the initial value, type holds the new value
            /*
                there are six possibilities
                hasThisUserLiked    type
                0                   1
                0                   -1
                1                   0
                1                   -1
                -1                  0
                -1                  1
            */
            changeButtonColours(hasThisUserLiked, type);
            hasThisUserLiked = type;
            result = true;

        }
    })

    return result;
}

function changeButtonColours(previousType, type){
    if(type == 0){
        // unliked or un-disliked
        console.log("UN-LIKE/UN-DISLIKE SUCCESSFUL");
        $("#likeBtn").attr("class","like-dislike-btn btn btn-sm btn-success");
        $("#dislikeBtn").attr("class","like-dislike-btn btn btn-sm btn-danger");
        if(previousType == 1){
            // previously liked, now un-liked
            orgNoOfLikes = parseInt($("#noOfLikes").html());
            $("#noOfLikes").html(orgNoOfLikes - 1);
        }
        else{
            // previously disliked, now un-disliked
            orgNoOfDislikes = parseInt($("#noOfDislikes").html());
            $("#noOfDislikes").html(orgNoOfDislikes - 1);
        }
    }
    else if(type == 1){
        // liked
        console.log("LIKE SUCCESSFUL");
        $("#likeBtn").attr("class","blue-like-dislike like-dislike-btn btn btn-sm btn-success");
        $("#dislikeBtn").attr("class","like-dislike-btn btn btn-sm btn-danger");
        if(previousType == 0){
            // previously no like or dislike, now liked
            orgNoOfLikes = parseInt($("#noOfLikes").html());
            $("#noOfLikes").html(orgNoOfLikes + 1);

        }
        else{
            // previously disliked, now liked
            orgNoOfLikes = parseInt($("#noOfLikes").html());
            $("#noOfLikes").html(orgNoOfLikes + 1);

            orgNoOfDislikes = parseInt($("#noOfDislikes").html());
            $("#noOfDislikes").html(orgNoOfDislikes - 1);
        }
    }
    else{
        // type == -1
        console.log("DISLIKE SUCCESSFUL");
        $("#likeBtn").attr("class","like-dislike-btn btn btn-sm btn-success");
        $("#dislikeBtn").attr("class","blue-like-dislike like-dislike-btn btn btn-sm btn-danger");
        if(previousType == 0){
            // previously no like or dislike, now disliked
            orgNoOfDislikes = parseInt($("#noOfDislikes").html());
            $("#noOfDislikes").html(orgNoOfDislikes + 1);

        }
        else{
            // previously liked, now disliked
             orgNoOfDislikes = parseInt($("#noOfDislikes").html());
            $("#noOfDislikes").html(orgNoOfDislikes + 1);

            orgNoOfLikes = parseInt($("#noOfLikes").html());
            $("#noOfLikes").html(orgNoOfLikes - 1);
        }
    }
}

$("#likeBtn").click(function(){
    console.log(postId);
    var result;
    if(hasThisUserLiked == 1){
        // already liked, unlike now
        result = like(0);

    }
    else{
        // not liked, or disliked
        result = like(1);

    }
});
$("#dislikeBtn").click(function(){
    console.log(postId);
    var result;
    if(hasThisUserLiked == -1){
        // already disliked, unlike now
        result = like(0);

    }
    else{
        // not liked, or disliked
        result = like(-1);

    }
});

$("#commentTextArea").keyup(function(){
    charCount = $("#commentTextArea").val().length;
    $("#charCount").html(charCount);
    if(charCount > 500 || charCount == 0){
        $("#charCount").attr("style","color:red;");
        $("#commentBtn").attr("disabled", true);
    }
    else{
        $("#charCount").removeAttr("style");
        $("#commentBtn").removeAttr("disabled");
    }

});

function checkCountInEditCmt(id){
    charCount = $("#editCommentTextArea"+id).val().length;
    $("#editCharCount"+id).html(charCount);
    if(charCount > 500 || charCount == 0){
        $("#editCharCount"+id).attr("style","color:red;");
        $("#editCommentCnf"+id).attr("disabled", true);
    }
    else{
        $("#editCharCount"+id).removeAttr("style");
        $("#editCommentCnf"+id).removeAttr("disabled");
    }

}

function editComment(target, id){
    var grandfather = target.parent().parent();
    var orgCmt = grandfather.find('p').text().trim();

    //grandfather.html("");
    grandfather.find('p').attr("hidden", "true");
    grandfather.find('h6').attr("hidden", "true");
    new_elem1 = '<textarea id="editCommentTextArea'+id+'" onkeyup="checkCountInEditCmt('+id+')" class="form-control" rows="5" style="resize:none;">'+orgCmt+'</textarea><br/>';
    new_elem2 = '<button id="editCommentCnf'+id+'" onclick="editCommentCnf('+id+')" class="btn btn-success">Post</button><small style="text-align: right; float:right;"><span id="editCharCount'+id+'">'+orgCmt.length+'</span>/500</small>';
    new_elem3 = '<button style="margin-left: 5px;" onclick="cancelEditComment('+id+')" id="cancelEditComment'+id+'" class="btn btn-danger">Cancel</button>';
    grandfather.append(new_elem1);
    grandfather.append(new_elem2);
    grandfather.append(new_elem3);

}

function editCommentCnf(id){

    commentText = $("#editCommentTextArea"+id).val();
    console.log("ID "+id+" COMMENT TEXT "+commentText);
    data = {
        id: id,
        comment: commentText
    };

    $.ajax({
        url: "/editComment",
        method: "POST",
        data: data,
        success: function(response){
            if(response.result == "OK"){
                // comment updated successfully
                editCommentInHTML(id, commentText);
            }
            else{
                alert("Comment length should be upto 500 characters");
            }
        }
    });
}

function cancelEditComment(id){
    var elem = $("#commentText"+id);
    var elemClone = elem.clone();
    elem.empty();
    elem.append(elemClone.find('p'));
    elem.append(elemClone.find('h6'));
    elem.find('p').removeAttr("hidden");
    elem.find('h6').removeAttr("hidden");
}

function editCommentInHTML(id, comment){
    var elem = $("#commentText"+id);
    var elemClone = elem.clone();
    elem.empty();
    elem.append(elemClone.find('p'));
    elem.append(elemClone.find('h6'));
    elem.find('p').text(comment);
    elem.find('p').removeAttr("hidden");
    elem.find('h6').removeAttr("hidden");
}

function deleteComment(target, id){
    swal({
        title: "Are you sure you want to delete this comment?",
        text: $("#commentText"+id).find('p').text(),
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
            deleteCommentCnf(id);
        } else {
            console.log("NOT DELETED");
        }
    });
}

function deleteCommentCnf(id){
    console.log("Delete comment cnf "+id);
    data = {
        id: id
    };
    $.ajax({
        url: "/deleteComment",
        method: "POST",
        data: data,
        success: function(response){
            // comment successfully deleted
            $("#commentAuthor"+id).remove();
            $("#commentText"+id).remove();
            var prevCmtsCnt = parseInt($("#commentsCnt").html());
            $("#commentsCnt").html(prevCmtsCnt - 1);
        },
        error: function(response){
            swal("Could not delete comment", "There was some problem", "error");
        }
    });
}

$("#reportSubmit").click(function(){
    var reasons = "";
    $('input[name="reasonCheckbox"]:checked').each(function(){
        reasons += ("_"+this.id);
    });
    var comment = $("#reportComment").val().substring(0, 100);
    var data = {
        articleId: postId,
        reasons: reasons,
        comment: comment
    };
    console.log(data);
    $.ajax({
        url: "/reportArticle",
        method: "POST",
        data: data,
        success: function(response){
            swal("Thanks for reporting", "We will take any further action required", "success");
            $("#reportModal").modal("toggle");
        },
        error: function(response){
            swal("Could not report", "Please try again", "error");
        }
    });
});

$("#deleteArticle").click(function(){
    swal({
        title: "Are you sure you want to delete this article?",

        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
            deleteArticleCnf();
        } else {
            swal("Article not deleted");
        }
    });
});

function deleteArticleCnf(){
    var data = {
        articleId: postId
    };
    $.ajax({
        url: "/deleteArticle",
        method: "POST",
        data: data,
        success: function(response){
            swal({

                title: "Article successfully deleted",
                icon: "success",
                buttons: true,
            }).then((ev) =>{
                window.location.href = "/";
            });

        },
        error: function(response){
            swal("Could not delete", "Please try again", "error");
        }
    });
}

$("#editArticle").click(function(){
    var data = {
        articleId: postId
    };
});