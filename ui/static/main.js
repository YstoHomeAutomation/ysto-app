var app = {};

Backbone._sync = Backbone.sync;

app.Session = Backbone.Model.extend({
    defaults: {
        email: '',
        password: ''
    },
    urlRoot: 'http://ysto.local:3001/api/auth'
});

// Views
app.DashView = Backbone.View.extend({
    el: '#app',
    template: _.template($('#tpl-dashboard').html()),
    initialize: function(){
        this.render();
    },
    render: function(){
        this.$el.html(this.template());
    },
    events: {
        'click #new-user': 'newUser',
        'click #new-device': 'newDevice',
        'click #devices': 'listDevices',
        'click #homeStart': 'homeStart'
    },
    newUser: function() {
        console.log('Novo usuario');
        app.router.navigate('new-user', {trigger: true});
    },
    newDevice: function() {
        console.log('Novo dispositivo');
        app.router.navigate('new-device', {trigger: true});
    },
    listDevices: function() {
        console.log('Lista dispositivos');
        app.router.navigate('list-devices', {trigger: true});
    },
    homeStart: function() {
        console.log('Inicio');
        app.router.navigate('home', {trigger: true});
    },
});

app.NewUserView = Backbone.View.extend({
    el: '#app',
    template: _.template($('#tpl-new-users').html()),
    initialize: function(){
        this.render();
    },
    render: function(){
        this.$el.html(this.template());
    },    
});

app.NewDeviceView = Backbone.View.extend({
    el: '#app',
    template: _.template($('#tpl-new-devices').html()),
    initialize: function(){
        this.render();
    },
    render: function(){
        this.$el.html(this.template());
    }
});

app.ListDevicesView = Backbone.View.extend({
    el: '#app',
    template: _.template($('#tpl-list-devices').html()),
    initialize: function(){
        this.render();
    },
    render: function(){
        this.$el.html(this.template());
    }
});

app.LoginView = Backbone.View.extend({
    el: '#app',
    template: _.template($('#tpl-login').html()),
    initialize: function(){
        this.render();
    },
    render: function(){
        this.$el.html(this.template());
        return this;
    },
    events: {
        'click #loginButton': 'login'
    },
    login: function(e) {
        e.preventDefault();
        console.log('Login');
        var formValues = {
            email: this.$('#EmailInput').val(),
            password: this.$('#PasswordInput').val()
        };
        console.log(formValues);
        var session = new app.Session(formValues);
        session.save({}, {
            success: function(model, xhr, options){
                session.token = xhr;
                console.log('Token: ' + session.token );
                app.router.navigate('home', {trigger: true});
            },
            error: function(model, xhr, options){
                console.log('Falha de autenticação');
            }
        });
    }
});

// Routes
app.Router = Backbone.Router.extend({
    dash: null,
    newUser: null,
    newDevice: null,
    listDevices: null,
    login: null,

    initialize: function() {
        this.dash = new app.DashView();        
    },

    routes: {
        '': 'handleDash',
        'home': 'handleDash',
        //~ '': 'handleLogin',
        'new-user': 'handleNewUser',
        'new-device': 'handleNewDevice',
        'list-devices': 'handleListDevices',
        'login': 'handleLogin',
    },
    handleDash: function(){
        if (this.dash == null) {
            this.dash = new app.DashView();
        }
    },
    handleNewUser: function(){
        if (this.newUser == null) {
            this.newUser = new app.NewUserView();
        }
    },
    handleNewDevice: function(){
        if (this.newDevice == null) {
            this.newDevice = new app.NewDeviceView();
        }
    },
    handleListDevices: function(){
        if (this.listDevices == null) {
            this.listDevices = new app.ListDevicesView();
        }
    },
    handleLogin: function(){
        if (this.login == null) {
            this.login = new app.LoginView();
        }
    },
});


$(document).ready(function(){
    app.router = new app.Router();
    Backbone.history.start();
});
