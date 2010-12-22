
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
            xtype: 'checkboxgroup',
            fieldLabel: 'Dataset',
            columns: 1,
            items: [
                {boxLabel: 'NIST', id: 'nist_dataset_spectra', name: 'dataset', inputValue: 'NIST', checked: true},
                {boxLabel: 'MA GC metabolite records', id: 'ma_gc_dataset_spectra', inputValue: 'MA GC', name: 'dataset', checked: true},
                {boxLabel: 'MA LC metabolite records', id: 'ma_lc_dataset_spectra', inputValue: 'MA LC', name: 'dataset', checked: true}
            ]
         } ,
         new Ext.form.ComboBox({
            fieldLabel: 'Algorithm',
            name: 'spectral_algorithm',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'id',
            hiddenName:'spectral_algorithm',
            lazyRender:true,
            typeAhead:false,
            triggerAction:'all',
            listWidth:230,
            allowBlank: false,
            disabled: that.readOnly,        
            mode: 'local',
            /* Note: Keep the algorithm id fields constant */
            store: new Ext.data.ArrayStore(
                    {
                        id:0,
                        fields: ['id', 'name'],
                        data: [[1, 'MA In House'], [2, 'Standard Dot Product']]
                    })
        }),
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


