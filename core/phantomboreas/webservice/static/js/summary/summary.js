$(function(){
	$.get('/api/citation?days_delta=7', function(data) {
		var citations_today = data.citations.filter(function(citation) {
			return Utils.time.date_is_today(citation.evidence[0].timestamp);
		}).length;

		var date_start = Utils.time.midnight_x_days_ago(7),
			weekly_summary = new WeeklySummary("#daily-averages-tile", data, date_start),
			citation_map = new CitationMap("#map-tile", data),
			day_counter = new Counter(citations_today, $("#day-citation-counter"));


		weekly_summary.render();
		citation_map.render();
		day_counter.render();
	});

	$.get('/api/citation?days_delta=10000', function(data) {
		var weekly_averages_summary = new WeeklyAveragesSummary("#citations-by-week", data),
			total_counter = new Counter(data.citations.length, $("#total-citation-counter"));

		weekly_averages_summary.render();
		total_counter.render();
	});	
});