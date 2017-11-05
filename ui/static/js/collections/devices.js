app.collections.Devices = Backbone.Collection.extend({
    initialize: function() {
        this.add({description: 'MA666'});
    },
    model: app.models.Device,
    changeStatus: function(state, index) {
        this.models[index].set("realizada", state);
    }
});
