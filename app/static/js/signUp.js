$(function(){
	$('#btnSignUp').click(function(){

		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				html = jQuery.parseJSON(response);
				if (typeof html.message != "undefined") {
					$("#status").empty().append(html.message);
					console.log(html.message);
				}
				else if (typeof html.error != "undefined") {
					$("#status").empty().append(html.error);
					console.log(html.error);
				}
				else if (typeof html.html != "undefined") {
					$("#status").empty().append(html.html);
					console.log(html.html);
				}
				console.log(response)
			},
			error: function(error){
				console.log(error);
				$("#status").append(error);
			}
		});
	});
});
