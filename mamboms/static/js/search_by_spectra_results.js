
Ext.madasSearchBySpectraResultsStore = new Ext.data.JsonStore({
    autoDestroy: true,
    url: 'mamboms/search/byspectra/',
    storeId: 'searchBySpectraStore',
    root: 'data',
    idProperty: 'id',
    totalProperty: 'results',
    fields: ['id', {name: 'score', type: 'float'}, 'cas_name', 'node', 'dataset', 'cas_regno', 'mol_formula', {name: 'mol_weight', type: 'float'}, 'record_uploaded_by']
});

Ext.madasSearchBySpectraResultsGridCmp = Ext.madasCreateSearchResultsGridCmp({
        store: Ext.madasSearchBySpectraResultsStore,
        idPrefix: 'searchbyspectra-',
        componentName: 'search:byspectraresults',
        extraColumns: [
                {position: 2,
                 column: {
                    id: 'score_col',
                    header: "Score (%)",
                    dataIndex: 'score',
                    align: 'center',
                    width: 20,
                    sortable: true
                   }
                }
            ],
});
//Override the single click behaviour
Ext.madasSearchBySpectraResultsGridCmp.items[0].listeners.rowclick = function(grid, rowIndex, evt){
    Ext.mambomsSearchResultsClickBehaviour(grid, rowIndex, evt);
    if (typeof(grid.selModel) != 'undefined' && grid.selModel.hasSelection()){
        Ext.mambomsPopulateHeadToTail(grid.selModel.getSelected().data.id);
    }
};


Ext.madasSearchBySpectraResultsInfoPanel = Ext.madasCreateSearchResultsInfoPanel({
    idPrefix: 'searchbyspectra-',
    button: { text: 'Search again', searchCmpId: 'searchbyspectra-container-panel'}
});

Ext.mambomsSearchBySpectraResultsHeadToTailPanel = Ext.mambomsCreateSearchResultsHeadToTailPanel({idPrefix: 'headtotail-'});

Ext.mambomsPopulateHeadToTail = function(compoundid){
    var ifr = Ext.getCmp('headtotail-graphiframe');
    var stb = Ext.getCmp('spectra_textbox').getValue();
    stb = stb.replace(/\s+/gi, ',');
    stb = stb.replace(/[,]+$/g, '');
    ifr.stb = stb;
    ifr.compoundid = compoundid;
    ifr.reload(ifr, compoundid, 'mamboms/graph/htt_image/' + compoundid + '/' + stb + '/');

};

Ext.madasSearchBySpectraResultsCmp = {
    id:'searchbyspectra-results-panel',
    title: 'Search Results',
    layout: 'border',
    items: [
        Ext.madasSearchBySpectraResultsInfoPanel,
        Ext.madasSearchBySpectraResultsGridCmp,
        Ext.mambomsSearchBySpectraResultsHeadToTailPanel
     ]
};

