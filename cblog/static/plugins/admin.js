var pluginD;
const routes= [
    {path: "/category", component: category},
    {path: "/file", component: file },
    {path: "/plugin", component: plugin , beforeEnter: (to, from, next)=>{
            $.get("/admin/plugin_query", function(ret, status){
                pluginD = ret;
                console.log(ret)
                var b = false;
                pluginD.plugin_list.forEach((element, index) => {
                    b = true;
                    $('#plugin-choice').append('<option value='+index+'>'+ element['name'] +'</option>')
                });
                if(b){
                    var cur_plugin_id = 0;
                    $('#pluginCode').val(pluginD.plugin_list[0].script);
                    pluginD.posts.forEach((element, index)=>{
                        var enable = 1;
                        pluginD.plugin_use.forEach((el)=>{
                            if(el.plugin_id ==pluginD.plugin_list[cur_plugin_id].id && 
                            el.post_id == element.id && el.use==0){
                                enable =0;
                            }
                        })
                        $('#plugin-table').append(
                            '<tr><td><a href="/view/'+element["id"]+'.html">'+ 
                            element['title'] +'</a></td>'+
                            '<td><button onclick="pluginSet(this,'+element["id"]+')">'+enable+'</button></td></tr>'
                            )
                    })
                    
                }

            })
            next()
    } },
    {path: "/article", component: article }
  ]
    const router = new VueRouter({
      routes
  })
  adminApp = new Vue({
      el: "#adminApp",
      delimiters: ["[[", "]]"],
      router,
      mounted: function () {
       
      },
      methods: {
          
      }
  })
  console.log(document.location.href)
  if (document.location.href.endsWith('/'))
      router.push('/article')
  


 function getpluginSelected(){
    var cur_plugin_id = parseInt($('#plugin-choice').val())
    $('#pluginCode').val(pluginD.plugin_list[cur_plugin_id].script);
    $('#plugin-table').empty();

    pluginD.posts.forEach((element, index)=>{
        var enable = 1;
        pluginD.plugin_use.forEach((el)=>{
            if(el.plugin_id ==pluginD.plugin_list[cur_plugin_id].id && 
            el.post_id == element.id && el.use==0){
                enable =0;
            }
        })
        $('#plugin-table').append(
            '<tr><td><a href="/view/'+element["id"]+'.html">'+ 
            element['title'] +'</a></td>'+
            '<td><button onclick="pluginSet(this,'+element["id"]+')">'+enable+'</button></td></tr>'
            )
    })
}

function pluginUpdate(){
    var index = parseInt($('#plugin-choice').val())
    var script = $('#pluginCode').val()
    pluginD.plugin_list[index]['script'] = script
    $.post("/admin/plugin_update", {"plugin_id": pluginD.plugin_list[index].id,
            "plugin_script": pluginD.plugin_list[index].script,
            "plugin_name": pluginD.plugin_list[index].name
        }, function(ret){
            console.log(ret)
        })

}

function pluginDelete(){
    var index = parseInt($('#plugin-choice').val())
    $.post("/admin/plugin_delete", {
            "plugin_name": pluginD.plugin_list[index].name
        }, function(ret){
            window.location.reload();
        })
}


function pluginAdd(){
    var plugin_name = $('#plugin-add').val().trim()
    var script = ''
    if(plugin_name){
        $.post("/admin/plugin_add", {'plugin_name': plugin_name, 'plugin_script': ''}, function(ret){
            console.log(ret)
            window.location.reload();
        })
    }

}

function pluginSet(_this, post_id){
    var index = parseInt($('#plugin-choice').val())
    var n = parseInt($(_this).text());

    $.post("/admin/plugin_set", {"plugin_id": pluginD.plugin_list[index].id,
            "post_id": post_id,
            "use": 1-n
        }, function(ret){
            $(_this).text(1-n);
            console.log(ret)
            
        })
    
}