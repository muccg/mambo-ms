
madasShowGraphWindow = function(id, id_type) {
    console.log('Normal graph window');
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
    console.log('Head to tail window');
    var url = 'mamboms/graph/htt_image/' + compound_id + '/' + queryspectra;
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
