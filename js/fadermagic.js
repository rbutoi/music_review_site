$(document).ready(function() {
$(".album_art").hover(function() {
		$(this).closest(".album").find("p").fadeTo(400, 1);
	},
	function(){
		$(this).closest(".album").find("p").fadeTo(400, 0);
	}
	);
});
