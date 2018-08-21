
console.log("connected!");
$(".choice").click(function() {
    $(this).children("input").attr("checked", "checked");
    $("#span_form").submit();

});




$("#ins_menu").click(function(event){
    $(".ins_select").toggleClass("not_show");
    // $(".ins_select").fadeOut(500,function(){})
});