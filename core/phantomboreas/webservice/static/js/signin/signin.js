$(function(){
	$("#account-register, #account-login").click(function(e) {
		$("#login-container, #register-container").toggle();
	});

	if($("#register-container").find(".custom-error-block").length) {
		$("#login-container, #register-container").toggle();
	}
})