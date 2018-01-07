<template>
  <v-container grid-list-md class="mt-1">
    <v-layout row wrap>

      <v-progress-linear color="pink" v-bind:indeterminate="isUpdating" v-if="isUpdating"></v-progress-linear>

    </v-layout>
    <v-layout row wrap>
      <v-flex md12>
        <v-card class="card ma-1">
          <v-card-title primary-title>
            <div class="headline">API Keys</div>
            <div>Set your web api keys</div>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-layout v-for="(value,key) in setting">
                <v-flex md4>
                  <v-subheader>{{key}}</v-subheader>
                </v-flex>
                <v-flex md8>
                  <v-text-field
                    v-bind:label="key"
                    v-model="value"
                    v-on:blur="onChange()"
                    v-bind:disabled="!isEnabled"
                  ></v-text-field>
                </v-flex>

              </v-layout>
            </v-container>

          </v-card-text>
        </v-card>
      </v-flex>


    </v-layout>
    <v-layout row wrap>
      <v-flex md5>
        <v-card class="card ma-1">
          <v-card-title primary-title>
            <div class="headline">Unlimited music now</div>
            <div>Listen to your favorite artists and albums whenever and wherever, online and offline.</div>
          </v-card-title>
          <v-card-actions>
            <v-btn flat>Listen now</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
      <v-flex md7>
        <v-card class="card ma-1">
          <v-card-title primary-title>
            <div class="headline">Unlimited music now</div>
            <div>Listen to your favorite artists and albums whenever and wherever, online and offline.</div>
          </v-card-title>
          <v-card-actions>
            <v-btn flat>Listen now</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>

    </v-layout>

  </v-container>

</template>


<script>

  export default {
    name: 'app',
    data () {
      return {
        setting:{
        },
        isEnabled:false,
        isUpdating:false
      }
    },
    watch: {

    },
    mounted: function () {
      let inst = this;
      this.$ws.addEventListener('open', function () {
          let command = {
            command: 'GET_ASSISTANT_SETTING',
            detail: {}
          }
          inst.$ws.send(JSON.stringify(command));
          inst.isUpdating = true;
      });

      this.$ws.addEventListener('message', function (msg) {
        let data = JSON.parse(msg.data);

        if(data.command === 'GET_ASSISTANT_SETTING'){
            inst.setting = data.detail.setting;
            inst.isEnabled = true;
            inst.isUpdating = false;
        }

        if(data.command === 'SET_ASSISTANT_SETTING'){
            inst.isEnabled = true;
            inst.isUpdating = false;
            inst.$emit('showNotify',{
              color: 'info',
              text:'setting updated'
            })
        }
      });


    },
    destroyed: function () {

    },
    methods: {
      onChange:function(){
          let command = {
            command: 'SET_ASSISTANT_SETTING',
            detail: {
                setting:this.setting
            }
          }
          this.$ws.send(JSON.stringify(command));
          this.isEnabled = false;
          this.isUpdating = true;
      }
    },
    watch: {

    }
  }
</script>


<style>

</style>
