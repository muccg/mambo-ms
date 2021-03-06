
madasShowGraphWindow = function(id, id_type) {
    var param_name = 'compound_id';
    if (id_type == 'spectrum_id') {
        param_name = 'spectrum_id';
    }
    var url = 'mamboms/graph/page?' + param_name + '=' + id;
    var width = 1000;
    var height = 700;
    var x = (screen.width - width) / 2;
    var y = (screen.height - height) / 2;
    var props = "width=" + width + ", height=" + height + ", left=" + x + ", top=" + y;
    var win = window.open(url, 'graph_window', props);
    win.resizeTo(width,height);
    win.moveTo(x,y);
    win.focus();
};

mambomsShowHeadToTailWindow = function(compound_id, queryspectra){
    console.log('show head to tail window, queryspectra is ' + queryspectra);
    var url = 'mamboms/graph/page_htt?compound_id=' + compound_id + '&queryspectra=' + queryspectra;
    var width = 1000;
    var height = 700;
    var x = (screen.width - width) / 2;
    var y = (screen.height - height) / 2;
    var props = "width=" + width + ", height=" + height + ", left=" + x + ", top=" + y;
    var win = window.open(url, 'htt_graph_window', props);
    win.resizeTo(width,height);
    win.moveTo(x,y);
    win.focus();
};
