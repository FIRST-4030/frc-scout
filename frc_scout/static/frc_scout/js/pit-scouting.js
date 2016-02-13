$("input[type=checkbox]").bootstrapSwitch({
                'offText': "NO",
                'onText': "YES",
                'size': 'large',
                'indeterminate': true
            });

            $(function() {
                if(window.location.hash) {
                    if(!isNaN(window.location.hash.substr(1))) {
                        $("#team_number").val(window.location.hash.substr(1));
                    }
                }
            });

            $(".set-indeterminate").click(function() {
                $(this).prev('.bootstrap-switch').find('input[type=checkbox]').bootstrapSwitch('indeterminate', true);
            });

            function getFormData() {
                var data = {}

                $.each($("#pit_scout_form").find('input, select').not('input[type=checkbox], input[type=file]'), function() {
                    if($(this).val() !== "") {
                        if(!isNaN($(this).val())) {
                            data[this.id] = parseFloat($(this).val());
                        } else {
                            data[this.id] = $(this).val();
                        }
                    }
                });

                $.each($("#pit_scout_form").find('input[type=checkbox]'), function() {
                    if(!$(this).bootstrapSwitch('indeterminate')) {
                        data[this.id] = $(this).bootstrapSwitch('state');
                    }
                })

                return data;
            }

            function clearForm() {
                $.each($("#pit_scout_form").find('input, select').not('input[type=checkbox]'), function() {
                    $(this).val("");
                });

                $.each($("#pit_scout_form").find('input[type=checkbox]'), function() {
                    $(this).bootstrapSwitch('indeterminate', true);
                })

                $("#toggle_modal")
                        .removeClass('success')
                        .addClass('primary')
                        .text("SELECT");

                $("#failure").hide();
            }

            /*
             Get the relative coordinates from start image
             */
            $("#auto_start_image").click(function (event) {
                var image = $(this);

                var xPosition = (event.pageX - image.offset().left) / image.width();
                var yPosition = (event.pageY - image.offset().top) / image.height();


                if(true) { //assume all locations are valid and that the scouter isnt an idiot.
                //i really don't want to deal with coordinates right now -_-
                    if(!confirm("Confirm autonomous starting location.")) {
                        return;
                    }

                    $("#auto_start_x").val(xPosition);
                    $("#auto_start_y").val(yPosition);
                    $("#autoStartModal").modal('hide');

                    $("#toggle_modal")
                            .removeClass('btn-primary')
                            .addClass('btn-success')
                            .html("<span class='glyphicon glyphicon-check'></span> Location set, click to edit.");
                } else {
                    alert("Invalid Location.");
                }
            });

            window.onbeforeunload = function() {
                if(Object.keys(getFormData()).length > 0) {
                    return "You've entered data into the form. Are you sure you want to reload the page?";
                }
            }

            function submitForm() {
                if($("#team_number").val() === "") {
                    window.scrollTo(0, 1);
                    $("#required_message").show();
                    return;
                }
                if(Object.keys(getFormData()).length > 1 || $("#robot_image").val() !== "") {

                    $("#submit_progress").show();
                    $("#submit_progress_bar").css('width', '20%');

                    $("#submit_button").button('loading');
                    postToImgur();
                } else {
                    window.scrollTo(0, 1);
                    $("#insufficient_message").show();
                }
            }

            function postToImgur() {
                if($("#robot_image")[0].files[0] == null){
                    
                }
                var formData = new FormData();
                formData.append("image", $("#robot_image")[0].files[0]);
                $.ajax({
                    url: "https://api.imgur.com/3/image",
                    type: "POST",
                    datatype: "json",
                    headers: {
                        "Authorization": "Client-ID 74944771f93ba86"
                    },
                    data: formData,
                    success: function(response) {
                        console.log(response);
                        $("#submit_progress_bar").css('width', '80%');
                        postFormData(response);
                    },
                    error: function(response) {
                        console.log(response);
                        $("#submit_progress_bar").css('width', '0%');
                        $("#failure").show();
                        postFormData(response);

                    },
                    cache: false,
                    contentType: false,
                    processData: false
                });
            }

            function postFormData(imageData) {
                var formData = getFormData();

                $.ajax({
                    url: '/scouting/pit/submit/',
                    type: "POST",
                    data: {
                        csrfmiddlewaretoken: $.cookie('csrftoken'),
                        data: JSON.stringify(formData),
                        image_data: JSON.stringify(imageData)
                    },
                    success: function() {
                        $("#submit_progress_bar").css('width', '100%');
                        window.setTimeout(function() {
                            $("#submit_button").button('reset');
                            clearForm();
                            window.scrollTo(0, 1);
                            $("#success_message").show();
                            $("#submit_progress").hide();
                        }, 2000);
                    },
                    error:function(response){
                        console.log(response);
                    }
                })

            }