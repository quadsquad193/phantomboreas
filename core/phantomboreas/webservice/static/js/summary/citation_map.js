CitationMap = (function() {
	function CitationMap(selector, data) {
		this.mapElem = $(selector);
		this.mapElem.css('min-height','500px');
		this.mapmarkers = [];
		this.data = data;
	}

	CitationMap.prototype.render = function() {
		this.mapSetup();
		this.mapShowCoords();
	}

    CitationMap.prototype.mapSetup = function() {
        var self = this;

        self.map = L.map(self.mapElem.attr('id')).setView([0, 0], 1);

        navigator.geolocation.getCurrentPosition(function(pos) {
            self.map.setView([pos.coords.latitude, pos.coords.longitude]);
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

    CitationMap.prototype.mapShowCoords = function() {
    	var self = this;

		L.Map = L.Map.extend({
		    openPopup: function(popup) {
		        //        this.closePopup();  // just comment this
		        this._popup = popup;

		        return this.addLayer(popup).fire('popupopen', {
		            popup: this._popup
		        });
		    }
		});

    	this.data.citations.forEach(function(d, i) {
	        if (self.mapmarkers.length < (i+1)) {
	            self.mapmarkers.push(L.marker([0, 0]))
	            self.mapmarkers[i].addTo(self.map);
	        }

	        self.mapmarkers[i].setLatLng([d.evidence[0].coordinates.latitude, d.evidence[0].coordinates.longitude]);
	    });
    }

    return CitationMap;
})();