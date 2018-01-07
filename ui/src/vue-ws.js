/**
 * Created by garicchi on 2018/01/06.
 */
export default{
  install(Vue,url){
    Vue.prototype.$ws = new WebSocket(url);
    Vue.prototype.$ws.addEventListener('message',function(msg){
        let data = JSON.parse(msg.data);
        Vue.prototype.$wsGetList.forEach(function(v,i){
          if(v.command===data.command){
            v.callback(data);
            Vue.prototype.$wsGetList.splice(i,1);
          }
        });

    });
    Vue.prototype.$wsGetList = [];
    Vue.prototype.$getWs = function(message,callback){
      Vue.prototype.$wsGetList.push({
        command:message.command,
        callback:callback
      });


      Vue.prototype.$ws.send(JSON.stringify(message));

    }

    Vue.prototype.$ws.addEventListener('open',function(msg){
        let keys = Object.keys(Vue.prototype.$wsOpenDic);
        keys.forEach(function(v){
          Vue.prototype.$wsOpenDic[v]();
        });

    });

    Vue.prototype.$wsOpenDic = {};
    Vue.prototype.$onWsOpen = function(sender,callback){
      Vue.prototype.$wsOpenDic[sender] = callback;
    }

    Vue.prototype.$ws.addEventListener('close',function(msg){
        let keys = Object.keys(Vue.prototype.$wsCloseDic);
        keys.forEach(function(v){
          Vue.prototype.$wsCloseDic[v]();
        });
    });

    Vue.prototype.$wsCloseDic = {};
    Vue.prototype.$onWsClose = function(sender,callback){
      Vue.prototype.$wsCloseDic[sender] = callback;
    }

    Vue.mixin({
      created:function(){

      },
      destroyed:function(){

      }
    });
  }
};
