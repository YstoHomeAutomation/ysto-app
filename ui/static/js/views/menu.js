app.views.menu = Backbone.View.extend({
    template: _.template($("#tpl-header").html()),
    initialize: function() {
        this.render();
    },
    render: function(){
        this.$el.html(this.template({}));
    }
});
