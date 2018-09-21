// instantiate the uploader

(function($) {
    Dropzone.autoDiscover = false;
    $('#file-dropzone').dropzone({
        url: "/cnn/change/", // 드롭다운 시 업로드 되는 URL
        maxFilesize: 1, // 드롭다운 시 파일 크기
        paramName: "userfile", // input file="user_file"
        maxThumbnailFilesize: 1, // 섬네일 사이즈 인데 안보여 줄거니까 1정도
        previewsContainer: ".dropzone-previews", // 섬네일 보여주는 Container class
        init: function () {
            this.on('success', function (file, json) {
                // 파일이 서버에 업로드가 완료 되었 을때
                var res = JSON.parse(json);

                if (res.msg == 'OK') {
                    //만약에 response message 가 OK 라면
                    $(".upload-progress").hide();
                    $(".resize-image").show();
                    $(".image-preview").show();
                    $("#preview-img").attr("src", res.path);
                    $("#image-down").attr("filename", res.path);
                } else {
                    // 만약에 OK 가 아니라면???
                    $("#file-dropzone").show();
                    $(".upload-progress").hide();
                    alert(res.msg);
                }
                console.log(json);
            });

            this.on('addedfile', function (file) {
                $("#file-dropzone").hide();
                $(".upload-progress").show();
            });

            this.on('drop', function (file) {
                // 파일이 드롭되면Upload Progress 나와줘야 된다.
                $("#file-dropzone").hide();
                $(".upload-progress").show();
            });
        }
    });
})(jQuery);