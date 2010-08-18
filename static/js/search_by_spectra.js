
var SEARCH_BY_SPECTRA_LIMIT = 10;

Ext.madasSearchBySpectraPanel = {
    xtype:'form', 
    labelWidth: 100, // label settings here cascade unless overridden
    id:'searchbyspectra-panel',
    url:'search',
    method:'POST',
    frame:true,
    title: 'Search by Spectra',
    bodyStyle:'padding:5px 5px 0',
    width: 370,
    style:'margin-left:30px;margin-top:20px;',
    defaults: {width: 240},
    defaultType: 'textarea',
    items: [
         {
            fieldLabel: 'Spectra',
            name: 'spectra',
            height: 350
         }
        ],
    buttons: [{
            text: 'Search',
            id:'requestSearchSubmit',
            handler: function() {
                    var formValues = Ext.getCmp('searchbyspectra-panel').getForm().getValues();
                    Ext.madasSearchBySpectraResultsStore.baseParams = formValues;
                    Ext.madasSearchBySpectraResultsStore.load({params:{start:0, limit:SEARCH_BY_SPECTRA_LIMIT}});
                    Ext.madasSearchBySpectraResultsStore.removeAll();
                    Ext.madasChangeMainContent("search:byspectraresults");
                }
        },{
            text: 'Reset',
            handler: function(){
                Ext.getCmp('searchbyspectra-panel').getForm().reset();
            }
        }]
};

Ext.madasSearchBySpectraCmp = {   
    id:'searchbyspectra-container-panel', 
    items:[ 
        Ext.madasSearchBySpectraPanel 
    ]
};


