
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
            ]
});

Ext.madasSearchBySpectraResultsInfoPanel = Ext.madasCreateSearchResultsInfoPanel({
    idPrefix: 'searchbyspectra-',
    button: { text: 'Search again', searchCmpId: 'searchbyspectra-container-panel'}
});

Ext.madasSearchBySpectraResultsCmp = {
    id:'searchbyspectra-results-panel',
    title: 'Search Results',
    layout: 'border',
    items: [
        Ext.madasSearchBySpectraResultsInfoPanel,
        Ext.madasSearchBySpectraResultsGridCmp
     ]
};
