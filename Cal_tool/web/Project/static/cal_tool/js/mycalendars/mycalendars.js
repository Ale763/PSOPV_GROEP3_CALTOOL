
class ShareCalendar {

    constructor(){
        this.cal_id=-1;
    }

    load_url(p_calendar_id){
        let url = "";
        $.ajax({
        url: '/ajax/share_url/',
        data: {
          'email': "",
          'id': p_calendar_id,
          'password': ""
        },
            type: "post",
        dataType: 'json',
        success: function (result) {
                if(result!=""){
                    $("#link").text(result);
                }
            }
        });
    }

    load_emails(p_calendar_id){
        $.ajax({
        url: '/ajax/share_emails/',
        data: {
          'id': p_calendar_id
        },
            type: "post",
        dataType: 'json',
        success: function (result) {
                newSharedCalendar.load_emails_in_HTML(result);
            }
        });
    }

    load_emails_in_HTML(p_emails){
        $("#share_emails").empty();
        if(p_emails.length > 0){
            for(var i = 0; i<p_emails.length;++i) {
                $("#share_emails").append("<li id='sharedEmail"+i.toString()+"' style='margin-top: 5px'>"+p_emails[i]+"<i class='material-icons iconButton right sourceDelete deleteFilter' onclick='newSharedCalendar.delete_email("+i.toString()+")' style='margin-top: 15px;'>delete</i></li>");
            }
        }
        else {
            $("#share_emails").text("Deze kalender wordt met geen enkel emailadres gedeeld.");
        }
    }

    load_shared_data(p_calendar_id){
        this.cal_id=p_calendar_id;
        this.load_url(p_calendar_id);
        this.load_emails(p_calendar_id);
    }

    add_shared_email(){
        let mail = $("#shareEmail").val();
        if(mail.indexOf("@") < 0 || !mail.indexOf(".") < 0)
            return;

        $.ajax({
            url: '/ajax/add_shared_emails/',
            type: "post",
            data: {
                'id': this.cal_id,
                'shareEmail': mail
            },
        dataType: 'json',
        success: function (result) {
                console.log(result);
            }
        });
        this.load_emails(this.cal_id);
    }

    delete_email(p_id){
        let email = $("#sharedEmail"+p_id.toString()).html().split('<')[0];
        $.ajax({
            url: '/ajax/delete_shared_email/',
            data: {
              'id': this.cal_id,
              'shareEmail': email
            },
            type: "post",
            dataType: 'json',
            success: function (result) {}
        });
        this.load_emails(this.cal_id);
    }
}

function delete_calendar(p_calendar_id){

    var answer = confirm("Weet u zeker dat u deze agenda wilt verwijderen!");
    if (answer == true) {
        $.ajax({
            url: '/ajax/delete_calendar/',
            data: {
              'id': p_calendar_id
            },
            type: "post",
            dataType: 'json',
            success: function (result) {}
        });

        $("#calendar"+p_calendar_id.toString()).replaceWith("Agenda succesvol verwijderd!");
        CalendarView.hide_cal(p_calendar_id);

    }
}

function check_houres_filter(p_calendar_id){
    let value = $("#filter_value").val();
    $.ajax({
        url: '/ajax/check_houres_filter/',
        data: {
          'id': p_calendar_id,
          'filter_value': value
        },
        type: "post",
        dataType: 'json',
        success: function (result) {alert("Je hebt in totaal "+result.toString()+" uren gewerkt aan: "+value)}
    });
}



$(document).ready(function ()
{
    $('.modal').modal();
    $("#sharingPopUp select").material_select();



});


newSharedCalendar = new ShareCalendar();



