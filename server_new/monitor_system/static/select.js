

$("#ins_menu").click(function(event){
    $(".ins").toggleClass("not_show");
    // $(".ins_select").fadeOut(500,function(){})
});

var datePicker = $("#datePicker");
var selected_instruments = [];

datePicker.on("submit",function(e){
       e.preventDefault();
   });

var name = '';
var app = {
    single: $("button#single"),
    multiple: $("button#multiple"),
    content: $("section#graph"),
    ins : $(".ins_select"),
    multi_ins: $(".multi_ins_select"),
    span: $("div#span label"),
    defaultSpan: $("label#default"),
    sidebar: $("section#sidebar"),
    confirm: $("button#confirm")
};

app.init = function(){
    app.ins.on("click",function(){
    //    从路径中取page这个data
    name = $(this).data('name');
    console.log(name);
    app.loadPage(name);
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
    name = $(this).data('name');
    //store selected instrument names into an array
    if(selected_instruments.indexOf(name)=== -1){
        console.log("new");
        $(this).addClass('active_ins');
        selected_instruments.push(name);
        console.log(selected_instruments);
    }
    //click a selected instrument will cancel the clicked status
    else{
       console.log("exist!");
        $(this).removeClass('active_ins');
        var index = selected_instruments.indexOf(name);
        console.log("delete: "+index + selected_instruments[index]);
        selected_instruments.splice(index,1);
    }
    });


      app.confirm.on("click",function(){
          console.log("confirm");
          app.loadMultiGraph(selected_instruments);
        });


     app.span.on("click",function(){

         if(name){
             console.log("clicked span!");
             console.log(typeof(name));
             console.log(name);
            var option = $(this).data('span');
            console.log(option);
            app.loadSpanPage(name,option);
         }
        });

    datePicker.on("submit",function(){
         if(name){
             console.log(name);
             app.span.removeClass('active');
             var start_time = document.querySelector("input[name='start_time']").value;
             var end_time = document.querySelector("input[name='end_time']").value;
             app.loadDatePage(name,start_time,end_time)
   }
    });

    app.single.on("click",function(){
        console.log("single")
    });

    app.multiple.on("click",function(){
        app.loadMultipleSidebar()
    });

    app.single.on("click",function(){
        app.loadSingleSidebar()
    });

}();

app.putContent = function(content) {
    this.content.html(content);
};

app.putSidebar = function(sidebar) {
    this.sidebar.html(sidebar)
}

app.loadPage = function(name){
      //发送data page，获取新render的html
      $.ajax({
        type:'GET',
          url:'/detail',
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

app.loadSpanPage = function(name,span){
      $.ajax({
        type:'GET',
          url:'/detail',
          // dataType:'json',
        cache:false,
        data: {name: name, span: span},
        success:function(data){
            console.log(name);
            console.log("hi!!!in the span loadpage");
            app.putContent(data);
            },
         error: function(){
            app.putContent("Invalid Input!")}
        });
};

app.loadDatePage = function(name,start_time,end_time){
     $.ajax({
        type:'GET',
          url:'/detail',
          // dataType:'json',
        cache:false,
        data: {name: name, start_time: start_time, end_time: end_time},
        success:function(data){
            console.log(name);
            console.log("hi!!!in the dates loadpage");
            app.putContent(data);
            },
         error: function(){
            app.putContent("Invalid Input!")}
        });
};

app.loadMultipleSidebar = function(){
    $.ajax({
        url:'/detail',
        type:'GET',
        cache:false,
        data:{sidebar: "multiSidebar"},
        success:function(data){
            app.putSidebar(data)

        },
        error: function(){
            app.putContent("Invalid Input!")}
    })

};

app.loadSingleSidebar = function(){
    $.ajax({
        url:'/detail',
        type:'GET',
        cache:false,
        data:{sidebar: "singleSidebar"},
        success:function(data){
            app.putSidebar(data)
        },
        error: function(){
            app.putContent("Invalid Input!")}
    })

};

app.loadMultiGraph = function(selected_instruments) {
    var instruments = JSON.stringify(selected_instruments);
     $.ajax({
        type:'GET',
          url:'/detail',
          // dataType:'json',
        cache:false,
         // traditional:true,
        data: {multi: "multi",selected_instruments:instruments},
        success:function(data){
            // console.log(name);
            console.log("hi!!!in the multi ins loadpage");
            app.putContent(data);
            },
         error: function(){
            app.putContent("Invalid Input!")}
        });
}