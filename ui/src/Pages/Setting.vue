<template>
  <v-container grid-list-md class="mt-1">
    <v-layout row wrap>

      <v-progress-linear color="pink" v-bind:indeterminate="isUpdating" v-if="isUpdating"></v-progress-linear>

    </v-layout>

    <v-layout row wrap>
      <v-flex md12>
        <v-card class="card ma-1">
          <v-card-title primary-title>
            <div class="headline">Update setting</div>
            <div class="ma-2">Assistant require restart to update setting</div>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-btn color="error" v-bind:disabled="!isEnabled" v-on:click="restartAssitant">
                Update Setting
                <v-icon right dark>autorenew</v-icon>
              </v-btn>
            </v-container>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row wrap>
      <v-flex md12>
        <v-card class="card ma-1">
          <v-card-title primary-title>
            <div class="headline">Setting</div>
            <div class="ma-2">Set your setting value</div>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-layout v-for="(value,key) in setting">
                <v-flex md4>
                  <v-subheader>{{key}}</v-subheader>
                  <p>{{value.description}}</p>
                </v-flex>
                <v-flex v-if="value.type==='string'" md8>
                  <v-text-field
                    v-bind:label="key"
                    v-model="value.value"
                    v-bind:disabled="!isEnabled"
                  ></v-text-field>
                </v-flex>

                <v-flex v-else-if="value.type==='select'" md8>
                  <v-select
                    v-model="value.value"
                    v-bind:items="value.option"
                    item-text="label"
                    item-value="value"
                    single-line
                    bottom
                    return-object
                    v-bind:disabled="!isEnabled"
                  >

                  </v-select>
                </v-flex>

                <v-flex v-else-if="value.type==='slider'" md8>
                  <v-slider
                    thumbLabel
                    v-bind:step="value.step"
                    v-bind:min="value.min"
                    v-bind:max="value.max"
                    v-bind:label="value.value"
                    v-model="value.value"
                    v-bind:disabled="!isEnabled"
                  >
                  </v-slider>
                </v-flex>
                <v-flex v-else md8>
                  <span>undefined setting type</span>
                </v-flex>

              </v-layout>

            </v-container>

          </v-card-text>
        </v-card>
      </v-flex>


    </v-layout>


  </v-container>

</template>


<script>

  export default {
    data () {
      return {
        setting: {},
        isEnabled: false,
        isUpdating: false
      }
    },
    created: function () {
      let inst = this;
      if (this.$ws.readyState === 1) {
        this.updateData();
      }
      this.$onWsOpen(this, function (arg) {
        inst.updateData();
      });
    },
    destroyed: function () {

    },
    methods: {
      updateData: function () {
        let inst = this;
        let command = {
          command: 'GET_ASSISTANT_SETTING',
          detail: {}
        }
        this.$getWs(command, function (msg) {
          inst.setting = msg.detail.setting;
          inst.isEnabled = true;
          inst.isUpdating = false;
        });
        this.isUpdating = true;
      },
      restartAssitant: function () {
        let inst = this;
        let command = {
          command: 'SET_ASSISTANT_SETTING',
          detail: {
            setting: this.setting
          }
        }
        this.$getWs(command, function (msg) {
          let command = {
            command: 'ASSISTANT_RESTART',
            detail: {}
          }
          inst.$getWs(command, function (msg) {
            inst.isEnabled = true;
            inst.isUpdating = false;
            inst.$emit('showNotify', {
              color: 'info',
              text: 'pyassistant save setting'
            })
          });
        });
        this.isEnabled = false;
        this.isUpdating = true;

      }
    },
    watch: {}
  }
</script>


<style>

</style>
