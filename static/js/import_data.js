

var that = {};
    that.readOnly = false;
    that.idPrefix = 'dataimport-panel';
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


Ext.madasGCLoadCombos = function(form, params, callbackFn) {
    var loadedCombosCount = 0;
    var combos = ["instrument", "method", "column", "sample_run_by", "metaboliteclass", "uploaded_by"];
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


Ext.madasDataImportPanel = {

    xtype:'form', 
    labelWidth: 100, // label settings here cascade unless overridden
    id:'dataimport-panel',
    url:'import/',
    method:'POST',
    frame:true,
    title: 'Data Import',
    fileUpload:true,
    bodyStyle:'padding:5px 5px 0',
    width: 370,
    style:'margin-left:30px;margin-top:20px;',
    defaults: {width: 240},
    defaultType: 'textfield',
    items: [
            {xtype: 'fieldset',
             title: 'Data Import',
             id: 'dataimportwarning',
             autoHeight : true,
             autoWidth: true,
             items: [
            
        {
            id: 'warningText',
            html: '<i>Warning: This tool performs no server-side data validation, and importing is unreversible. Use with care.</i>',
            style: {
                'margin' : '0px 0px 5px 0px'
            }
        }]},
         {
            fieldLabel: 'Dataset (NIST, MA GC, MA LC):',
            name: 'dataset',
            disabled: that.readOnly,        
            allowBlank: false
         },
         {
            xtype:'checkbox',
            name: 'known',
            id: 'known',
            inputValue: 'true',
            disabled: false,        
            fieldLabel: 'Known'
         }, 
         new Ext.form.ComboBox({
            fieldLabel: 'Uploading Node',
            name: 'uploading_node',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'name',
            hiddenName:'uploading_node',
            lazyRender:true,
            typeAhead:false,
            triggerAction:'all',
            listWidth:230,
            allowBlank: false,
            disabled: that.readOnly,        
            mode: 'local',
            store: new Ext.data.JsonStore({
                proxy: new Ext.data.HttpProxy({ url: 'user/listAllNodes', method: 'GET'}),
                root: 'response["value"]["items"]',
                autoLoad: true,
                fields: ['name', 'username']
            })
        }),
         new Ext.form.ComboBox({
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
            disabled: false,        
            mode: 'local',
            store: that.create_store('reference/instruments?all=True/')
        }),
         new Ext.form.ComboBox({
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
            disabled: false,        
            mode: 'local',
            store: that.create_store('reference/gc_methods/', ['id', 'name', 'platform', 'deriv_agent', 'mass_adducts', 'mass_range', 'instrument_method', 'method_summary'])
        }),
        new Ext.form.ComboBox({
            fieldLabel: 'Metabolite Class',
            name: 'metaboliteclass',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'id',
            hiddenName:'metaboliteclass',
            lazyRender:true,
            typeAhead:false,
            triggerAction:'all',
            listWidth:230,
            allowBlank: false,
            disabled: false,        
            mode: 'local',
            store: that.create_store('reference/metabolite_classes/')
        }),
        new Ext.form.ComboBox({
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
            store: that.create_store('reference/columns?all=True/')
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
                proxy: new Ext.data.HttpProxy({ url: 'user/listUsers?all=1', method: 'GET'}),
                root: 'data',
                autoLoad: true,
                fields: ['name', 'username']
            })
        }), new Ext.form.ComboBox({
            fieldLabel: 'Record Uploaded By',
            id: that.idPrefix + 'metabolite-uploaded-by',
            name: 'uploaded_by',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'username',
            hiddenName:'uploaded_by',
            lazyRender:true,
            typeAhead:false,
            triggerAction:'all',
            listWidth:230,
            allowBlank: false,
            disabled: that.readOnly,        
            mode: 'local',
            store: new Ext.data.JsonStore({
                proxy: new Ext.data.HttpProxy({ url: 'user/listUsers?all=1', method: 'GET'}),
                root: 'data',
                autoLoad: true,
                fields: ['name', 'username']
            })
        })
        ,{
            fieldLabel: 'Record Uploaded Date',
            id: that.idPrefix + 'metabolite-uploaded-date',
            name: 'uploaded_date',
            value: 'To be generated on Save',
            disabled: true
        },{
            fieldLabel: 'Retention Time',
            name: 'retention_time',
            disabled: that.readOnly,        
            allowBlank: false
        },{
            fieldLabel: 'Extract Description',
            name: 'extract_description',
            xtype: 'textarea',
            disabled: that.readOnly,        
            allowBlank: false
        },
        {
            fieldLabel: 'Data File',
            id: that.idPrefix + 'datafile',
            xtype: 'fileuploadfield',
            name: 'datafile',
            emptyText: ''
        }
        ],
    buttons: [{
            text: 'Import',
            id:'requestImportSubmit',
            handler: function() 
            {
                    var formValues = Ext.getCmp('dataimport-panel').getForm().submit(
                    {   
                        successProperty: 'success',        
                        success: function (form, action) {
                            if (action.result.success === true) 
                            {
                                form.reset(); 
                                //display a success alert that auto-closes in 5 seconds
                                Ext.Msg.alert("Data Import successful: " + action.result.text, "(this message will auto-close in 5 seconds)");
                                setTimeout(function() {Ext.Msg.hide();}, 5000);
                                           
                                //load up the menu and next content area as declared in response
                                //Ext.madasChangeMainContent(params.saveTarget);
                                Ext.madasChangeMainContent("dataimport");
                            } 
                        },
                        failure: function (form, action) 
                        {
                            Ext.Msg.alert("Data Import failed: " + action.result.text, "(this message will auto-close in 5 seconds)");
                            setTimeout(function() {Ext.Msg.hide();}, 5000);
                            //do nothing special. this gets called on validation failures and server errors
                        }
                    }
                    );
            }
         },{
            text: 'Reset',
            handler: function(){
                Ext.getCmp('dataimport-panel').getForm().reset();
            }
        }]
};

Ext.madasDataImportInit = function(params) {
    var form = Ext.getCmp('dataimport-panel').getForm();
    Ext.madasGCLoadCombos(form, params, Ext.emptyFn);
};


Ext.madasDataImportCmp = {   
    id:'dataimport-container-panel', 
    items:[ 
        Ext.madasDataImportPanel 
    ]
};


