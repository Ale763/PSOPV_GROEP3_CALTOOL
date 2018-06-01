


class calendar {
    constructor(p_cal_id,p_color,p_events) {
        this.color = p_color;
        this.id = p_cal_id ;
        this.events= p_events;
    }

    get_id(){
        return this.id;
    }

    hide_calendar(fullcal){
        $(".event_id"+this.id).hide();
    }


    show_calendar(fullcal){
        $(".event_id"+this.id).show();
    }


    render_calendar(fullcal){

        var index = 0;
        for ( index = 0; index < this.events.length; index++) {
            var event = this.events[index];
             $(fullcal).fullCalendar( 'renderEvent', event , true);
        }
    }



    get_events(){
        return this.events;
    }

}


class calendarview {
    constructor(p_callview_id) {
        this.calendars = [];
        this.calview_id = p_callview_id;
    }

    get_calendars(){
        return this.calendars;
    }

    add_calendar(calendar){
        this.calendars.push(calendar);
    }



    show_cal(id){
        $(".event_id"+id).show();
    }


    hide_cal(id){
        $(".event_id"+id).hide();
    }

    set_visible_calendars(){
        var index = 0;
        for (  index = 0; index < this.calendars.length; index++) {
            this.set_status_calendar(this.calendars[index].get_id());
        }
    }

    set_status_calendar(id){
        var check = $('#'+id).val();


        if (check == "SHOW"){
            this.hide_cal(id);
        }
    }


    render_all_calendars(){
        var index = 0;
        for (  index = 0; index < this.calendars.length; index++) {
            this.calendars[index].render_calendar(this.calview_id);
        }

    }

    show_all_calendars(){
        var index = 0;
        for (  index = 0; index < this.calendars.length; index++) {
            this.calendars[index].show_calendar(this.calview_id);
        }

    }


    hide_all_calendars(){
        var index = 0;
        for (  index = 0; index < this.calendars.length; index++) {
            this.calendars[index].hide_calendar(this.calview_id);
        }

    }

    change_calendar(id){
        var check = $('#'+id).val();

        if (check == "SHOW"){
            this.show_cal(id)
            $('#'+id).val("HIDE");
        }
        else{
            this.hide_cal(id);
            $('#'+id).val("SHOW");
        }
    }


    render_calendar(id){

        var index = 0;
        for ( index = 0; index < this.calendars.length; index++) {
            this.calendars[index].render_calendar();

        }

    }

    select_all(){
        var check = $('#select_all').val();


        if (check == "SHOW"){
            var index;

            this.show_all_calendars();

            for ( index = 0; index < this.calendars.length; index++) {
                var id = change_cal(this.calendars[index].get_id());
                $(".event_id"+id).prop('checked', true);
            }
             $(select_all).val("HIDE");

        }

        else{
            var index;

            this.hide_all_calendars();

            for ( index = 0; index < this.calendars.length; index++) {
                var id = change_cal(this.calendars[index].get_id());
                $(".event_id"+id).removeAttr('checked');
            }

             $(select_all).val("SHOW");

        }

    }
}

function loadCalendar(CalendarView) {

    $('#calendarview').fullCalendar({

        themeSystem: 'standard',
        defaultView: 'agendaWeek', //Possible Values: month, basicWeek, basicDay, agendaWeek, agendaDay
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'agendaWeek,agendaDay,month,listWeek'
        },
        lang: 'nl',
        slotLabelFormat: "HH:mm",
        allDaySlot: false,
        nowIndicator: true,
        timezone: 'local'
    });

    CalendarView.render_all_calendars();
    CalendarView.hide_all_calendars();


    $('#cal_load_icon').remove();

    agenda = document.getElementsByClassName("calendarview")[0];
    Buttons = agenda.getElementsByTagName("button");


    var index = 0;

    for ( index ; index < Buttons.length; index++) {
        Buttons[index].onclick = function () {
            CalendarView.set_visible_calendars();
        }
        }




}



CalendarView = new calendarview("#calendarview");

function change_cal(id){
    CalendarView.change_calendar(id);
}


