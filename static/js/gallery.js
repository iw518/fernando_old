function uploadFiles(formId, selectId, galleryId, submitId) {
  var form = document.getElementById(formId);
  var selectInput = document.getElementById(selectId);
  var gallery = document.getElementById(galleryId);
  var submitBtn = document.getElementById(submitId);

  selectInput.addEventListener(
    'change',
    function() {
      //若gallery有子节点，删除所有子节点
      while (gallery.hasChildNodes()) //当div下还存在子节点时 循环继续
      {
        gallery.removeChild(gallery.firstChild);
      }

      for (var i = 0; i <= this.files.length - 1; i++) {
        var file = this.files[i];
        previewImage(file, gallery);
      }
    },
    false
  );

  submitBtn.addEventListener(
    'click',
    function() {
      var xhr = new XMLHttpRequest();
      var form_data = new FormData(form);
      xhr.open("POST", selectInput.getAttribute("action"));
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
          console.log(xhr.responseText); // handle response.
        }
      };
      xhr.send(form_data);
    });

  // ajax方法
  // submitBtn.addEventListener(
  //   'click',
  //   function() {
  //     // 因为new FormData的参数需要一个HTMLElement类型的数据，而jQuery得到的是个HTMLElement的集合，哪怕只有一个元素。所以需要用[]取其第一个元素。
  //     //var form_data = new FormData($('#upload-file')[0]);
  //     var form_data = new FormData(form);
  //     $.ajax({
  //       type: 'POST',
  //       data: form_data,
  //       contentType: false,
  //       cache: false,
  //       processData: false,
  //       success: function(data) {
  //         console.log('Uploading Success!');
  //       },
  //     });
  //   });
}

function previewImage(file, parent) {
  var imageType = /image.*/;
  if (!file.type.match(imageType)) {
    throw "File Type must be an image";
  }
  var thumb = document.createElement("div");
  thumb.classList.add('col-sm-2');
  thumb.classList.add('thumbnail'); // Add the class thumbnail to the created div
  var img = document.createElement("img");
  img.file = file;
  thumb.appendChild(img);
  parent.appendChild(thumb);

  // Using FileReader to display the image content
  var reader = new FileReader();
  reader.onload = (function(aImg) {
    return function(e) {
      aImg.src = e.target.result;
    };
  })(img);
  reader.readAsDataURL(file);

  var note = document.createElement("input");
  note.setAttribute("type", "text");
  note.setAttribute("name", "note");
  thumb.appendChild(note);

  var checkbox = document.createElement("input");
  checkbox.setAttribute("type", "Checkbox");
  checkbox.checked = true;
  var check = document.createElement("div");
  check.appendChild(checkbox);
  thumb.appendChild(check);

  // This code is only for demo ...
  console.log("name : " + file.name);
  console.log("size : " + file.size);
  console.log("type : " + file.type);
  console.log("date : " + file.lastModified);
}