/**
 * Created by garicchi on 2018/01/06.
 */
export default{
  install(Vue,url){
    Vue.prototype.$ws = new WebSocket(url);

    Vue.mixin({
      created:function(){

      },
      destroyed:function(){

      }
    });
  }
};
