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
                <a class="button button-primary u-full-width" id="devices" href="#" @click="changeView('list-devices')">Devices</a>
              </div>
          </div>
          <div class="row">
              <div class="one-third column">
                <a class="button u-full-width" id="logout" href="#">Logout</a>
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
          <div class="one-half column">
            <label for="EmailInput">Your email</label>
            <input class="u-full-width" type="email" placeholder="your email" id="EmailInput">
          </div>
          <div class="one-half column">
            <label for="PasswordInput">Password</label>
            <input class="u-full-width" type="password" id="PasswordInput">
            <input class="button-primary u-full-width" type="submit" value="Save">
            <input class="button u-full-width" type="submit" value="Logout">
          </div>
        </div>
      </form>
    </div>
    `,
    props: ['currentView']
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
            <input class="u-full-width" type="text" placeholder="Ex. MA006" id="NamelInput">
           </div>
          <div class="one-third column">
            <input class="button-primary u-full-width" type="submit" value="Save">
            <input class="button u-full-width" type="submit" value="Logout">
          </div>
        </div>
      </form>
    </div>
  `,
  props: ['currentView']
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
                <td>MA001</td>
                <td>ONLINE</td>
                <td><a class="button button-primary" href="#">Switch</a></td>
              </tr>
              <tr>
                <td>MA003</td>
                <td>OFFLINE</td>
                <td><a class="button button" href="#">Switch</a></td>
              </tr>
            </tbody>
          </table>
      </div>
      <div class="row">
        <div class="one-third column">
          <input class="button u-full-width" type="submit" value="Logout">
        </div>
      </div>
    </div>
  `
});


// Ponto de entrada do app
var app = new Vue({
  el: '#app',
  data: {
    currentView: 'dash'
  }
});
