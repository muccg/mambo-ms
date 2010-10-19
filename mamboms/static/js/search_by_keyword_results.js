
Ext.Ajax.on('requestexception', function(conn, response, options) {
    // Unauthorized
    if (response.status == 401) {
        Ext.madasChangeMainContent('login');
    } 
    // Forbidden
    if (response.status == 403) {
        Ext.madasChangeMainContent('notauthorized');
    } 
}, this);

Ext.madasSearchByKeywordResultsStore = new Ext.data.JsonStore({
    autoDestroy: true,
    url: 'mamboms/search/bykeyword/',
    storeId: 'searchByKeywordStore',
    root: 'data',
    idProperty: 'id',
    totalProperty: 'results',
    remoteSort: true,
    fields: ['id', 'cas_name', 'compound_name', 'node', 'dataset', 'cas_regno', 'mol_formula', {name: 'mol_weight', type: 'float'}, 'record_uploaded_by']
});

Ext.madasSearchByKeywordResultsGridCmp = Ext.madasCreateSearchResultsGridCmp({
    store: Ext.madasSearchByKeywordResultsStore,
    componentName: 'search:bykeywordresults',
    idPrefix: 'searchbykeyword-',
    pagingOn: true,
    limit: SEARCH_RESULTS_LIMIT
});

Ext.madasSearchByKeywordResultsInfoPanel = Ext.madasCreateSearchResultsInfoPanel({
    idPrefix: 'searchbykeyword-',
    button: { text: 'Refine Your Search', searchCmpId: 'searchbykeyword-container-panel'}
});

Ext.madasSearchByKeywordResultsCmp = {
    id:'searchbykeyword-results-panel',
    title: 'Search Results',
    layout: 'border',
    deferredRender: false,
    forceLayout: true,
    defaults: {
        deferredRender: false,
        forceLayout: true
    },
    items: [
        Ext.madasSearchByKeywordResultsInfoPanel,
        Ext.madasSearchByKeywordResultsGridCmp
     ]
};

Ext.updateSearchByKeywordResultsInfoPanel = function(formValues) {
    var infoText = '';
    var datasets = null;
    var where = '';
    var matchType = null;
    var relation = '';
    var value = '';
    if (typeof(formValues.dataset) == "undefined") {
        infoText = 'Please select at least one dataset or no search results can be returned.';
    } else {
        datasets = formValues.dataset;
        where = '';
        if (formValues.cas_name !== '') {
            where += 'the <i>CAS Name</i> ';
            matchType = formValues.cas_name_match_type;
            if (matchType == 'exact') { matchType = 'is'; }
            where += matchType + ' "'  + formValues.cas_name + '" and '; 
        }
        if (formValues.compound_name !== '') {
            where += 'the <i>Compound Name</i> ';
            matchType = formValues.compound_name_match_type;
            if (matchType == 'exact') { matchType = 'is'; }
            where += matchType + ' "'  + formValues.compound_name + '" and '; 
        }
        if (formValues.cas_regno !== '') {
            where += 'the <i>CAS Registration Number</i> is "' + 
                     formValues.cas_regno + '" and ';
        }
        if (formValues.mol_formula !== '') {
            where += 'the <i>Molecular Formula</i> is "' + 
                     formValues.mol_formula + '" and ';
        }
        if (formValues.mol_weight_start !== '' || formValues.mol_weight_end !== '') {
            if (formValues.mol_weight_start !== '' && formValues.mol_weight_end !== '') {
                relation = 'between';
                value = formValues.mol_weight_start + ' and ' + 
                        formValues.mol_weight_end ;
            } else if (formValues.mol_weight_start !== '') {
                relation = 'greater than';
                value = formValues.mol_weight_start; 
            } else if (formValues.mol_weight_end !== '') {
                relation = 'less than';
                value = formValues.mol_weight_end; 
            }
            where += 'the <i>Molecular Weight</i> is ' + 
                     relation + ' ' + value + ' and '; 
        }


        if (where === '') {
            infoText = 'You are searching for <b>all</b> <i>' + datasets + '</i> records';
        } else {
            where = where.substring(0, where.length - ' and '.length);
            infoText = 'You are searching for <i>' + datasets + '</i> records where ' + where;
        }
        infoText += '.';
    }
    Ext.getCmp('searchbykeyword-results-info-panel-text').body.dom.innerHTML = infoText;
};

