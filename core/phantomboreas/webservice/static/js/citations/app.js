$(document).ready(function() {
    urls = {
        assets_capture: '/assets/capture/',
    };
    templates   = {
        citation: $('#template-citation').html(),
    };
    service     = new Citations.service('/api/citation/');
    app         = new Citations.app($('#citation-app-container'), urls, templates, service);

    app.init();

    $(document).foundation();
});
