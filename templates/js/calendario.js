$(document).ready(function() {
    $('#calendar').fullCalendar({
    header: {
    left: 'prev,next today',
    center: 'title',
    right: 'month,agendaWeek,agendaDay,listWeek'
    },
    defaultDate: '2018-10-05',
    editable: true,
    navLinks: true, // can click day/week names to navigate views
    eventLimit: true, // allow "more" link when too many events
    events: {
        url: '/agenda',
        error: function() {
        $('#script-warning').show();
        }
    },
    loading: function(bool) {
        $('#loading').toggle(bool);
    }
    });
});