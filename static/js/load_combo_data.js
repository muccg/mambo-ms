Ext.madasComboData = {};

function loadComboData(url, key, mappingFn) {
    var conn = new Ext.data.Connection();
    if (mappingFn === undefined) {
        mappingFn = function(responseObject) {
            var data = Ext.decode(responseObject.responseText).data;
            var row;
            Ext.madasComboData[key] = [];
            for (var i = 0; i < data.length; i++) {
                row = data[i];
                Ext.madasComboData[key].push([row.id, row.name]);
            }
        };
    }
    conn.request({
        url: url,
        method: 'GET',
        success: mappingFn,
        failure: function() {
            Ext.Msg.alert('Error', 'Unable to load reference data.');
        }
    });
}

loadComboData('reference/mass_spectra_types/', 'massSpectraTypes');
loadComboData('reference/precursor_selections/', 'precursorSelections');
loadComboData('reference/precursor_types/', 'precursorTypes', function(responseObject) {
    var data = Ext.decode(responseObject.responseText).data;
    var row;
    var i;
    Ext.madasComboData.precursorTypes = {'Positive': [], 'Negative': []};
    for (i = 0; i < data.P.length; i++) {
        row = data.P[i];
        Ext.madasComboData.precursorTypes.Positive.push([row.id, row.name]);
    }
    for (i = 0; i < data.N.length; i++) {
        row = data.N[i];
        Ext.madasComboData.precursorTypes.Negative.push([row.id, row.name]);
    }
    
});
