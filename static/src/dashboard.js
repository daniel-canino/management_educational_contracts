odoo.define('educational_contract.PowerbiDashboardView', function(require) {
    "use strict";

    var FormView = require('web.FormView');
    var FormController = require('web.FormController');
    var view_registry = require('web.view_registry');
    var rpc = require('web.rpc');

    var PowerbiDashboardController = FormController.extend({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.render_powerbi_dashboard();
        },

        render_powerbi_dashboard: function() {
            var self = this;
            rpc.query({
                route: '/get/dashboardparameter',
                params: {},
            }).then(function(data) {
                var container = self.$el.find('#powerbi_dashboard_container')[0];

                if (container && data.embed_url) {
                    let models = window['powerbi-client'].models;
                    
                    // Definir la configuración de incrustación
                    let embedConfiguration = {
                        type: "dashboard",
                        id: data.dashboard_id,
                        embedUrl: data.embed_url,
                        accessToken: data.embed_token,
                        tokenType: models.TokenType.Embed,
                    };
                    
                    // Incrusta el dashboard directamente. La librería se encarga de crear el iframe.
                    var dashboard = powerbi.embed(container, embedConfiguration);
                    
                    // Manejo de eventos
                    dashboard.on("loaded", function () {
                        console.log("Dashboard load successful");
                    });
                    
                    dashboard.on("rendered", function () {
                        console.log("Dashboard render successful");
                    });
                    
                    dashboard.on("error", function (event) {
                        var errorMsg = event.detail;
                        console.error("Error de incrustación:", errorMsg);
                    });
                }
            }).catch(function(error) {
                 console.error("Error en la llamada RPC:", error);
            });
        }
    });

    var PowerbiDashboardView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: PowerbiDashboardController,
        }),
    });

    view_registry.add('powerbi_dashboard_form', PowerbiDashboardView);
});