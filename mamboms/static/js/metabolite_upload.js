Ext.ux.IFrameComponent = Ext.extend(Ext.BoxComponent, {
     onRender : function(ct, position){
          this.el = ct.createChild({tag: 'image', height: '133px', width: '400px'});

    },
    reload : function(that, spectrumId)
     {
        var url = 'mamboms/graph/image/' + spectrumId + '/';
        that.el.dom.src = url;
        that.el.on({
            'click': {
                    fn: function(el) {
                        madasShowGraphWindow(spectrumId, 'spectrum_id');
                    }, 
                    scope: this
                }
            });
     }
});

Ext.madasMetaboliteLoadCombos = function(form, params, callbackFn) {
    var loadedCombosCount = 0;
    var combos = ["instrument", "method", "column", "sample_run_by", "biological_systems", "metabolite_class", "ionized_species"];
    var onComboFilled = function(r, options, success) {
            loadedCombosCount++;
            if (loadedCombosCount === combos.length) {
                callbackFn(form, params);
           }
        };
    var cmb = null;
    for (var i = 0; i < combos.length; i++) {
        cmb = form.findField(combos[i]);
        if (cmb === null) {
            onComboFilled();
            continue;
        }
        if (params === undefined || params.id === undefined) { 
            cmb.store.load({callback: onComboFilled});
        } else {
            cmb.store.load({params: {id: params.id},callback: onComboFilled});
        }
    }

};

Ext.madasMetaboliteLoadCombosAndForm = function(form, params, successFunc) {
    Ext.madasMetaboliteLoadCombos(form, params, function(form, params) {
                form.referrerCmpName = params.referrerCmpName;
                var loadUrl = 'mamboms/metabolite/' + params.type + '/load/';
                form.load({url: loadUrl, params: {id: params.id}, waitMsg:'Loading',
                    success:  successFunc
                });
    }); 
};

Ext.madasMetaboliteEditInit = function(params) {
    var savedMsg = Ext.getCmp('edit-gcsaved-message');
    if (typeof params.justUploaded !== 'undefined') {
        savedMsg.setHeight(28);
    } else {
        savedMsg.setHeight(0);
    }
    var form = Ext.getCmp('edit-gcmetabolite-panel').getForm(); 
    //Ext.madasMetaboliteLoadCombosAndForm(form, params, Ext.emptyFn);
    Ext.madasMetaboliteLoadCombosAndForm(form, params, 
            function(form, action) {
                var spectrumId = form.getValues(false).spectrumId;
                ifr = Ext.getCmp('edit-gc-graphiframe');
                ifr.reload(ifr, spectrumId);
            }
    );
};

Ext.madasMetaboliteViewInit = function(params) {
    var form = Ext.getCmp('view-gcmetabolite-panel').getForm(); 
    Ext.madasMetaboliteLoadCombosAndForm(form, params,
            function(form, action) {
                var spectrumId = form.getValues(false).spectrumId;
                if (Ext.getCmp('view-gcmetabolite-can-vet').getValue() !== "false") {
                    Ext.getCmp('view-gcmetabolite-vet').enable();
                } else {
                    Ext.getCmp('view-gcmetabolite-vet').disable();
                }
                ifr = Ext.getCmp('edit-gc-graphiframe');
                ifr.reload(ifr, spectrumId);
             }
    );
};

Ext.madasMetaboliteUploadInit = function(params) {
    var form = Ext.getCmp('upload-gcmetabolite-panel').getForm(); 
    form.reset(); 
    Ext.madasMetaboliteLoadCombos(form, params, Ext.emptyFn); 
};

Ext.madasMetaboliteFieldCreator = function(idPrefix, readOnly) {
    var that = {};
    that.readOnly = readOnly;
    that.idPrefix = idPrefix;

    that.create_store = function(url, fields) {
        if (fields === undefined) {
            fields = ['name', 'id'];
        }
        return new Ext.data.JsonStore({
            proxy: new Ext.data.HttpProxy({ url: url, method: 'GET'}),
            root: 'data',
            autoLoad: false,
            fields: fields
        });
    };

    that.commonFieldDefinitions = function () { 
        return [{
            fieldLabel: 'Metabolite ID',
            name: 'id_display',
            disabled: true,
            value: 'To be generated on Save'
        }, {
            xtype: 'hidden',
            id: that.idPrefix + 'id',
            name: 'id',
            value: ''
        }, {
            xtype:'checkbox',
            name: 'known',
            id: that.idPrefix + 'known',
            inputValue: 'true',
            disabled: that.readOnly,        
            fieldLabel: 'Known'
        }, {
            fieldLabel: 'Node',
            name: 'node',
            disabled: true
        }, new Ext.form.ComboBox({
            fieldLabel: 'Instrument',
            name: 'instrument',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'id',
            hiddenName:'instrument',
            lazyRender:true,
            typeAhead:false,
            triggerAction:'all',
            listWidth:230,
            allowBlank: false,
            disabled: that.readOnly,        
            mode: 'local',
            store: that.create_store('reference/instruments/')
        }),{
            fieldLabel: 'Platform Name',
            id: that.idPrefix + 'metabolite-platform',
            name: 'platform',
            disabled: true
        },{
            fieldLabel: 'Derivitization Agent',
            id: that.idPrefix + 'metabolite-derivagent',
            name: 'deriv_agent',
            disabled: true
        },{
            fieldLabel: 'Mass Range Acquired',
            id: that.idPrefix + 'metabolite-massrange',
            name: 'mass_range',
            disabled: true
        },{
            fieldLabel: 'Instrument Method',
            xtype: 'displayfield',
            id: that.idPrefix + 'instrument-method',
            name: 'instrument_method'
        },{
            fieldLabel: 'Method Summary',
            xtype: 'displayfield',
            id: that.idPrefix + 'method-summary',
            name: 'method_summary'
        }, new Ext.form.ComboBox({
            fieldLabel: 'Column',
            name: 'column',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'id',
            hiddenName:'column',
            lazyRender:true,
            typeAhead:false,
            triggerAction:'all',
            listWidth:230,
            allowBlank: false,
            disabled: that.readOnly,        
            mode: 'local',
            store: that.create_store('reference/columns/')
        }), new Ext.form.ComboBox({
            fieldLabel: 'Sample Run By',
            name: 'sample_run_by',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'username',
            hiddenName:'sample_run_by',
            lazyRender:true,
            typeAhead:false,
            triggerAction:'all',
            listWidth:230,
            allowBlank: false,
            disabled: that.readOnly,        
            mode: 'local',
            store: new Ext.data.JsonStore({
                proxy: new Ext.data.HttpProxy({ url: 'user/listNodeUsers', method: 'GET'}),
                root: 'data',
                autoLoad: false,
                fields: ['name', 'username']
            })
        }),{
            fieldLabel: 'Record Uploaded By',
            id: that.idPrefix + 'metabolite-uploaded-by',
            name: 'uploaded_by',
            value: 'To be generated on Save',
            disabled: true
        },{
            fieldLabel: 'Record Uploaded Date',
            id: that.idPrefix + 'metabolite-uploaded-date',
            name: 'uploaded_date',
            value: 'To be generated on Save',
            disabled: true
        },{
            fieldLabel: 'Compound Name',
            name: 'compound_name',
            allowBlank: false,
            disabled: that.readOnly        
        },{
            fieldLabel: 'Synonyms (comma separated)',
            name: 'synonyms',
            disabled: that.readOnly        

        }, new Ext.ux.form.SuperBoxSelect({
            allowBlank: true,
            fieldLabel: 'Biological Systems',
            emptyText: '',
            resizable: true,
            name: 'biological_systems',
            store: that.create_store('reference/biological_systems/'),
            mode: 'local',
            listWidth: 230,
            displayField: 'name',
            displayFieldTpl: '{name}',
            valueField: 'id',
            disabled: that.readOnly,
            forceSelection : true
        }), new Ext.form.ComboBox({
            fieldLabel: 'Metabolite Class',
            name: 'metabolite_class',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'id',
            hiddenName:'metabolite_class',
            lazyRender:true,
            typeAhead:false,
            triggerAction:'all',
            listWidth:230,
            allowBlank: false,
            disabled: that.readOnly,
            mode: 'local',
            store: that.create_store('reference/metabolite_classes/')
        }),{
            fieldLabel: 'CAS Registration Number',
            name: 'cas_regno',
            disabled: that.readOnly,        
            allowBlank: false
        },{
            fieldLabel: 'Molecular Formula',
            name: 'mol_formula',
            disabled: that.readOnly,        
            allowBlank: false
        },{
            fieldLabel: 'Retention Time',
            name: 'retention_time',
            disabled: that.readOnly,        
            allowBlank: false
        },{
            fieldLabel: 'Retention Index',
            name: 'retention_index',
            disabled: that.readOnly
        },{
            fieldLabel: 'KEGG ID',
            name: 'kegg_id',
            disabled: that.readOnly
        },{
            fieldLabel: 'KEGG Link',
            name: 'kegg_link',
            disabled: that.readOnly
        },{
            fieldLabel: 'Extract Description',
            name: 'extract_description',
            xtype: 'textarea',
            disabled: that.readOnly,        
            allowBlank: false
        },{
            fieldLabel: 'Structure',
            id: that.idPrefix + 'structure',
            xtype: 'fileuploadfield',
            name: 'structure',
            emptyText: ''
        },{
            name: 'vetted',
            id: that.idPrefix + 'metabolite-vetted', 
            xtype: 'hidden',
            value: ''
        },{
            name: 'can_vet',
            id: that.idPrefix + 'metabolite-can-vet', 
            xtype: 'hidden',
            value: false
        },{
            fieldLabel:'Record Vetted By',
            id: idPrefix + 'record-vetted-by',
            name: 'vetted_by',
            xtype:'textarea',
            disabled: true
        }
    ];
    };

    that.additionalFieldDefinitions = function() {
        return [];
   };

    that.createFields = function() {
        fields = {};
        fieldDefinitions = that.commonFieldDefinitions().concat(that.additionalFieldDefinitions());
        for (var i = 0; i < fieldDefinitions.length; i++) {
            def = fieldDefinitions[i];
            fields[def.name] = def;
        }
        return fields;
    };
    return that;
};

Ext.madasMetaboliteGCFieldCreator = function(idPrefix, readOnly) {
    var that = Ext.madasMetaboliteFieldCreator(idPrefix, readOnly);
    that.additionalFieldDefinitions = function() {
        return [
        {
            fieldLabel: 'Mass of Expected Derivitization Adducts',
            id: that.idPrefix + 'metabolite-massadducts',
            name: 'mass_adducts',
            disabled: true
        },{
            fieldLabel: 'CAS Name',
            name: 'cas_name',
            disabled: that.readOnly
        },{
            fieldLabel: 'Quant Ion',
            name: 'quant_ion',
            xtype: 'numberfield',
            disabled: that.readOnly
        },{
            fieldLabel: 'Molecular Weight',
            id: idPrefix + 'mol_weight',
            name: 'mol_weight',
            xtype: 'numberfield',
            disabled: that.readOnly,        
            decimalPrecision: 10,
            allowBlank: false
        },{
            fieldLabel: 'Qualifying Ion 1',
            emptyText: 'Enter value with decimals',
            name: 'qual_ion_1',
            xtype: 'numberfield',
            disabled: that.readOnly
        },{
            fieldLabel: 'Qualifying Ion 2',
            emptyText: 'Enter value with decimals',
            name: 'qual_ion_2',
            xtype: 'numberfield',
            disabled: that.readOnly
        },{
            fieldLabel: 'Qualifying Ion 3',
            emptyText: 'Enter value with decimals',
            name: 'qual_ion_3',
            xtype: 'numberfield',
            disabled: that.readOnly
        },{
            fieldLabel: 'Qualifying Ion Ratio (Ion 1:Ion 2)',
            name: 'qual_ion_ratio_1_2',
            value: 'To be generated on Save',
            disabled: true
        },{
            fieldLabel: 'Qualifying Ion Ratio (Ion 2:Ion 3)',
            name: 'qual_ion_ratio_2_3',
            value: 'To be generated on Save',
            disabled: true
        }, new Ext.form.ComboBox({
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
                    Ext.getCmp(that.idPrefix + 'metabolite-massadducts').setValue(method.mass_adducts);
                    Ext.getCmp(that.idPrefix + 'metabolite-massrange').setValue(method.mass_range);
                    Ext.getCmp(that.idPrefix + 'instrument-method').setValue(method.instrument_method);
                    Ext.getCmp(that.idPrefix + 'method-summary').setValue(method.method_summary);
                }
            },
            store: that.create_store('reference/gc_methods/bynode/', 
                ['id', 'name', 'platform', 'deriv_agent', 'mass_adducts', 'mass_range', 'instrument_method', 'method_summary'])
        }),
        {
            xtype: 'panel',
            name: 'spectrum-panel',
            layout: 'column',
            bodyStyle: 'padding-top: 5px;',
            items: [{
                columnWidth: 0.5,
                defaultType: 'textfield',
                defaults: {width: 230},
                layout: 'form',
                items: [{
                        //itemId: 'specid',
                        xtype: 'hidden',
                        name: 'spectrumId'
                    },{
                        fieldLabel: 'Mass spectra',
                        name: 'mass_spectra',
                        xtype: 'textarea',
                        height: 140,
                        disabled: that.readOnly,
                        allowBlank: false
                }]
                },{
                columnWidth: 0.5,
                defaults: {width: 400},
                items: [
                    new Ext.ux.IFrameComponent({
                        url: 'about:none',
                        id: that.idPrefix + '-graphiframe'
                    })
                ]

            }]
        }
     ];
    };
    return that;
};

Ext.madasCreateMetaboliteCmp = function(params) {
    var that = {};
    that.readOnly = false;
    if (params.readOnly !== undefined) {
        that.readOnly = params.readOnly;
    }

    var fields = params.fieldCreator(params.idPrefix, that.readOnly).createFields();
    function setUpColumn(fieldNames) {
        var column = [];
        for (var i = 0; i < fieldNames.length; i++) {
            column.push(fields[fieldNames[i]]);
        }
        return column;
    }

    var formItems = [ {
            id: params.idPrefix + 'saved-message',
            html: 'The Metabolite has been successfully uploaded. You can continue editing it or click Cancel when done.',
            // TODO: should probably style this in CSS file
            style: {
                'color': 'green',
                'font-weight': 'bold',
                'font-size': '1.1em',
                'margin': '0px auto 0px auto'
            },
            width: 600,
            //height: 28
            height: 0
        },{
            layout: 'column',
            items: [{
                    columnWidth: 0.5,
                    defaultType: 'textfield',
                    defaults: {width: 230},
                    layout: 'form',
                    items: setUpColumn(params.column1Fields)
                },{
                    columnWidth: 0.5,
                    defaultType: 'textfield',
                    defaults: {width: 230},
                    layout: 'form',
                    items: setUpColumn(params.column2Fields) 
                }]
        }];
    if (params.southFields !== undefined) {
        for (i = 0; i < params.southFields.length; i++) {
            formItems.push(fields[params.southFields[i]]);
        }
    }

    that.createCmp = function() {
        return {
        
        id: params.idPrefix + 'metabolite-container-panel', 
        layout:'absolute', 
        hideMode: that.readOnly ? 'offsets' : 'display', 
        autoScroll: true,
        items:[ {
            xtype:'form',
            labelWidth: 150, // label settings here cascade unless overridden
            idPrefix: params.idPrefix,
            id: params.idPrefix + 'metabolite-panel',
            url: params.url,
            method:'GET',
            frame:true,
            fileUpload:true,
            reader: Ext.madasJsonReader,
            title: params.formTitle,
            bodyStyle:'padding:5px 5px 0',
            width: 870,
            x: 50,
            y: 10,
            trackResetOnLoad: true,
            waitMsgTarget: true,
            items: formItems,
            listeners: {
                // This workaround is needed to avoid the some of the fields 
                // being marked as invalid
                afterrender: function() {
                    (function() {
                        var cmp;
                        for (var i = 0; i < params.clearInvalidCmps.length; i++) {
                            cmp = Ext.getCmp(params.idPrefix + params.clearInvalidCmps[i]);
                            cmp.clearInvalid();
                        }
                    }).defer(50);
                },
                actioncomplete: (params.onActionComplete !== undefined) ? params.onActionComplete: Ext.emptyFn 
            },
            buttons: [{
                    id: params.idPrefix + 'metabolite-vet',
                    text: 'Vet this Metabolite Record',
                    disabled: true,
                    handler: function(){
                        var id = Ext.getCmp(params.idPrefix + 'id').getValue();
                        Ext.Ajax.request({
                            url: 'mamboms/metabolite/vet/',
                            params: { id: id },
                            method: 'POST',
                            success: function ( result, request ) {
                                var lbl = Ext.getCmp(params.idPrefix + 'record-vetted-by');
                                lbl.setValue(result.responseText);
                                Ext.getCmp(params.idPrefix + 'metabolite-vet').disable();
                            },
                            failure: function ( result, request ) {
                                Ext.MessageBox.alert('Failed', result.responseText);
                            }
                        });
                    }
                },{
                    text: 'Cancel',
                    handler: function(){
                        var form = Ext.getCmp(params.idPrefix + 'metabolite-panel').getForm();
                        //form.reset(); 
                        Ext.madasChangeMainContent(form.referrerCmpName);
                    }
                },{
                    text: 'Save',
                    formBind: true,
                    disabled: that.readOnly,        
                    handler: function(){
                        Ext.getCmp(params.idPrefix + 'metabolite-panel').getForm().submit(
                            {   
                                successProperty: 'success',        
                                success: params.afterSave,
                                failure: function(form, action) {
                                    //do nothing special. this gets called on validation failures and server errors
                                }
                             });
                    }
                }]
            }]
        };
    };
    return that;
};

Ext.madasMetaboliteGCSpec = function() {
    var that = {
        type: 'gc',
        title: 'GCMS MA Metabolite Record',
        fieldCreator: Ext.madasMetaboliteGCFieldCreator,
        url: 'mamboms/metabolite/save/',
        clearInvalidCmps: ['mol_weight'],
        column1Fields: [
            'id_display', 'id', 'known', 'node', 'instrument', 'method', 'platform', 'deriv_agent',
            'mass_adducts', 'mass_range', 'instrument_method', 'method_summary', 'column', 
            'sample_run_by', 'uploaded_by', 'uploaded_date', 'vetted_by', 'biological_systems', 
            'metabolite_class'
        ],
        column2Fields: [
            'compound_name', 'synonyms', 'cas_name', 'cas_regno', 'mol_formula', 'mol_weight',
            'retention_time', 'retention_index', 'kegg_id', 'kegg_link', 'quant_ion',
            'qual_ion_1', 'qual_ion_2', 'qual_ion_3', 'qual_ion_ratio_1_2', 'qual_ion_ratio_2_3',
            'extract_description', 'structure', 'vetted', 'can_vet'
        ],
        southFields: ['spectrum-panel']
    };
    return that;
};

Ext.madasMetaboliteUploadSpec = function(parent) {
        var that = {
            idPrefix: 'upload-' + parent.type,
            formTitle: 'Upload ' + parent.title,
            afterSave: function(form, action) {
                    var paramsArg;
                    paramsArg = { 'id' : action.result.id, 'justUploaded': true, 'type': parent.type };
                    Ext.madasChangeMainContent('metabolite:edit' + parent.type, paramsArg);
            }
        };
        Ext.apply(that, parent);
        return that;
};

Ext.madasMetaboliteEditSpec = function(parent) {
        var that = {
            idPrefix: 'edit-' + parent.type,
            formTitle: 'Edit ' + parent.title,
            afterSave: function(form, action) {
                        Ext.Msg.alert(parent.title + " successfully saved.", "(this message will auto-close in 5 seconds)");
                        setTimeout(function() {Ext.Msg.hide();}, 5000);
                        Ext.madasChangeMainContent(form.referrerCmpName);
                }
        };
        Ext.apply(that, parent);
        return that;
};

Ext.madasMetaboliteViewSpec = function(parent) {
        var that = {
            readOnly: true,
            idPrefix: 'view-' + parent.type,
            formTitle: 'View ' + parent.title
        };
        Ext.apply(that, parent);
        return that;
};

// TODO put these in their own namespace

Ext.madasMetaboliteUploadCmp = Ext.madasCreateMetaboliteCmp(
        Ext.madasMetaboliteUploadSpec(Ext.madasMetaboliteGCSpec())).createCmp();
Ext.madasMetaboliteEditCmp   = Ext.madasCreateMetaboliteCmp(
        Ext.madasMetaboliteEditSpec(Ext.madasMetaboliteGCSpec())).createCmp();
Ext.madasMetaboliteViewCmp   = Ext.madasCreateMetaboliteCmp(
        Ext.madasMetaboliteViewSpec(Ext.madasMetaboliteGCSpec())).createCmp();

