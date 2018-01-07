<template>
  <v-app>
    <v-navigation-drawer
      fixed
      clipped
      app
      v-model="navBar"
    >
      <v-list v-for="route in this.$router.options.routes" dense class="pt-0">
        <router-link v-bind:to="route.path">
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>{{route.icon}}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{route.name}}</v-list-tile-title>
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
      <v-toolbar-title class="white--text">Pi Assistant - {{title}}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-slider thumb-label dark prepend-icon="volume_up" v-model="volume" v-on:blur="setVolume(volume)" v-bind:label="volume" color="pink"
                thumbColor="pink"></v-slider>

      <v-btn v-if="isMute" icon v-on:click="setMute(false)">
        <v-icon>mic_off</v-icon>
      </v-btn>
      <v-btn v-else icon v-on:click="setMute(true)">
        <v-icon>mic</v-icon>
      </v-btn>

    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-fade-transition mode="out-in">
          <router-view v-on:showNotify="showNotify"></router-view>
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
        notifySnack: {
          show: false,
          color: 'info',
          timeout: '6000',
          text: ''
        },
        volume: 70
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
        let command = {
          command: 'GET_VOLUME',
          detail: {}
        }
        inst.$ws.send(JSON.stringify(command));
      });

      this.$ws.addEventListener('message', function (msg) {
        let data = JSON.parse(msg.data);
        if (data.command === 'ASSISTANT_MUTE') {

          if (data.detail.isMute) {

            inst.showNotify({
              color: 'info',
              text: 'マイクはオフです'
            });
          } else {
            inst.showNotify({
              color: 'info',
              text: 'マイクはオンです'
            });
          }
        }

        if (data.command === 'GET_VOLUME') {
          inst.volume = data.detail.volume;
        }

        if (data.command === 'SET_VOLUME') {
          inst.showNotify({
            color: 'info',
            text: 'set volume [' + data.detail.volume + ']'
          });
        }

        if (data.command === 'ASSISTANT_RESTART') {
          inst.showNotify({
            color: 'info',
            text: 'assistant restart complete'
          });
        }

        if (data.command === 'ASSISTANT_ERROR') {
          inst.showNotify({
            color: 'error',
            text: 'エラーが発生しました [' + data.detail.message + ']'
          });
        }


      });


    },
    destroyed: function () {

    },
    methods: {
      setMute: function (isMute) {
        this.isMute = isMute
        let command = {
          command: 'ASSISTANT_MUTE',
          detail: {
            'isMute': isMute
          }
        }
        this.$ws.send(JSON.stringify(command));
      },
      showNotify: function (prop) {
        this.notifySnack.color = prop.color;
        this.notifySnack.text = prop.text;
        this.notifySnack.show = true;
      },
      assistantRestart: function () {
        let command = {
          command: 'ASSISTANT_RESTART',
          detail: {}
        }
        this.$ws.send(JSON.stringify(command));
      },
      setVolume(vol){
          this.volume = vol;
          let command = {
            command: 'SET_VOLUME',
            detail: {
              'volume': this.volume
            }
          }
        this.$ws.send(JSON.stringify(command));
      }
    }
  }
</script>

<style>
  a {
    text-decoration: none;
  }

  .card {
    min-height: 150px;
  }

</style>
