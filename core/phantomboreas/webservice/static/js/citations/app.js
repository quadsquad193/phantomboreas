$(document).ready(function() {
    urls = {
        assets_capture: '/assets/capture/',
    };
    templates   = {
        citation: $('#template-citation').html(),
    };
    service     = new Citations.service('/api/citation/');
    app         = new Citations.app($('#citation-app-container'), urls, templates, service);

    app.init(parseInt(location.hash.slice(1)) || undefined);

    window.addEventListener("hashchange", function(event) {
        app.load(parseInt(location.hash.slice(1)) || undefined);
    }, false);

    $(document).foundation();
});
