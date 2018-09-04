

$("#ins_menu").click(function(event){
    $(".ins").toggleClass("not_show");
    // $(".ins_select").fadeOut(500,function(){})
});


var selected_instruments = [];

// app.datePicker.on("submit",function(e){
//        e.preventDefault();
//    });

var name = '';
var app = {
    single: $("button#single"),
    multiple: $("button#multiple"),
    content: $("section#graph"),
    timePicker: $("section#timePicker"),
    ins : $(".ins_select"),
    multi_ins: $(".multi_ins_select"),
    span: $("div#span label"),
    defaultSpan: $("label#default"),
    multi_span: $("div#multi_span label"),
    multi_defaultSpan: $("label#multi_default"),
    sidebar: $("section#sidebar"),
    confirm: $("button#confirm"),
    datePicker: $("#datePicker"),
    // multiDatePicker: $("#multi_datePicker")
};

app.init = function(){
    app.ins.on("click",function(){
    //    从路径中取page这个data
    name = $(this).data('name');
    // console.log(name);
    app.loadSingleGraph(name);
    console.log("clicked instrument");
    app.span.removeClass('active');
    app.defaultSpan.addClass('active');
    $(".ins_select").removeClass("active_ins");
    $(this).addClass('active_ins');
    document.querySelector("input[name='start_time']").value = '';
    document.querySelector("input[name='end_time']").value = '';
});

    app.multi_ins.on("click",function(){
    //    从路径中取page这个data
    mul_name = $(this).data('dt');
    // console.log("111111111111111111");
    // console.log(selected_instruments.indexOf(mul_name));
    //store selected instrument names into an array
    if(selected_instruments.indexOf(mul_name)=== -1){
        console.log("new");
        $(this).addClass('active_ins');
        selected_instruments.push(mul_name);
        console.log(selected_instruments);
    }
    //click a selected instrument will cancel the clicked status
    else{
       // console.log("exist!");
       // console.log(selected_instruments);
        $(this).removeClass('active_ins');
        var index = selected_instruments.indexOf(mul_name);
        // console.log("delete: "+index + selected_instruments[index]);
        selected_instruments.splice(index,1);
    }
    });

      app.confirm.on("click",function(){
          // console.log("confirm");
            app.span.removeClass('active');
            app.defaultSpan.addClass('active');
            document.querySelector("input[name='start_time']").value = '';
            document.querySelector("input[name='end_time']").value = '';
            app.loadDefaultMultiGraph(selected_instruments);
        });

     app.span.on("click",function() {
         var option = $(this).data('span');
 //
 //         $('a.active_ins').each(function(){
 //         var ins_name = $(this).data('name');
 //         sele.push(ins_name);
 //        console.log(ins_name);
 // });
         if (selected_instruments.length > 0) {
             // console.log("11111111111111selcted: ");
             // console.log(selected_instruments);
             // console.log(option);
             app.loadMultiSpanGraph(selected_instruments,option);
         }
         else {
             app.loadSpanGraph(name, option);
         }
     });

     app.multi_span.on("click",function(){
         app.span.removeClass('active');
         var option = $(this).data('span');
         app.loadMultiSpanGraph(selected_instruments,option);
        });

    app.datePicker.on("submit",function(e){
         e.preventDefault();
         app.span.removeClass('active');
          if(selected_instruments.length > 0){
             var start_time = document.querySelector("input[name='start_time']").value;
             var end_time = document.querySelector("input[name='end_time']").value;
             app.loadMultiDatePage(selected_instruments,start_time,end_time)
   }
         else{
             var start_time = document.querySelector("input[name='start_time']").value;
             var end_time = document.querySelector("input[name='end_time']").value;
             app.loadDatePage(name,start_time,end_time)
   }
    });

    app.single.on("click",function(){
        // console.log("single");
        app.loadSingleSidebar();
        $(this).addClass("active");
        app.multiple.removeClass("active");
    });

    app.multiple.on("click",function(){
        app.loadMultipleSidebar();
        $(this).addClass("active");
        app.single.removeClass("active");
    });
}();

app.putContent = function(content) {
    this.content.html(content);
};

app.putTimePicker = function(timePicker) {
  this.timePicker.html(timePicker)
};

app.putSidebar = function(sidebar) {
    this.sidebar.html(sidebar)
};

app.loadSingleGraph = function(name){
      //发送data page，获取新render的html
      $.ajax({
        type:'GET',
          url:'/singleGraph',
          // dataType:'json',
        cache:false,
        data: {name: name},
        success:function(data){
            // console.log(data);
            app.putContent(data);
            },
         error: function(){
            app.putContent("Invalid Input!")}
        });
};

app.loadSpanGraph = function(name,span){
      $.ajax({
        type:'GET',
          url:'/singleGraph',
        cache:false,
        data: {name: name, span: span},
        success:function(data){
            // console.log(name);
            // console.log("hi!!!in the span loadpage");
            app.putContent(data);
            },
         error: function(){
            app.putContent("Invalid Input!")}
        });
};

app.loadDatePage = function(name,start_time,end_time){
     $.ajax({
        type:'GET',
          url:'/singleGraph',
          // dataType:'json',
        cache:false,
        data: {name: name, start_time: start_time, end_time: end_time},
        success:function(data){
            // console.log(name);
            // console.log("hi!!!in the dates loadpage");
            app.putContent(data);
            },
         error: function(){
            app.putContent("Invalid Input!")}
        });
};

app.loadMultiDatePage = function(selected_instruments,start_time,end_time){
    if (selected_instruments.length > 0) {
        var instruments = JSON.stringify(selected_instruments);
        $.ajax({
            type: 'GET',
            url: '/multiGraph',
            // dataType:'json',
            cache: false,
            data: {selected_instruments: instruments, start_time: start_time, end_time: end_time},
            success: function (data) {
                // console.log(selected_instruments);
                // console.log("hi!!!in the multi dates loadpage");
                app.putContent(data);
            },
            error: function () {
                app.putContent("Invalid Input!")
            }
        });
    }
};

app.loadMultipleSidebar = function(){
    $.ajax({
        url:'/sidebar',
        type:'GET',
        cache:false,
        data:{sidebar: "multi"},
        success:function(data){
            app.putSidebar(data)

        },
        error: function(){
            app.putContent("Invalid Input!")}
    })

};

app.loadSingleSidebar = function(){
    $.ajax({
        url:'/sidebar',
        type:'GET',
        cache:false,
        data:{sidebar: "single"},
        success:function(data){
            app.putSidebar(data)
        },
        error: function(){
            app.putContent("Invalid Input!")}
    })

};

app.loadMultiSpanGraph = function(selected_instruments, span) {
    if (selected_instruments.length > 0) {
        var instruments = JSON.stringify(selected_instruments);
        $.ajax({
            type: 'GET',
            url: '/multiGraph',
            cache: false,
                // traditional:true,
            data: {span: span, selected_instruments: instruments},
            success: function (data) {
                // console.log("!!!!!!!!!!!!!span: " + span);
                // console.log("hi!!!in the multi ins loadpage");
                app.putContent(data);
                },
            error: function () {
                app.putContent("Invalid Input!")
            }
        });
    }

};

app.loadDefaultMultiGraph = function(selected_instruments) {
    var instruments = JSON.stringify(selected_instruments);
     $.ajax({
        type:'GET',
        url:'/defaultMultiGraph',
          // dataType:'json',
        cache:false,
         // traditional:true,
        data: {selected_instruments:instruments},
        success:function(data){
            // console.log(name);
            // console.log("hi!!!in the multi ins loadpage");
            app.putContent(data);
            },
         error: function(){
            app.putContent("Invalid Input!")}
        });
};

// app.loadMultiTime = function() {
//     $.ajax({
//         type:'GET',
//         url:'/timePicker',
//           // dataType:'json',
//         cache:false,
//          // traditional:true,
//         data: {time: "multi"},
//         success:function(data){
//             // console.log(name);
//             // console.log("hi!!!in the multi ins loadpage");
//             app.putTimePicker(data);
//             },
//          error: function(){
//             app.putTimePicker("Invalid Input!")}
//         });
// };

// app.loadSingleTime = function() {
//     $.ajax({
//         type:'GET',
//         url:'/timePicker',
//           // dataType:'json',
//         cache:false,
//          // traditional:true,
//         data: {time: "single"},
//         success:function(data){
//             // console.log(name);
//             console.log("hi!!!in the single ins loadpage");
//             app.putTimePicker(data);
//             },
//          error: function(){
//             app.putTimePicker("Invalid Input!")}
//         });
// };