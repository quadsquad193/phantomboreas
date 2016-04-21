$(function(){
	$("#create_user").click(function(e) {
		if($("#username").val().length && $("#password").val().length) {
			$.ajax({
				url: '/users',
				type: 'POST',
				contentType: 'application/json',
				data: JSON.stringify({username: $("#username").val(), password: $("#password").val()}, null, '\t'),
				success: function(data) {
					$(".user-table tbody").append(
						"<tr>" +
							"<td>" + data.id + "</td>" +
							"<td>" + data.username + "</td>" +
							"<td>" + data.is_admin + "</td" +
						"</tr>"
					);

					$("#username, #password").val('');
				},
				error: function() {
					$("#username, #password").val('');
				}
			});
		}
	});

	$(".is_admin").on('change', function(e) {
		var id = $(this).attr('data-id'),
			checked = $(this).prop('checked');

		$.ajax({
			url: '/users/'+id,
			type: 'PATCH',
			contentType: 'application/json',
			data: JSON.stringify({is_admin: checked}, null, '\t'),
			success: function(data) {
				console.log("Success", data);
			},
			error: function() {
				console.log("error");
			}
		});
	});
});