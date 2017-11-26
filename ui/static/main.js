// cabeçalho com token de validação.
Vue.http.headers.common['Authorization'] = 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6W3siaWQiOjF9XX0.eetLj4DKGNshMe9uCZmtvOayZPFHva_PsrqANvG6pRI';
//~ var API='http://ysto.local:3001/api'
var API='http://192.168.10.101:3001/api'
Vue.config.debug = true;


Vue.component('dash', {
    template:`
        <div>
          <div class="row">
              <h5>Dashboard</h5>
          </div>
            <div class="row">
              <div class="one-third column" >
                <a class="button button-primary u-full-width" id="new-user" href="#" @click="changeView('new-user')">New user</a>
              </div>
              <div class="one-third column">
                <a class="button button-primary u-full-width" id="new-device" href="#" @click="changeView('new-device')">New device</a>
              </div>
              <div class="one-third column">
                <a class="button button-primary u-full-width" id="btn-devices" href="#" @click="changeView('list-devices')">Devices</a>
              </div>
          </div>
          <div class="row">
              <div class="one-third column">
               <!-- <a class="button u-full-width" id="logout" href="#">Logout</a> -->
              </div>
          </div>
        </div>
    `,
    props: ['currentView'],
    methods: {
      changeView: function(view) {
        app.currentView=view;
      }
    }
});

Vue.component('new-user', {
  template: `
    <div>
      <div class="row">
          <h5>New User</h5>
      </div>
      <form>
        <div class="row">
          <div class="one-third column">
            <label for="NameInput">Your name</label>
            <input class="u-full-width" type="text" placeholder="your name" id="NameInput">
          </div>
          <div class="one-third column">
            <label for="EmailInput">Your email</label>
            <input class="u-full-width" type="email" placeholder="your email" id="EmailInput">
          </div>
          <div class="one-third column">
            <label for="PasswordInput">Password</label>
            <input class="u-full-width" type="password" id="PasswordInput">
            <input class="button-primary u-full-width" v-on:click="sendUser" type="submit" value="Save">
            <!-- <input class="button u-full-width" v-on:click="getDevices" type="submit" value="Logout"> -->
          </div>
        </div>
      </form>
    </div>
    `,
    props: ['currentView'],
    
    methods: {
        aboutAPI: function(){
            this.$http.get(API)
            .then(result => {

                if (result.status == 200) {
                    console.log('SUCESSO GALERA!');
                    console.log(result.data);
                }
            })
        },
        getDevices: function(){
            this.$http.get(API+'/devices')
            .then(result => {
                if (result.status == 200) {
                    console.log('SUCESSO 2 GALERA!');
                    console.log(result.data);
                }
            })
        },
        sendUser: function() {
            console.log('Teste de envio');
            user = {
                name:  NameInput.value,
                email: EmailInput.value,
                password: PasswordInput.value
            }

            console.log(user);

            this.$http.post(API+'/users', user)
            .then(result => {
                if (result.status == 200) {
                    console.log('Cadastro de usuario com sucesso');
                } else {
                    console.log('Falha no cadastro de usuario: ' + reult.status);
                }
            })
        }
    }
});

Vue.component('new-device', {
  template:`
    <div>
      <div class="row">
        <h5>New Device</h5>
      </div>
      <form>
        <div class="row">
          <div class="two-thirds column">
            <label for="NamelInput">Device name</label>
            <input class="u-full-width" type="text" placeholder="Ex. MA006" id="DeviceName">
           </div>
          <div class="one-third column">
            <input class="button-primary u-full-width" v-on:click="sendDevice" type="submit" value="Save">
             <!-- <input class="button u-full-width" type="submit" value="Logout"> -->
          </div>
        </div>
      </form>
    </div>
  `,
  props: ['currentView'],
  methods: {
    sendDevice: function(){
        device = {
            description: DeviceName.value,
            user_id: 1
        };
        
        this.$http.post(API+'/devices', device)
        .then(result => {
            if (result.status == 200) {
                console.log('Cadastro de dispositivo com sucesso');
            } else {
                console.log('Falha no cadastro de usuario: ' + reult.status);
            }
        })
    }
  }
});

Vue.component('list-devices',{
  template:`
    <div>
      <div class="row">
      <h5>Device(s)</h5>
      </div>
      <div class="row">
          <table class="u-full-width">
            <thead>
              <tr>
                <th>Device</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>MA002</td>
                <td>ONLINE</td>
                <td><a class="button button-primary" v-on:click="switchON(2)" href="#">Switch</a></td>
              </tr>
              <tr>
                <td>MA003</td>
                <td>ONLINE</td>
                <td><a class="button button-primary" v-on:click="switchON(670)" href="#">Switch</a></td>
              </tr>
            </tbody>
          </table>
      </div>
      <div class="row">
        <div class="one-third column">
          <!-- <input class="button u-full-width" type="submit" value="Logout"> -->
          <!-- <input class="button u-full-width" v-on:click="listDevices" type="submit" value="Logout"> -->
        </div>
      </div>
    </div>
  `,
    props: ['devices'],
    
    methods: {
        listDevices: function(){
            console.log(devices);
        },
        switchON: function(id) {
          var state;
        
          this.$http.get(API+'/devices/'+id)
          .then(result => {
            if (result.status == 200) {
              state = result.data.devices[0]['switch_on'];
              if (state === 0) {
                state = 1;
              } else {
                state = 0;
              }
            }
            this.$http.put(API+'/devices/'+id, {switch_on:state})
            .then(result => {
              if (result.status == 200) {
                console.log('Troquei estado');
              }
            })
          })
        }
    }
});


// Ponto de entrada do app
var app = new Vue({
  el: '#app',
  data: () => ({
    currentView: 'dash',
    devices: []
  }),
  // Carrega a lista de dispositivos cadastrados
  created: function() {
    this.$http.get(API+'/devices')
    .then(result => {
      if (result.status == 200) {
        devices = result.data.devices;
      }
    })
  },
});
