
//
// var instruments = document.querySelectorAll(".instrument");
// for(var i = 0; i < instruments.length; i++) {
// 	instruments[i].addEventListener("click", function() {
// 	    selected = instruments[i].textContent;
// 	    alert(selected);
// 	})
//
// }
alert("connected");
console.log("hi");

var radios = document.querySelectorAll(".span_radio");
for (var i = 0; i < radios.length; i++)
	radios[i].addEventListener("click", function() {
		console.log("clicked!")
		alert("submitted!!");
		document.getElementById("radio").submit();
});




