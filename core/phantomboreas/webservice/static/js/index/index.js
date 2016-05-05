$(function(){
	$.get('/api/citation?days_delta=7', function(data) {
		console.log(data);

		var date_start = Utils.time.midnight_x_days_ago(7),
			weekly_summary = new WeeklySummary("#daily-averages-tile", data, date_start),
			citation_map = new CitationMap("#map-tile", data);

		weekly_summary.render();
		citation_map.render();
	});
});