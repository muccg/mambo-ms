
var SEARCH_RESULTS_LIMIT = 30;
 
Ext.madasSearchByKeywordPanelValidator = function() {
    var mol_weight_start = Ext.getCmp('mol_weight_start').getValue();
    var mol_weight_end = Ext.getCmp('mol_weight_end').getValue();
    if (mol_weight_start !== '' && mol_weight_end !== '') {
        if (mol_weight_end < mol_weight_start) {
            Ext.getCmp('mol_weight_start').markInvalid('Invalid range for the molecular weight field.');
            Ext.getCmp('mol_weight_end').markInvalid('Invalid range for the molecular weight field.');
            return false;
        }
    }

    return true;
};

Ext.madasSearchByKeywordPanelInit = function() {
    Ext.getCmp('nist_dataset').setValue(!Ext.madasIsClient);
    Ext.getCmp('nist_dataset').setDisabled(Ext.madasIsClient);
};

Ext.madasDeselectNIST = function() {
    Ext.getCmp('nist_dataset').setValue(false);
};

Ext.madasSearchByKeywordPanel = {
    xtype:'form', 
    labelWidth: 150, // label settings here cascade unless overridden
    id:'searchbykeyword-panel',
    url:'search',
    method:'POST',
    frame:true,
    title: 'Search',
    bodyStyle:'padding:5px 5px 0',
    width: 430,
    style:'margin-left:30px;margin-top:20px;',
    defaults: {width: 250},
    defaultType: 'textfield',
    items: [
        {
            xtype: 'checkboxgroup',
            fieldLabel: 'Dataset',
            columns: 1,
            items: [
                {boxLabel: 'NIST', id: 'nist_dataset', name: 'dataset', inputValue: 'NIST', checked: true},
                {boxLabel: 'MA GC metabolite records', id: 'ma_gc_dataset', inputValue: 'MA GC', name: 'dataset', checked: true},
                {boxLabel: 'MA LC metabolite records', id: 'ma_lc_dataset', inputValue: 'MA LC', name: 'dataset', checked: true}
            ]
        },
        {
            fieldLabel: 'Compound Name',
            maxLength: 2000,
            name: 'compound_name'
        },
        {
            xtype: 'radiogroup',
            items: [
                {boxLabel: 'contains', name: 'compound_name_match_type', inputValue: 'contains', checked: true},
                {boxLabel: 'starts with', name: 'compound_name_match_type', inputValue: 'starts with'},
                {boxLabel: 'exact      ', name: 'compound_name_match_type', inputValue: 'exact', width: 30}
            ]
        },
        {
            fieldLabel: 'CAS Registration Number',
            maxLength: 255,
            name: 'cas_regno'
        },{
            fieldLabel: 'Molecular Formula',
            maxLength: 255,
            name: 'mol_formula'
         },{
            fieldLabel: 'Molecular Weight',
            xtype: 'panel',
            layout: 'hbox',
            columns: 2,
            items: [
                { 
                    xtype: 'numberfield',
                    id: 'mol_weight_start',
                    name: 'mol_weight_start',
                    margins: '0 0 5 0',
                    maxLength: 10,
                    width: 70
                },{
                    xtype: 'numberfield',
                    id: 'mol_weight_end',
                    name: 'mol_weight_end',
                    margins: '0 5',
                    maxLength: 10,
                    width: 70
                }
            ]
        },
        {
            fieldLabel: 'Mono Isotopic Mass (LC Only)', 
            xtype: 'numberfield',
            decimalPrecision:5,
            id: 'mono_isotopic_mass',
            name: 'mono_isotopic_mass',
            margins: '0 5',
            maxLength: 10,
            width: 70
        },
       {xtype:'fieldset',
        title:'Advanced Search',
        id:'advancedsearchFieldset',
        autoHeight:true,
        autoWidth:true,
        items:[

        {
            id: 'advancedSearchText',
            html: '<i>Using Advanced Search fields will automatically deselect NIST from the searched datasets. To force inclusion of NIST, reselect it before clicking Search.</i>',
            style: {
                /*'font-weight' : 'bold',*/
                'margin' : '0px 0px 5px 0px'
            }
        },
       new Ext.ux.form.LovCombo({
		    fieldLabel: 'Derivitization Agent',
		    name: 'derivitization_agent',
            hideOnSelect:false,
            store: new Ext.data.JsonStore({
                    proxy: new Ext.data.HttpProxy({ url:'reference/derivitization_agents' , method: 'GET'}),
                    root: 'data',
                    autoLoad: true,
                    fields: ['name']
                }),
            editable: false,
            //lazyRender: true,
            valueField: 'name',
            displayField: 'name',
		    triggerAction:'all',
		    mode:'local',
            addSelectAllItem:true,
            listeners: { 'blur' : Ext.madasDeselectNIST }  
	    }),
        new Ext.ux.form.LovCombo({
		    fieldLabel: 'Chromatography Type',
            name: 'chromatography_type',
		    hideOnSelect:false,
            store: new Ext.data.JsonStore({
                    proxy: new Ext.data.HttpProxy({ url:'reference/chromatography_types' , method: 'GET'}),
                    root: 'data',
                    autoLoad: true,
                    fields: ['name', 'id']
                }),
            editable: false,
            //lazyRender: true,
            valueField: 'id',
            hiddenName: 'chromatography_type',
            displayField: 'name',
		    triggerAction:'all',
		    mode:'local',
            listeners: { 'blur' : Ext.madasDeselectNIST },  
            addSelectAllItem:true
        }),
        new Ext.ux.form.LovCombo({
		    id: 'geom_combo',
            fieldLabel: 'MS Geometry',
            name: 'ms_geometery',
		    hideOnSelect:false,
            store: new Ext.data.JsonStore({
                    proxy: new Ext.data.HttpProxy({ url:'reference/msgeometry_types' , method: 'GET'}),
                    root: 'data',
                    autoLoad: true,
                    fields: ['name', 'id']
                }),
            editable: false,
            //lazyRender: true,
            valueField: 'id',
            hiddenName: 'ms_geometry',
            displayField: 'name',
		    triggerAction:'all',
		    mode:'local',
            listeners: { 'blur' : Ext.madasDeselectNIST },  
            addSelectAllItem:true
        }),
        new Ext.ux.form.LovCombo({
		    id: 'mass_spectra_types_combo',
            fieldLabel: 'Mass Spectra (LC Only)',
            name: 'mass_spectra_types',
		    hideOnSelect:false,
            store: new Ext.data.JsonStore({
                    proxy: new Ext.data.HttpProxy({ url:'reference/mass_spectra_types' , method: 'GET'}),
                    root: 'data',
                    autoLoad: true,
                    fields: ['name', 'id']
                }),
            editable: false,
            //lazyRender: true,
            valueField: 'id',
            hiddenName: 'mass_spectra_types',
            displayField: 'name',
		    triggerAction:'all',
		    mode:'local',
            listeners: { 'blur' : Ext.madasDeselectNIST },  
            addSelectAllItem:true
        }),
        new Ext.ux.form.LovCombo({
		    fieldLabel: 'Ionization Mode',
            name: 'ionization_mode',
		    hideOnSelect:false,
            store: new Ext.data.JsonStore({
                    proxy: new Ext.data.HttpProxy({ url:'reference/ionization_modes' , method: 'GET'}),
                    root: 'data',
                    autoLoad: true,
                    fields: ['name', 'id']
                }),
            editable: false,
            //lazyRender: true,
            valueField: 'id',
            hiddenName: 'ionization_mode',
            displayField: 'name',
		    triggerAction:'all',
		    mode:'local',
            listeners: { 'blur' : Ext.madasDeselectNIST },  
            addSelectAllItem:true
        }),
        new Ext.ux.form.LovCombo({
		    fieldLabel: 'Polarity',
            name: 'polarity',
		    hideOnSelect:false,
            store: new Ext.data.JsonStore({
                    proxy: new Ext.data.HttpProxy({ url:'reference/polarities' , method: 'GET'}),
                    root: 'data',
                    autoLoad: true,
                    fields: ['name', 'id']
                }),
            editable: false,
            //lazyRender: true,
            valueField: 'id',
            hiddenName: 'polarity',
            displayField: 'name',
		    triggerAction:'all',
		    mode:'local',
            listeners: { 'blur' : Ext.madasDeselectNIST },  
            addSelectAllItem:true
        }),
        new Ext.ux.form.LovCombo({
            fieldLabel: 'Biological Systems',
            name: 'biological_systems',
		    hideOnSelect:false,
            store: new Ext.data.JsonStore({
                    proxy: new Ext.data.HttpProxy({ url:'reference/biological_systems' , method: 'GET'}),
                    root: 'data',
                    autoLoad: true,
                    fields: ['name', 'id']
                }),
            editable: false,
            //lazyRender: true,
            valueField: 'id',
            hiddenName: 'biological_systems',
            displayField: 'name',
		    triggerAction:'all',
		    mode:'local',
            listeners: { 'blur' : Ext.madasDeselectNIST },  
            addSelectAllItem:true
        }),
        new Ext.ux.form.LovCombo({
            fieldLabel: 'Metabolite Class',
            name: 'metabolite_class',
		    hideOnSelect:false,
            store: new Ext.data.JsonStore({
                    proxy: new Ext.data.HttpProxy({ url:'reference/metabolite_classes' , method: 'GET'}),
                    root: 'data',
                    autoLoad: true,
                    fields: ['name', 'id']
                }),
            editable: false,
            //lazyRender: true,
            valueField: 'id',
            hiddenName: 'metabolite_class',
            displayField: 'name',
		    triggerAction:'all',
		    mode:'local',
            listeners: { 'blur' : Ext.madasDeselectNIST },  
            addSelectAllItem:true
        }),
        {
            fieldLabel: 'Retention Time', 
	        xtype: 'numberfield',
            decimalPrecision:5,
            id: 'retention_time',
            name: 'retention_time',
            margins: '0 5',
            listeners: { 'blur' : Ext.madasDeselectNIST },  
            maxLength: 10,
            width: 70	
        }
        ] //end fieldset items
        } //end fieldset definition
        ],
    buttons: [{
            text: 'Search',
            id:'requestSearchSubmit',
            handler: function() {
                var formValue = null;
                if (!Ext.getCmp('searchbykeyword-panel').getForm().isValid()) {
                    alert('Please correct the validation errors first!');
                }
                else {
                    // custom validation
                    if (!Ext.madasSearchByKeywordPanelValidator()) {
                        alert('Please correct the validation errors first!');
                    } else {
                        formValues = Ext.getCmp('searchbykeyword-panel').getForm().getValues();
                        Ext.madasSearchByKeywordResultsStore.baseParams = formValues;
                        Ext.madasSearchByKeywordResultsStore.load({params:{start:0, limit:SEARCH_RESULTS_LIMIT}});
                        Ext.madasSearchByKeywordResultsStore.removeAll();
                        Ext.updateSearchByKeywordResultsInfoPanel(formValues);
                        Ext.madasChangeMainContent("search:bykeywordresults");
                    }
                }}
        },{
            text: 'Reset',
            handler: function(){
                Ext.getCmp('searchbykeyword-panel').getForm().reset();
            }
        }]
};

Ext.madasSearchByKeywordCmp = {   
    id:'searchbykeyword-container-panel', 
    autoScroll: true,
    items:[ 
        Ext.madasSearchByKeywordPanel 
    ]
};


