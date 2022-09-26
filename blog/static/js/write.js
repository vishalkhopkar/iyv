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
var noOfReferences = 3;
tinymce.init({
        selector: 'textarea#writer',
        height: 1000,
        menubar: false,
        plugins: [
          'advlist autolink lists link image charmap print preview anchor',
          'searchreplace visualblocks code fullscreen',
          'insertdatetime media table paste code help wordcount'
        ],
        toolbar: 'undo redo | formatselect | ' +
        'bold italic | alignleft aligncenter ' +
        'alignright alignjustify | bullist numlist outdent indent | ' +
        ' image | ' +
        'removeformat | help',
        content_css: '//www.tiny.cloud/css/codepen.min.css',

        images_upload_handler: function (blobInfo, success, failure, progress){
            var xhr, formData;

            xhr = new XMLHttpRequest();
            xhr.withCredentials = false;
            xhr.open('POST', '/upload_img');

            xhr.upload.onprogress = function (e) {
              progress(e.loaded / e.total * 100);
            };

            xhr.onload = function() {
                var json;

                if (xhr.status < 200 || xhr.status >= 300) {
                    failure('HTTP Error: ' + xhr.status);
                    return;
                }

                json = JSON.parse(xhr.responseText);

                if (!json || typeof json.location != 'string') {
                    failure('Invalid JSON: ' + xhr.responseText);
                    return;
                }

                success(json.location);
            };
            formData = new FormData();
            formData.append('file', blobInfo.blob(), blobInfo.filename());
            // append CSRF token in the form data
            formData.append('_csrfToken', csrfToken);
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
            xhr.send(formData);

        }
});
$("#editorialSave").click(function(){
    //console.log(document.getElementById("writer_ifr").contentWindow.document.body.innerHTML);
    var myContent = tinymce.activeEditor.getContent();
    console.log(myContent);
    //TODO
});

$('#articleForm').on('keyup keypress', function(e) {
  var keyCode = e.keyCode || e.which;
  if (keyCode === 13) {
    e.preventDefault();
    return false;
  }
});

$("#editorialSubmit").click(function(){
    //document.getElementById("writer_ifr").contentWindow.document.body.innerHTML = "<p>Hello</p>";
    //$("#writer").val("<p>Hello</p>");
    var myContent = tinymce.activeEditor.getContent();
    var title = $("#title").val();
    if(myContent == "" || title == ""){
        alert("Please fill all the required fields");
        return;
    }

    var references = [];
    var tags = $("#tagsInput").val();

    // displayed like Amsterdam, fallow, Sourav Ganguly
    console.log(tags);

    $(".ref-value").each(function(){
        val = $(this).val();
        if(val != ""){
            references.push(val);
        }
    });
    console.log(references);
    data = {
        title: title,
        content: myContent,
        references: JSON.stringify(references),
        tags: tags
    };
    $.ajax({
        url: "/submitArticle",
        type: "POST",
        data: data,
        success : function(response){
            console.log(response);
            if(response.result == "OK"){
                console.log("NACH BALIYE");
                alert("/"+response.url);
                window.location.href = "/"+response.url;
            }
        },
        error: function(response){
            console.log(response);
        }

    });

});
$("#addRefBtn").click(function(){
    newRef =
    '<li class="reference-input"><div class="input-group "><input type="text" class="form-control ref-value" placeholder="Enter a reference"><span class="input-group-btn"><button class="delete-ref btn btn-success" onclick="removeReference(this);" type="button"><span class="glyphicon glyphicon-trash"></span></button></span></div></li>';
    $("#referenceArray").append(newRef);
    noOfReferences++;
});


$(function () {
  $('.import-url-btn').popover({
    container: 'body'
  })
})

function removeReference(currElem){
    console.log(currElem);
    var elem = $(currElem).parent().parent().parent();
    console.log(elem);
    elem.remove();
    noOfReferences--;
}
/*
var citynames = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: {
    url: '../static/json/citynames.json',
    filter: function(list) {
      return $.map(list, function(cityname) {
        return { name: cityname }; });
    }
  }
});
citynames.initialize();

$('input').tagsinput({
  typeaheadjs: {
    name: 'citynames',
    displayKey: 'name',
    valueKey: 'name',
    source: citynames.ttAdapter()
  }
});
*/


