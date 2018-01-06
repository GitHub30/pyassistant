<template>
  <v-app>
    <v-navigation-drawer
      fixed
      clipped
      app
      v-model="navBar"
    >
      <v-list dense class="pt-0">
        <router-link to="/">
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>dashboard</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>DASHBOARD</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </router-link>
        <router-link to="/setting">
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>settings</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>SETTING</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </router-link>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      dark
      color="primary"
      clipped-left
      fixed
      app
    >
      <v-toolbar-side-icon @click.stop="navBar = !navBar"></v-toolbar-side-icon>
      <v-toolbar-title class="white--text">{{title}}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="isMute" icon v-on:click="setMute(false)">
        <v-icon>mic_off</v-icon>
      </v-btn>
      <v-btn v-else icon v-on:click="setMute(true)">
        <v-icon>mic</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>apps</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>refresh</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>more_vert</v-icon>
      </v-btn>

    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-fade-transition mode="out-in">
          <router-view></router-view>
        </v-fade-transition>
      </v-container>
    </v-content>
    <v-snackbar
      :timeout="notifySnack.timeout"
      :color="notifySnack.color"
      v-model="notifySnack.show"
    >
      {{ notifySnack.text }}
      <v-btn dark flat @click.native="snackbar = false">Close</v-btn>
    </v-snackbar>
  </v-app>
</template>

<script>

  export default {
    name: 'app',
    data () {
      return {
        navBar: null,
        title: '',
        isMute: false,
        notifySnack:{
          show:false,
          color:'info',
          timeout:'6000',
          text:''
        }
      }
    },
    watch: {
      '$route': function (data) {
        this.title = data.name;
      }
    },
    mounted: function () {
      this.title = this.$route.name;
      let inst = this;
      this.$ws.addEventListener('open', function () {
        console.log('on open');
      });

      this.$ws.addEventListener('message', function (msg) {
          let data = JSON.parse(msg.data);
          if(data.command==='ASSISTANT_MUTE'){

              if(data.detail.isMute){

                inst.showNotify({
                  color:'info',
                  text:'マイクはオフです'
                });
              }else{
                inst.showNotify({
                  color:'info',
                  text:'マイクはオンです'
                });
              }
          }

          if(data.command==='ASSISTANT_ERROR'){
            inst.showNotify({
                  color:'error',
                  text:'エラーが発生しました ['+data.detail.message+']'
                });
          }
      });

    },
    destroyed: function () {

    },
    methods:{
        setMute:function(isMute){
          this.isMute = isMute
          let command = {
              command:'ASSISTANT_MUTE',
              detail:{
                  'isMute':isMute
              }
          }
          this.$ws.send(JSON.stringify(command));
        },
        showNotify:function(prop){
            this.notifySnack.color = prop.color;
            this.notifySnack.text = prop.text;
            this.notifySnack.show = true;
        }
    }
  }
</script>

<style>
  a {
    text-decoration: none;
  }

  .card{
    min-height:200px;
  }

</style>
