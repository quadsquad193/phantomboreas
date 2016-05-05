Utils = (function() {
    var human_date = function(timestamp) {
        var date = new Date(timestamp * 1000);

        var year        = date.getFullYear();
        var month       = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][date.getMonth()];
        var day         = date.getDate();

        return month + ' ' + day + ', ' + year;
    };


    var human_timestamp = function(timestamp) {
        date = new Date(timestamp * 1000);

        hours       = date.getHours();
        minutes     = "0" + date.getMinutes();
        period      = (hours < 12) ? 'AM' : 'PM';
        adjusted_hours = (hours == 0) ? 12 : ((hours > 12) ? hours - 12 : hours);

        return human_date(timestamp) + ' — ' + adjusted_hours + ':' + minutes.substr(-2) + ' ' + period;
    };


    var midnight_x_days_ago = function(x) {
        var date = new Date();

        return new Date(
            date.getTime() - 
            (date.getHours() * 60 * 60 * 1000) - 
            (date.getMinutes() * 60 * 1000) - 
            (date.getSeconds() * 1000) - 
            ((x-1) * 24 * 60 * 60 * 1000)
        );
    };

    var date_x_days_from_y = function(x, y) {
        return human_date(Math.floor(y.getTime() / 1000) + (x*24*60*60));
    };

    return {
        time: {
            human_timestamp: human_timestamp,
            midnight_x_days_ago: midnight_x_days_ago,
            human_date: human_date,
            date_x_days_from_y: date_x_days_from_y,
        }
    };
})();