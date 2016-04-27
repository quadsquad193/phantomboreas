Citations = (function() {
    _modules = {
        Citation:           undefined,
        CitationApp:        undefined,
        CitationService:    undefined,
    };

    CitationRepr = function(repr) {
        Object.assign(this, repr);
     };

    CitationRepr.prototype.plate_image_url = function() {
        return _modules.Citation.urls.assets_capture + this.plate.capture_url;
    };

    CitationRepr.prototype.context_capture_url = function() {
        return _modules.Citation.urls.assets_capture + this.capture_url;
    };

    CitationRepr.prototype.plate_human_time = function() {
        return Utils.time.human_timestamp(this.plate.timestamp);
    };

    CitationRepr.prototype.context_human_time = function() {
        return Utils.time.human_timestamp(this.timestamp);
    };

    CitationRepr.prototype.is_actionable = function() {
        return !this.status.verified && !this.status.dismissed && !this.status.delegate_to;
    };

    CitationRepr.prototype.can_delegate_to = function() {
        return !this.status.delegations.length && this.is_actionable();
    }

    _modules.Citation = Citation = function(repr) {
        this.repr   = new CitationRepr(repr);

        this.id     = repr.citation_id;
        this.elem   = null;
        this.render();
    };

    Citation.templates = {};
    Citation.service = undefined;

    Citation.prototype.update = function(repr) {
        this.repr = new CitationRepr(repr);
        this.render();
    };

    Citation.prototype.render = function() {
        rendered = Mustache.render(Citation.templates.citation, this.repr);

        if (!this.elem)
            this.elem = $(rendered);
        else
            this.elem.html(rendered).off();

        this.bind();
        $(document).foundation();
    };

    Citation.prototype.bind = function() {
        service = Citation.service;

        $('.button.action-verify:first', this.elem).bind('click', {self: this}, function(event) {
            service.putCitation(event.data.self.id, 'verify', true);
        });
        $('.button.action-dismiss:first', this.elem).bind('click', {self: this}, function(event) {
            service.putCitation(event.data.self.id, 'dismiss', true);
        });
        $('.button.action-delegate-to:first', this.elem).bind('click', {self: this}, function(event) {
            if (to = $('input.delegate-to:first', event.data.self.elem).val()) service.putCitation(event.data.self.id, 'delegate_to', to);
        });
        $('.button.revoke-verify:first', this.elem).bind('click', {self: this}, function(event) {
            service.putCitation(event.data.self.id, 'verify', false);
        });
        $('.button.revoke-dismiss:first', this.elem).bind('click', {self: this}, function(event) {
            service.putCitation(event.data.self.id, 'dismiss', false);
        });
        $('.button.revoke-delegate-to:first', this.elem).bind('click', {self: this}, function(event) {
            service.putCitation(event.data.self.id, 'delegate_to', 0);
        });
    };

    _modules.CitationService = CitationService = function(baseUrl) {
        this.baseUrl = baseUrl;

        this.citations = {};
    };

    CitationService.prototype.flush = function() {
        this.citations = {};
    };

    CitationService.prototype.getCitation = function(id) {
        var self = this;

        return $.get(this.baseUrl + id, function(data) {
            response_citation = new Citation(data.citation);
            self.flush();
            self.citations[response_citation.id] = response_citation;
        }, 'json');
    };

    CitationService.prototype.getCitations = function() {
        var self = this;

        return $.get(this.baseUrl, function(data) {
            response_citations = data.citations;
            self.flush();
            for (var i = 0; i < response_citations.length; ++i) {
                response_citation = new Citation(response_citations[i]);
                self.citations[response_citation.id] = response_citation;
            }
        }, 'json');
    };

    CitationService.prototype.updateCitation = function(id) {
        var self = this;

        if (!self.citations.hasOwnProperty(id)) return;

        $.ajax({
            url: this.baseUrl + id,
            method: 'GET',
            dataType: 'json',
        }).done(function(data) {
            repr    = data.citation;
            id      = repr.citation_id;

            citation = self.citations[id];
            citation.update(repr);
        }).fail(function(data) {
            alert('Could not submit request.');
            console.log(data);
        });
    };

    CitationService.prototype.putCitation = function(id, key, value) {
        var self = this;

        data = {};
        data[key] = value;

        $.ajax({
            url: this.baseUrl + id,
            method: 'PUT',
            dataType: 'json',
            data: data,
        }).done(function(data) {
            repr        = data.citation;
            id          = repr.citation_id;

            citation    = self.citations[id];
            old_repr    = citation.repr

            citation.update(repr);

            if (key == 'delegate_to') {
                if (value == 0) self.updateCitation(old_repr.status.delegate_to);
                else self.updateCitation(repr.status.delegate_to);
            }
        }).fail(function(data) {
            alert('Could not submit request.');
            console.log(data);
        });
    };

    _modules.CitationApp = CitationApp = function(listContainer, urls, templates, service) {
        this.container  = listContainer;
        this.urls       = urls;
        this.templates  = templates;
        this.service    = service;
    };

    CitationApp.prototype.attach = function() {
        citations = this.service.citations;

        for (var id in citations) if (citations.hasOwnProperty(id))
            this.container.append(citations[id].elem);
    };

    CitationApp.prototype.detach = function() {
        this.container.empty();
    };

    CitationApp.prototype.init = function(id) {
        Citation.service = this.service;

        Citation.urls = this.urls;

        Mustache.parse(this.templates.citation);
        Citation.templates.citation = this.templates.citation;

        this.load(id);
    };

    CitationApp.prototype.load = function(id) {
        var self = this;

        promise = undefined;

        if (id == undefined) promise = this.service.getCitations();
        else promise = this.service.getCitation(id);

        promise.done(function() {
            self.detach();
            self.attach();
            $(document).foundation();
        });
    };

    return {
        service:    CitationService,
        app:        CitationApp,
    };
})();
