
var ImageManager = {
    cropper: null,
    mapcropper: null,

    init: function(spectrumId, interactive, queryspectra) {
        this.imageInfoHistory = [];
        this.spectrumId = spectrumId;
        this.queryspectra = queryspectra;
        this.initImages();
        if (interactive) {
            this.initCroppers();
        }
    },

    initImages: function() {
        if (typeof(this.queryspectra) === 'undefined'){
            $( 'graphmap_img' ).src = 'htt_image/' + this.spectrumId + '/' + this.queryspectra + '/';
        }
        else{
            $( 'graphmap_img' ).src = 'imagemap/' + this.spectrumId + '/'; 
        }
        this.loadStartImage();
    },

    initCroppers: function() {
        this.mapcropper = new Cropper.Img('graphmap_img',
            {
                minHeight: $('graphmap_img').height,
                onEndCrop: onMapEndCrop
            }
        );
        this.cropper = new Cropper.Img('graph_img',
            {
                minHeight: $('graph_img').height,
                onEndCrop: onEndCrop
            }
        );
    },

    redrawFrom: function(newImageInfo) {
        this.curImageInfo = newImageInfo;
        if (this.mapxrange !== undefined && this.mapxrange !== null) {
            // keep the mapcropper selection where it was
            // there are small differences between server-side and client-side
            // pixel values and it looks funny if the map cropper is resized
           this.curImageInfo.mapxstart = this.mapxrange.start;
           this.curImageInfo.mapxend = this.mapxrange.end;
        }
        this.setImages();
    },

    requestRedraw: function(request, mapxrange) {
        // mapxrange contains the start and end on the map image in pixels.
        // it is passed in only if the user was zooming the map not the image
        this.mapxrange = mapxrange;
        return new Ajax.Request('imageaction/', {
            asynchronous: false,
            postBody: Object.toJSON(request),
            onSuccess: redrawCallback
        });
    },

    crop: function(xstart, xend, type) {
        var zoomAction = 'zoom';
        var request = null;
        var mapxrange = null;
        if (type == 'map') { zoomAction = 'mapzoom'; }
        var xmin = this.curImageInfo.xstart;
        var xmax = this.curImageInfo.xend;
        if (xstart < xmin && xend < xmin) {
            this.moveLeft();
        } else if (xstart > xmax && xend > xmax) {
            this.moveRight();
        } else if (xend-xstart < 5) {
            this.loadStartImage();
        } else {
            request = this.buildRequest(zoomAction, {
                        newxstart: xstart,
                        newxend:   xend
                    });
            if (zoomAction == 'mapzoom') {
                mapxrange = {start: xstart, end: xend};
            }
            this.requestRedraw(request, mapxrange);
        }
    },

    moveLeft: function() {
        this.requestRedraw(
            this.buildRequest('moveLeft'));
    },

    moveRight: function() {
        this.requestRedraw(
            this.buildRequest('moveRight'));
    },

    loadStartImage: function() {
        this.requestRedraw(
            this.buildRequest('startImage'));
    },

    buildRequest: function(actionName,extraParams) { 
        var request = {
            spectrumId: this.spectrumId,
            action: actionName
        };                          
        if (this.curImageInfo) {
            request.datastart = this.curImageInfo.datastart;
            request.dataend = this.curImageInfo.dataend;
        }
        if (extraParams) {
            for (prop in extraParams) {
                request[prop] = extraParams[prop];
            }
        }
        return request;
    },

    setImages: function() {
        var imgInfo = this.curImageInfo;
        this.imageInfoHistory.push(imgInfo);
        var params = imgInfo.spectrumId + '/' +
                imgInfo.datastart + '/' +
                imgInfo.dataend + '/';
        $( 'graph_img' ).src = 'image/' + params; 
        if (this.cropper !== null) {
            this.updateCropper();
       }
        if (this.mapcropper !== null) {
            this.updateMapCropper(imgInfo);
        }
    },

    updateCropper: function() {
        if (Prototype.Browser.IE) {
            // for IE we remove and recreate the image cropper every time.
            // it isn't the nicest, but avoids IE hanging 
            this.cropper.remove();
            this.cropper = new Cropper.Img('graph_img', {
                   minHeight: $('graph_img').height,
                   onEndCrop: onEndCrop
                });
        } else {
            this.cropper.reset();
        }
    },

    updateMapCropper: function(imgInfo) {
        this.mapcropper.reset();
        if (imgInfo.mapxstart <= imgInfo.xstart && imgInfo.mapxend >= imgInfo.xend) {
            this.mapcropper.reset();
            return;
        }
        this.mapcropper.setAreaCoords({
                x1: imgInfo.mapxstart, 
                y1: 0, 
                x2: imgInfo.mapxend, 
                y2: $('graphmap_img').getHeight()
            }, false, false, null);
        this.mapcropper.selArea.show();
        this.mapcropper.drawArea();
    },

    historyBack: function() {
        var curImgInfo = null;
        var prevImgInfo = null;
        if (this.imageInfoHistory.length >= 2) {
            curImgInfo = this.imageInfoHistory.pop();
            prevImgInfo = this.imageInfoHistory.pop();
            this.mapxrange = null;
            this.redrawFrom(prevImgInfo);
        }
    }
};

function onEndCrop(coords, dimensions) {
    if (wasCropperReset(coords)) { return; }
    ImageManager.crop(coords.x1, coords.x2, 'graph');
}

function onMapEndCrop(coords, dimensions) {
    if (wasCropperReset(coords)) { return; }
    ImageManager.crop(coords.x1, coords.x2, 'map');
}

function wasCropperReset(coords) {
    if (coords.x1 === 0 && coords.x2 === 0) {
        return true;
    }
    return false;
}

function redrawCallback(transport) {
    var newImageInfo = transport.responseText.evalJSON(true);
    this.ImageManager.redrawFrom(newImageInfo);
}

function onMoveLeft() { ImageManager.moveLeft(); }
function onMoveRight() { ImageManager.moveRight(); }
function onReset() { ImageManager.loadStartImage(); }
function onHistoryBack() { ImageManager.historyBack(); }

function onLoad(spectrumId, interactive) {
    ImageManager.init(spectrumId, interactive);

    if (interactive) {
        Event.observe('back', 'click', onHistoryBack);
        Event.observe('reset', 'click', onReset);
        Event.observe('moveleft', 'click', onMoveLeft );
        Event.observe('moveright', 'click', onMoveRight );
    }
}

function viewGraph(id, id_type) {
    var param_name = 'compound_id';
    if (id_type == 'spectrum_id') {
        param_name = 'spectrum_id';
    }
    var url = 'mamboms/graph?' + param_name + '=' + id;
    var width = 1000;
    var height = 700;
    var x = (screen.width - width) / 2;
    var y = (screen.height - height) / 2;
    var props = "width=" + width + ", height=" + height + ", left=" + x + ", top=" + y;
    var win = window.open(url, 'graph_window', props);
    win.resizeTo(width,height);
    win.moveTo(x,y);
    win.focus();
}

