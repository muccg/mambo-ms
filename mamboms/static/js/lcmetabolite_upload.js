Ext.madasLCMetaboliteUploadPostActivate = function() {
    // Adding an initial tab has to be done after the main form panel has been
    // activated, otherwise width will be set to 0 on the tabs and all children.
    var tabs = Ext.getCmp('upload-lcspectrum-tabpanel');
    tabs.createNewTabs(1);
};

Ext.madasLCMetaboliteUploadInit = function(params) {
    var form = Ext.getCmp('upload-lcmetabolite-panel').getForm(); 
    form.reset(); 
    Ext.mambomsLoadCombos(form, params, Ext.emptyFn, metabolite_combo_names); 
};

Ext.madasLCMetaboliteViewInit = function(params) {
    var form = Ext.getCmp('view-lcmetabolite-panel').getForm(); 
    Ext.madasMetaboliteLoadCombosAndForm(form, params,
            function(form, action) {
                if (Ext.getCmp('view-lcmetabolite-can-vet').getValue() !== "false") {
                    Ext.getCmp('view-lcmetabolite-vet').enable();
                } else {
                    Ext.getCmp('view-lcmetabolite-vet').disable();
                }
             }
    );
};

Ext.madasLCMetaboliteEditInit = function(params) {
    var savedMsg = Ext.getCmp('edit-lcsaved-message');
    if (typeof params.justUploaded !== 'undefined') {
        savedMsg.setHeight(28);
    } else {
        savedMsg.setHeight(0);
    }
    var form = Ext.getCmp('edit-lcmetabolite-panel').getForm(); 
    Ext.madasMetaboliteLoadCombosAndForm(form, params, Ext.emptyFn);
};

Ext.madasSpectrumTabCreator = function(idPrefix, index, readOnly) {
    var spectrumId =  'spectrum' + index;

    var markTabInvalidListeners = {
        invalid: function(field, msg) {
            var panel = Ext.getCmp(idPrefix + spectrumId + '-tab');
            panel.setTitle("<font color=\"red\">" + panel.title + "</font>");
        },
        valid: function(field) {
            var panel = Ext.getCmp(idPrefix + spectrumId + '-tab');
            panel.setTitle('Spectrum');
        }
    };
    return {
        id: idPrefix + spectrumId + '-tab',
        title:'Spectrum',
        layout:'column',
        items: [{
                columnWidth: 0.5,
                defaultType: 'textfield',
                defaults: {width: 230},
                labelWidth: 120,
                layout: 'form',
                itemId: 'col1',
                items: [{
                        fieldLabel: 'Spectral ID',
                        name: spectrumId + '_id_display',
                        disabled: true
                    },{
                        //itemId: 'specid',
                        xtype: 'hidden',
                        id: idPrefix + spectrumId + 'id',
                        name: spectrumId + '_id'
                    }, new Ext.form.ComboBox({
                        id: idPrefix + spectrumId + 'mass-spectra-type',
                        fieldLabel: 'Mass Spectra Type',
                        editable:false,
                        forceSelection:true,
                        displayField:'name',
                        valueField:'id',
                        hiddenName:spectrumId + '_mass_spectra_type',
                        lazyRender:true,
                        typeAhead:false,
                        triggerAction:'all',
                        listWidth:230,
                        allowBlank: false,
                        mode: 'local',
                        disabled: readOnly,
                        listeners: markTabInvalidListeners,
                        store: new Ext.data.ArrayStore({
                            idIndex: 0,
                            fields: ['id', 'name']
                        })
                    }),{
                        fieldLabel: 'Description',
                        name: spectrumId + '_description',
                        allowBlank: false,
                        listeners: markTabInvalidListeners,
                        disabled: readOnly
                    },{
                        id: idPrefix + spectrumId + 'ionization-mode',
                        fieldLabel: 'Ionization Mode',
                        name: spectrumId + '_ionization_mode',
                        disabled: true
                    },{
                        id: idPrefix + spectrumId + 'polarity',
                        fieldLabel: 'Polarity',
                        name: spectrumId + '_polarity',
                        disabled: true
                    }, new Ext.form.ComboBox({
                        id: idPrefix + spectrumId + 'precursor-selection',
                        fieldLabel: 'Precursor Selection',
                        editable:false,
                        forceSelection:true,
                        displayField:'name',
                        valueField:'id',
                        hiddenName:spectrumId + '_precursor_selection',
                        lazyRender:true,
                        lazyInit: false,
                        typeAhead:false,
                        triggerAction:'all',
                        listWidth:230,
                        allowBlank: false,
                        mode: 'local',
                        disabled: readOnly,
                        listeners: markTabInvalidListeners,
                        store: new Ext.data.ArrayStore({
                            idIndex: 0,
                            fields: ['id', 'name']
                        })
                    }), new Ext.form.ComboBox({
                        id: idPrefix + spectrumId + 'precursor-type',
                        fieldLabel: 'Precursor Type',
                        editable:false,
                        forceSelection:true,
                        displayField:'name',
                        valueField:'id',
                        hiddenName:spectrumId + '_precursor_type',
                        lazyRender:true,
                        typeAhead:false,
                        triggerAction:'all',
                        listWidth:230,
                        allowBlank: false,
                        mode: 'local',
                        disabled: readOnly,
                        listeners: markTabInvalidListeners,
                        store: new Ext.data.ArrayStore({
                            idIndex: 0,
                            fields: ['id', 'name']
                        })
                    }),{
                        fieldLabel: 'Collison Energy',
                        allowBlank: false,
                        disabled: readOnly,
                        listeners: markTabInvalidListeners,
                        name: spectrumId + '_collison_energy'
                    }, new Ext.ux.form.LovCombo({
                        id: idPrefix + spectrumId + 'ionized_species',
                        name: idPrefix + spectrumId + 'ionized_species',
                        fieldLabel: 'Ionized Species',
                        store: new Ext.data.ArrayStore({
                            //idIndex: 0,
                            fields: ['id', 'name']
                        }),
                        
                        editable:false,
                        forceSelection:false,
                        hideOnSelect:false,
                        //The select all option seems to be confusing the control
                        //when data is passed into it for it to make initial 
                        //selections. For now, if we disable 'select all', the
                        //control behaves correctly (BP)
                        //addSelectAllItem:true, 
                        displayField:'name',
                        valueField:'id',
                        hiddenName: spectrumId + '_ionized_species',
                        //lazyRender:true,
                        typeAhead:false,
                        triggerAction:'all',
                        listWidth:230,
                        allowBlank: true,
                        disabled: readOnly,
                        mode: 'local'
                        })]
                    } ,{
                    columnWidth: 0.5,
                    layout: 'form',
                    defaults: {'width': 400},
                    labelWidth: 150,
                    itemId: 'col2',
                    items: [
                        new Ext.ux.MambomsGraphIFrameComponent(
                            {url: 'about:none',
                             itemId: 'graphiframe'
                            }).setParams('400px', '133px', 'mamboms/graph/image/'),
                    {
                        fieldLabel: 'Mass spectra',
                        name: spectrumId + '_mass_spectra',
                        xtype: 'textarea',
                        width: 230,
                        height: 195,
                        listeners: markTabInvalidListeners,
                        allowBlank: false,
                        disabled: readOnly
                    }]
                }
        ],
        setMethod: function(method) {
                        
            Ext.getCmp(idPrefix + spectrumId + 'ionization-mode').setValue(method.ionization_mode);
            Ext.getCmp(idPrefix + spectrumId + 'polarity').setValue(method.polarity);
            var massSpectraTypeCmb = Ext.getCmp(idPrefix + spectrumId + 'mass-spectra-type');
            var precursorTypeCmb = Ext.getCmp(idPrefix + spectrumId + 'precursor-type');
            var precursorSelectionCmb = Ext.getCmp(idPrefix + spectrumId + 'precursor-selection');
            var ionizedSpeciesCmb = Ext.getCmp(idPrefix + spectrumId + 'ionized_species'); 
            massSpectraTypeCmb.store.loadData(Ext.madasComboData.massSpectraTypes);
            precursorSelectionCmb.store.loadData(Ext.madasComboData.precursorSelections);
            ionizedSpeciesCmb.store.loadData(Ext.madasComboData.ionizedSpeciesSelections);
            if (method.polarity == 'Positive') {
                precursorTypeCmb.store.loadData(Ext.madasComboData.precursorTypes.Positive);
                //if (precursorTypeCmb.store.find('name', precursorTypeCmb.value) == -1) {
                //    precursorTypeCmb.clearValue();
                //}
            } else if (method.polarity == 'Negative') {
                precursorTypeCmb.store.loadData(Ext.madasComboData.precursorTypes.Negative);
            }
        },
        addMiniGraph: function(that){
            //must be called after we have obtained out specrtral id value
            var spectrumId = that.getComponent('col1').findByType('hidden')[0].getValue();
            ifr = that.getComponent('col2').getComponent('graphiframe');
            ifr.reload(ifr, spectrumId);
        }
    };
};

Ext.madasLCSpectrumTabPanelCreator = function(idPrefix, readOnly) {

    function addTab() {
            var tabs = Ext.getCmp(idPrefix + 'spectrum-tabpanel');
            var newTab = Ext.madasSpectrumTabCreator(idPrefix, ++tabs.index, readOnly);
           
            var record = null;
            var methodCmb = Ext.getCmp(idPrefix + 'method');
            if (methodCmb.getValue() !== '') {
                record = methodCmb.getStore().getById(methodCmb.getValue());
            }
            var t = tabs.add(newTab);
            t.show();
            if (typeof(tabs.tabrefs) != 'undefined'){
                tabs.tabrefs.push(t);
            }
            if (record !== null) {
                    newTab.setMethod(record.data);
            }
            
        }
    function deleteTab() {
            var tabs = Ext.getCmp(idPrefix + 'spectrum-tabpanel');
            tabs.remove(tabs.activeTab);
            //TODO remove from tabrefs here
        }
    
    var that = {
        xtype: 'panel',
        name: 'spectrum-tabpanel',
        tbar: new Ext.Toolbar({
            items: [
                new Ext.Button({
                    text: 'Add Spectrum',
                    handler: addTab,
                    disabled: readOnly
                }),
                new Ext.Button({
                    text: 'Delete Spectrum',
                    handler: deleteTab,
                    disabled: readOnly
                })
            ] 
        }),
        items: [{
                index: 0,
                xtype:'tabpanel',
                id: idPrefix + 'spectrum-tabpanel',
                plain:true,
                activeTab: 0,
                enableTabScroll:true,
                resizeTabs:true,
                minTabWidth: 115,
                height:300,
                deferredRender: false,
                forceLayout: true,
                defaults:{
                    autoScroll: true,
                    bodyStyle:'padding:10px' 
                },
                createNewTabs: function(count) {
                    this.index = 0;
                    this.removeAll();
                    for (var i = 0; i < count; i++) {
                        addTab();
                    }
                    if (count > 0) { // are there any tabs
                        this.activate(0);
                    }
                },
                setMethod: function(method) {
                    for (var i = 0; i < this.items.length; i++) {
                        this.get(i).setMethod(method);
                    }
                }
        }]
     }; 
    return that;
};

Ext.madasMetaboliteLCFieldCreator = function(idPrefix, readOnly) {
    var that = Ext.madasMetaboliteFieldCreator(idPrefix, readOnly);

    that.additionalFieldDefinitions = function() {
        return [
                {
                    fieldLabel: 'm/z of Expected Derivitization Adducts',
                    id: that.idPrefix + 'metabolite-mzadducts',
                    name: 'mz_adducts',
                    disabled: true
                },{
                    fieldLabel: 'CAS/IUPAC Name',
                    name: 'cas_name',
                    disabled: that.readOnly
                },{
                    fieldLabel: 'm/z',
                    id: idPrefix + 'mol_weight',
                    name: 'mol_weight',
                    xtype: 'numberfield',
                    decimalPrecision: 10,
                    disabled: that.readOnly,        
                    allowBlank: false
                },{
                    fieldLabel: 'Calculated monoisotopic neutral mass',
                    id: that.idPrefix + 'mono_isotopic_mass',
                    name: 'mono_isotopic_mass',
                    decimalPrecision: 4,
                    xtype: 'numberfield',
                    disabled: that.readOnly,        
                    allowBlank: false
                }, new Ext.form.ComboBox({
                    id: that.idPrefix + 'method',
                    fieldLabel: 'Method',
                    name: 'method',
                    editable:false,
                    forceSelection:true,
                    displayField:'name',
                    valueField:'id',
                    hiddenName:'method',
                    lazyRender:true,
                    typeAhead:false,
                    triggerAction:'all',
                    listWidth:230,
                    allowBlank: false,
                    disabled: that.readOnly,        
                    mode: 'local',
                    listeners: {
                        select: function(combo, record, index) {
                            var method = record.data;
                            Ext.getCmp(that.idPrefix + 'metabolite-platform').setValue(method.platform);
                            Ext.getCmp(that.idPrefix + 'metabolite-derivagent').setValue(method.deriv_agent);
                            Ext.getCmp(that.idPrefix + 'metabolite-mzadducts').setValue(method.mz_adducts);
                            Ext.getCmp(that.idPrefix + 'metabolite-massrange').setValue(method.mass_range);
                            Ext.getCmp(that.idPrefix + 'instrument-method').setValue(method.instrument_method);
                            Ext.getCmp(that.idPrefix + 'method-summary').setValue(method.method_summary);
                            Ext.getCmp(that.idPrefix + 'spectrum-tabpanel').setMethod(method);
                        }
                    },
                    store: that.create_store('reference/lc_methods/bynode/', 
                        ['id', 'name', 'platform', 'deriv_agent', 'mz_adducts', 'mass_range', 
                         'instrument_method', 'method_summary', 'polarity', 'ionization_mode'])
                }),
                Ext.madasLCSpectrumTabPanelCreator(idPrefix,readOnly)
        ];
    };
    return that;
};

Ext.madasMetaboliteLCSpec = function() {
    var that = {
        type: 'lc',
        title: 'LCMS MA Metabolite Record',
        fieldCreator: Ext.madasMetaboliteLCFieldCreator,
        url: 'mamboms/lcmetabolite/save/',
        clearInvalidCmps: ['mono_isotopic_mass', 'mol_weight'],
        column1Fields: [
            'id_display', 'id', 'known', 'node', 'instrument', 'method', 'platform', 'deriv_agent',
            'mz_adducts', 'mass_range', 'instrument_method', 'method_summary', 'sample_run_by', 
            'uploaded_by', 'uploaded_date', 'vetted_by', 'structure'
        ],
        column2Fields: [
            'column', 'compound_name', 'synonyms',
            'biological_systems', 'metabolite_class', 'cas_name', 'cas_regno', 'mol_formula', 
            'mono_isotopic_mass', 'mol_weight', 'retention_time', 'retention_index', 'kegg_id', 
            'kegg_link','extract_description', 'vetted', 'can_vet'
        ],  
        southFields: ['spectrum-tabpanel'],
        onActionComplete: function(form, action) {
            var lc, tabs, methodCmb, record, i;
            if (action.type == 'load') {
                lc = action.result.data;
                tabs = Ext.getCmp(this.idPrefix + 'spectrum-tabpanel');
                tabs.tabrefs = [];
                methodCmb = Ext.getCmp(this.idPrefix + 'method');
                tabs.createNewTabs(lc.spectrum_count);
                
                record = methodCmb.getStore().getById(methodCmb.getValue());
                methodCmb.fireEvent('select', methodCmb, record);
                form.setValues(lc);
                for (i=0; i < tabs.tabrefs.length; i++)
                {
                    tabs.tabrefs[i].addMiniGraph(tabs.tabrefs[i]);
                    tabs.tabrefs[i].doLayout(false, true);
                }
            }
        }
    };
    return that;
};

Ext.madasLCMetaboliteUploadCmp = Ext.madasCreateMetaboliteCmp(Ext.madasMetaboliteUploadSpec(Ext.madasMetaboliteLCSpec())).createCmp();
Ext.madasLCMetaboliteEditCmp   = Ext.madasCreateMetaboliteCmp(Ext.madasMetaboliteEditSpec(Ext.madasMetaboliteLCSpec())).createCmp();
Ext.madasLCMetaboliteViewCmp   = Ext.madasCreateMetaboliteCmp(Ext.madasMetaboliteViewSpec(Ext.madasMetaboliteLCSpec())).createCmp();
