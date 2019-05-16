  $(document).ready(function() {
    $('#contact_form').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            organizer_ico: {
                validators: {
                        stringLength: {
                        min: 2,
                    },
                        notEmpty: {
                        message: 'Vyplňte svoje IČO'
                    }
                }
            },
             organizer_dic: {
                validators: {
                     stringLength: {
                        min: 5,
                    },
                    notEmpty: {
                        message: 'Vyplňte svoje DIČ'
                    }
                }
            },
			 organizer_name: {
                validators: {
                     stringLength: {
                        min: 1,
                    },
                    notEmpty: {
                        message: 'Vyplňte meno organizátora'
                    }
                }
            },
          
          		 user_name: {
                validators: {
                     stringLength: {
                        min: 8,
                    },
                    notEmpty: {
                        message: 'Vložte svoje uživatelské jméno'
                    }
                }
            },
          
			 organizer_password: {
                validators: {
                     stringLength: {
                        min: 8,
                    },
                    notEmpty: {
                        message: 'Vložte heslo'
                    }
                }
            },
			organizer_password_confirmed: {
                validators: {
                     stringLength: {
                        min: 8,
                    },
                    notEmpty: {
                        message: 'Vložte potvrzené heslo'
                    }
                }
            },
            organizer_email: {
                validators: {
                    notEmpty: {
                        message: 'Vožte emailovu adresu'
                    },
                    emailAddress: {
                        message: 'Vložte platnú emailovu adresu'
                    }
                }
            },
            organizer_phone: {
                validators: {
                  stringLength: {
                        min: 14, 
                        max: 14,
                    notEmpty: {
                        message: 'Vložte svoje telefónni číslo'
                     }
                }
             
            },
			 department: {
                validators: {
                    notEmpty: {
                        message: 'Please select your Department/Office'
                    }
                }
            },
                }
            }
        })
        .on('success.form.bv', function(e) {
            $('#success_message').slideDown({ opacity: "show" }, "slow") // Do something ...
                $('#contact_form').data('bootstrapValidator').resetForm();

            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data
            $.post($form.attr('action'), $form.serialize(), function(result) {
                console.log(result);
            }, 'json');
        });
});