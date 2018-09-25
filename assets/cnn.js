// instantiate the uploader

(function($) {

    Dropzone.options.mydropzone = {
      paramName: "origin", // The name that will be used to transfer the file
      maxFilesize: 1, // MB
      thumbnailWidth: 150,
      thumbnailHeight: 150,
      timeout: 600000,
      dictDefaultMessage: "Drop a photo or click here",

      init: function() {
        this.on("addedfile", function() {
          if (this.files[1]!=null){
            this.removeFile(this.files[0]);
          }
        });
      }
    };

})(jQuery);