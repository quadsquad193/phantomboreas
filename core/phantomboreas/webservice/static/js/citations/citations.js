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
    };

    CitationRepr.prototype.has_delegations = function() {
        return this.status.delegations.length > 0;
    };

    _modules.Citation = Citation = function(repr) {
        this.repr   = new CitationRepr(repr);

        this.id     = repr.citation_id;
        this.elem   = null;
        this.render();
    };

    Citation.templates = {};
    Citation.app = undefined;
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
        app = Citation.app;
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
        $('.revoke-verify:first', this.elem).bind('click', {self: this}, function(event) {
            service.putCitation(event.data.self.id, 'verify', false);
        });
        $('.revoke-dismiss:first', this.elem).bind('click', {self: this}, function(event) {
            service.putCitation(event.data.self.id, 'dismiss', false);
        });
        $('.revoke-delegate-to:first', this.elem).bind('click', {self: this}, function(event) {
            service.putCitation(event.data.self.id, 'delegate_to', 0);
        });
        $('.button.map-coords', this.elem).bind('click', {self: this}, function(event) {
            app.mapShowCoords(event.data.self.id, parseFloat($(this).attr('data-longitude')), parseFloat($(this).attr('data-latitude')));
        });
    };

    _modules.CitationService = CitationService = function(baseUrl) {
        this.baseUrl = baseUrl;

        this.citations = {};
    };

    CitationService.prototype.flush = function() {
        this.citations = {};
    };

    CitationService.prototype.responseCitation = function(data) {
        response_citation = new Citation(data.citation);
        this.flush();
        this.citations[response_citation.id] = response_citation;
    };

    CitationService.prototype.responseCitations = function(data) {
        response_citations = data.citations;
        this.flush();
        for (var i = 0; i < response_citations.length; ++i) {
            response_citation = new Citation(response_citations[i]);
            this.citations[response_citation.id] = response_citation;
        }
    };

    CitationService.prototype.searchCitations = function(form) {
        var self = this;

        return $.get(this.baseUrl + 'search', form.serialize(), function(data) {
            self.responseCitations(data);
        }, 'json');
    };

    CitationService.prototype.getCitation = function(id) {
        var self = this;

        return $.get(this.baseUrl + id, function(data) {
            self.responseCitation(data);
        }, 'json');
    };

    CitationService.prototype.getCitations = function() {
        var self = this;

        return $.get(this.baseUrl, function(data) {
            self.responseCitations(data);
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

    _modules.CitationApp = CitationApp = function(listContainer, searchElem, controlElem, mapElem, urls, templates, service) {
        this.container      = listContainer;
        this.searchElem     = searchElem;
        this.controlElem    = controlElem;
        this.mapElem        = mapElem;
        this.urls           = urls;
        this.templates      = templates;
        this.service        = service;
    };

    CitationApp.prototype.refresh = function() {
        this.detach();
        this.attach();
        $(document).foundation();
    };

    CitationApp.prototype.attach = function() {
        citations = this.service.citations;

        for (var id in citations) if (citations.hasOwnProperty(id))
            this.container.append(citations[id].elem);
    };

    CitationApp.prototype.detach = function() {
        this.container.empty();
    };

    CitationApp.prototype.search = function() {
        var self = this;

        this.service.searchCitations(this.searchElem).done(function() {
            self.refresh();
        }).fail(function(response) {
            alert(response.responseJSON.message);
        });
    };

    CitationApp.prototype.init = function(id) {
        Citation.app = this;
        Citation.service = this.service;

        Citation.urls = this.urls;

        Mustache.parse(this.templates.citation);
        Citation.templates.citation = this.templates.citation;

        this.mapSetup();
        this.bindings();

        this.load(id);
    };

    CitationApp.prototype.mapSetup = function() {
        var self = this;

        self.map = L.map(self.mapElem.attr('id')).setView([0, 0], 1);

        navigator.geolocation.getCurrentPosition(function(pos) {
            self.map.setView([pos.coords.latitude, pos.coords.longitude], 13);
        }, function() {
            console.warn('Could not get geolocation.');
        });

        L.tileLayer('https://api.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            id: mapbox_api.id,
            accessToken: mapbox_api.accessToken,
        }).addTo(this.map);
    };

    CitationApp.prototype.mapShowCoords = function(id, longitude, latitude) {
        if (this.mapmarker == undefined) {
            this.mapmarker = L.marker([0, 0], {icon: L.divIcon({className: 'leaflet-map-icon'})}).addTo(this.map);
            this.mapmarker.bindPopup('<span>Citation Label</span>');
        }

        this.mapmarker.setLatLng([latitude, longitude]);
        this.mapmarker.getPopup().setContent('<span>Citation #' + id + '</span>');
        this.mapmarker.openPopup();
        this.map.setView([latitude, longitude], 17);
    }

    CitationApp.prototype.bindings = function() {
        var self = this;

        $('a#citation-search-submit', this.searchElem).click(function(e) {
            self.search();
        });

        $('a#citation-search-reset', this.searchElem).click(function(e) {
            self.searchElem[0].reset();
            $('input[type=datetime-local]', this.searchElem).removeClass('bad-input not-paired');
            $('span.error', this.searchElem).removeClass('show');
            location.hash = '#';
        });

        $('input[type=datetime-local]', this.searchElem).keyup(function(e) {
            if ($(this)[0].validity.badInput) {
                $(this).addClass('bad-input');
                $(this).siblings('span.error.bad-input').addClass('show');
            } else {
                $(this).removeClass('bad-input');
                $(this).siblings('span.error.bad-input').removeClass('show');
            }
        });

        $('input[type=datetime-local][name=start_datetime]', this.searchElem).keyup(function(e) {
            if (!$('input[type=datetime-local][name=end_datetime]', this.searchElem)[0].value) {
                $('input[type=datetime-local][name=end_datetime]', this.searchElem).addClass('not-paired');
                $('input[type=datetime-local][name=end_datetime]', this.searchElem).siblings('span.error.not-paired').addClass('show');
            }

            if ($(this)[0].value) {
                $(this).removeClass('not-paired');
                $(this).siblings('span.error.not-paired').removeClass('show');
            }
        });

        $('input[type=datetime-local][name=end_datetime]', this.searchElem).keyup(function(e) {
            if (!$('input[type=datetime-local][name=start_datetime]', this.searchElem)[0].value) {
                $('input[type=datetime-local][name=start_datetime]', this.searchElem).addClass('not-paired');
                $('input[type=datetime-local][name=start_datetime]', this.searchElem).siblings('span.error.not-paired').addClass('show');
            }

            if ($(this)[0].value) {
                $(this).removeClass('not-paired');
                $(this).siblings('span.error.not-paired').removeClass('show');
            }
        });

        $('a#citation-control-toggle-verified', this.controlElem).click(function(e) {
            $(this).toggleClass('hollow');
            self.container.toggleClass('hide-verified');
        });

        $('a#citation-control-toggle-dismissed', this.controlElem).click(function(e) {
            $(this).toggleClass('hollow');
            self.container.toggleClass('hide-dismissed');
        });

        $('a#citation-control-toggle-delegate-to', this.controlElem).click(function(e) {
            $(this).toggleClass('hollow');
            self.container.toggleClass('hide-delegate-to');
        });

        $('a#citation-control-toggle-evidence', this.controlElem).click(function(e) {
            $(this).toggleClass('hollow');
            self.container.toggleClass('hide-evidence');
        });
    }

    CitationApp.prototype.load = function(id) {
        var self = this;

        promise = undefined;

        if (id == undefined) promise = this.service.getCitations();
        else promise = this.service.getCitation(id);

        promise.done(function() {
            self.refresh();
        });
    };

    return {
        service:    CitationService,
        app:        CitationApp,
    };
})();
