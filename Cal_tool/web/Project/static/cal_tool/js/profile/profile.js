function reveal_password(p_id)
{
    $(p_id).attr("type", "text");
}

function hide_password(p_id)
{
    $(p_id).attr("type", "password");
}

function show_hide_password(p_id, p_revealer_id)
{
    $(p_revealer_id)
      .mouseenter(function()
      {
        reveal_password(p_id);
      })
      .mouseleave(function()
      {
        hide_password(p_id)
      });
}

function check_password_status()
{
    if (check_password_length($("#password1").val())
        && check_password_length($("#password2").val())
        && check_passwords_equal())
    {
        return true;
    }
    else if(check_passwords_equal() && $("#password1").val() === "")
        return true;
    else
    {
        return false;
    }
}

function check_passwords_equal()
{
    let pass1 = $("#password1").val();
    let pass2 = $("#password2").val();

    return pass1 === pass2;

}

// This function expects the value of the password field
function check_password_length(p_pass)
{
    if (p_pass.length >= 8)
        return true;
    return false;
}

function password_checker(p_pass_id)
{
    $(p_pass_id).keyup(function ()
    {
        let pass1 = $("#password1");
        let pass2 = $("#password2");
        if (check_passwords_equal())
        {
           if (check_password_length(pass1.val()) && check_password_length(pass2.val()))
           {
               // Set valid
               pass1.removeClass("invalid");
               pass1.addClass("valid");
               pass2.removeClass("invalid");
               pass2.addClass("valid");
               $("#label_password1").html("Wachtwoord");
               $("#label_password2").html("Herhaal wachtwoord");
           }
           else
           {
               // Set invalid and error message
               pass1.removeClass("valid");
               pass1.addClass("invalid");
               pass2.removeClass("valid");
               pass2.addClass("invalid");
               $("#label_password1").html("<span class='red-text'>Gebruik minstens 8 characters.</span>");
               $("#label_password2").html("<span class='red-text'>Gebruik minstens 8 characters.</span>");
           }
        }
        else if (pass1.val() === "" && pass1.val() === ""){
            // Set valid
            pass1.removeClass("invalid");
            pass1.addClass("valid");
            pass2.removeClass("invalid");
            pass2.addClass("valid");
            $("#label_password1").html("Wachtwoord");
            $("#label_password2").html("Herhaal wachtwoord");
        }
        else
        {
            // Set invalid and error message
            pass1.removeClass("valid");
            pass1.addClass("invalid");
            pass2.removeClass("valid");
            pass2.addClass("invalid");
            $("#label_password1").html("<span class='red-text'>De wachtwoorden komen niet overeen.</span>");
            $("#label_password2").html("<span class='red-text'>De wachtwoorden komen niet overeen.</span>");
        }
    });
}

function trigger_tooltip(p_id)
{
    $(p_id).trigger("mouseenter.tooltip");

}

function untrigger_tooltip(p_id)
{
    $(p_id).trigger("mouseleave.tooltip");

}

function show_hide_tooltip(p_id)
{
    $(p_id)
      .focusin(function()
      {
        trigger_tooltip(p_id);
      })
      .focusout(function()
      {
        untrigger_tooltip(p_id)
      });
}

function uname_checker()
{
    $("#uname").change(function ()
    {
        check_uname();
    });
}

function check_uname()
{
    let uname = $("#uname");
    if (uname.attr("value") === uname.val()){
        uname.removeClass("invalid");
        uname.addClass("valid");
        $("#label_uname").html("Gebruikersnaam<span class='red-text'> *</span>");
    }
    else{
        $.ajax(
        {
            url: '/ajax/uname_checker/',
            data: {'uname': uname.val()},
            dataType: 'json',
            success: function (data)
            {
                if (! data.available)
                {
                    uname.removeClass("valid");
                    uname.addClass("invalid");
                    $("#label_uname").html("<span class='red-text'>Deze gebruikersnaam is al in gebruik.</span>");
                }
                else
                {
                    uname.removeClass("invalid");
                    uname.addClass("valid");
                    $("#label_uname").html("Gebruikersnaam<span class='red-text'> *</span>");
                }
            }
        });
    }
}

function email_checker()
{
    $("#email").change(function ()
    {
        check_email();
    });
}

function check_email()
{
    let email = $("#email");
    if (email.val() === "" || email.attr("value") === email.val()){
        email.removeClass("invalid");
        email.addClass("valid");
        $("#label_email").html("Email");
    }
    else {
        $.ajax(
        {
            url: '/ajax/email_checker/',
            data: {'email': email.val()},
            dataType: 'json',
            success: function (data)
            {
                if (! data.available)
                {
                    email.removeClass("valid");
                    email.addClass("invalid");
                    $("#label_email").html("<span class='red-text'>Dit emailadres is al in gebruik.</span>");
                }
                else
                {
                    email.removeClass("invalid");
                    email.addClass("valid");
                    $("#label_email").html("Email");
                }
            }
        });
    }
}

function checker_slacktoken()
{
    $("#slacktoken").change(function ()
    {
        $("#slacktoken").removeClass("invalid");
        $("#slacktoken").addClass("valid");
        $("#label_slacktoken").html("Slacktoken");
    });
}

function checker_slackchannel()
{
    $("#slackchannel").change(function ()
    {
        $("#slackchannel").removeClass("invalid");
        $("#slackchannel").addClass("valid");
        $("#label_slackchannel").html("Slackchannel");
    });
}

function delete_profile(evt)
{
    evt.preventDefault();
    if(confirm("Sure you want to delete your account?")) {
        $.ajax(
            {
                url: '/ajax/delete_profile/',
                dataType: 'json'
            });
        window.location = $("#delete_button").attr('href');
    }
}

function submit_handler()
{
    $("#registration_form").submit(function (evt)
    {
        let uname = $("#uname");

        // Check uname
        check_uname();
        let uname_status = uname.hasClass("valid");

        // Check password
        let password_status = check_password_status();

        // Check email
        let email = $("#email");
        check_email();
        let email_status = email.hasClass("valid");

        if (uname_status && password_status && email_status){

        }
        else
            evt.preventDefault();
    });

}

// TODO:: Add domain checking

$(document).ready(function()
{
    uname_checker();
    check_uname();
    email_checker();
    check_email();
    checker_slackchannel();
    checker_slacktoken();

    password_checker("#password1");
    password_checker("#password2");

    show_hide_password("#password1", "#password1_revealer");
    show_hide_password("#password2", "#password2_revealer");

    show_hide_tooltip("#uname");
    show_hide_tooltip("#email");
    show_hide_tooltip("#domain_select_wrapper");

    submit_handler();
});