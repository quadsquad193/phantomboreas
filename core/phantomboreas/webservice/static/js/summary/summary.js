$(function(){
	$.get('/api/citation?days_delta=7', function(data) {
		var date_start = Utils.time.midnight_x_days_ago(7),
			weekly_summary = new WeeklySummary("#daily-averages-tile", data, date_start),
			citation_map = new CitationMap("#map-tile", data);

		weekly_summary.render();
		citation_map.render();
	});

	$.get('/api/citation?days_delta=10000', function(data) {
		var weekly_averages_summary = new WeeklyAveragesSummary("#citations-by-week", data);

		weekly_averages_summary.render();
	});	
});