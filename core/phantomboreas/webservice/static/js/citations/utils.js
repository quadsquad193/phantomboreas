Utils = (function() {
    human_timestamp = function(timestamp) {
        date = new Date(timestamp * 1000);

        year        = date.getFullYear();
        month       = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][date.getMonth()];
        day         = date.getDate();
        hours       = date.getHours();
        minutes     = "0" + date.getMinutes();
        period      = (hours < 12) ? 'AM' : 'PM';
        adjusted_hours = (hours == 0) ? 12 : ((hours > 12) ? hours - 12 : hours);

        return month + ' ' + day + ', ' + year + ' — ' + adjusted_hours + ':' + minutes.substr(-2) + ' ' + period;
    };

    return {
        time: {
            human_timestamp: human_timestamp,
        }
    };
})();
