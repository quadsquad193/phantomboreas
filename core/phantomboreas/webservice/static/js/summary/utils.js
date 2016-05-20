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

    var day_of_week = function(timestamp) {
        var weekday = new Array(7);

        weekday[0]=  "Sunday";
        weekday[1] = "Monday";
        weekday[2] = "Tuesday";
        weekday[3] = "Wednesday";
        weekday[4] = "Thursday";
        weekday[5] = "Friday";
        weekday[6] = "Saturday";

        var date = new Date(timestamp * 1000);

        return weekday[date.getDay()];
    }

    var date_is_today = function(timestamp) {
        var date = new Date(timestamp * 1000),
            date_now = new Date();

        return date.toDateString() == date_now.toDateString();
    }

    var weeks_elapsed = function(timestamps) {
        var minTime = Math.min.apply(null, timestamps), 
            maxTime = Math.max.apply(null, timestamps);

        return Math.ceil((maxTime - minTime) / (60*60*24*7));
    }

    return {
        time: {
            human_timestamp: human_timestamp,
            midnight_x_days_ago: midnight_x_days_ago,
            human_date: human_date,
            date_x_days_from_y: date_x_days_from_y,
            day_of_week: day_of_week,
            weeks_elapsed: weeks_elapsed,
            date_is_today: date_is_today
        }
    };
})();