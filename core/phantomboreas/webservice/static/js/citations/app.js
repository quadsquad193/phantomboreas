$(document).ready(function() {
    urls = {
        assets_capture: '/assets/capture/',
    };
    templates   = {
        citation: $('#template-citation').html(),
    };
    service     = new Citations.service('/api/citation/');
    app         = new Citations.app($('div#citation-app-container'), $('form#citation-app-search'), $('ul#citation-app-controls'), $('div#citation-app-map'), urls, templates, service);

    app.init(parseInt(location.hash.slice(1)) || undefined);

    window.addEventListener("hashchange", function(event) {
        app.load(parseInt(location.hash.slice(1)) || undefined);
    }, false);

    $(document).foundation();
});
