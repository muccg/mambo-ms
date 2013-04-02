
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
that.create_importable_dropdown = function(displayname, name, nullable, datafields){
    return new Ext.form.ComboBox({
        fieldLabel: displayname,
        id: that.idPrefix + name,
        name: name,
        hiddenName: name,
        lazyRender:true,
        typeAhead: false,
        triggerAction: 'all',
        listWidth: 230,
        allowBlank: nullable,
        disabled: false,
        mode: 'local',
        store: new Ext.data.JsonStore({
            root: 'data',
            data: datafields,
            fields: ['fielddisplay', 'fieldvalue']}),
        displayField: 'fielddisplay',
        valueField: 'fieldvalue',
        editable: true,
        forceSelection: false
    });
};


Ext.madasGCLoadCombos = function(form, params, callbackFn) {
    var loadedCombosCount = 0;
    var combos = ["instrument", "method", "column", "sample_run_by", "metabolite_class", "uploaded_by"];
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

Ext.mambomsDataImportFileImportPanel = {
    xtype: 'form',
    labelWidth: 100,
    id:'dataimport_fileimport-panel',
    url:'import/fileupload',
    method: 'POST',
    frame: true,
    title: 'Data Import Step 1 of 3',
    fileUpload: true,
    bodyStyle: 'padding:5px 5px 0',
    width: 370,
    style:'margin-left:30px;margin-top:20px;',
    defaults: {width: 240},
    defaultType: 'textfield',
    items: [
        
        {xtype: 'fieldset',
             title: 'Upload Data file',
             id: 'datafileuploadset',
             autoHeight : true,
             autoWidth: true,
             items: [
            
        {
            id: 'datafileuploadtext',
            html: 'To begin, upload your data file and set the Dataset. We will define how the data will be imported later.',
            style: {
                'margin' : '0px 0px 5px 0px'
            }
        }]},
        {xtype: 'fieldset',
             title: 'Warning!',
             id: 'datafileuploadwarning',
             autoHeight : true,
             autoWidth: true,
             items: [
            
        {
            id: 'datafileuploadwarningtext',
            html: 'Before using the data importer, you should always <b>backup your database</b> first, in case something goes wrong with the import.',
            style: {
                'margin' : '0px 0px 5px 0px'
            }
        }]},
        new Ext.form.ComboBox({
            fieldLabel: 'Dataset',
            name: 'dataset',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'name',
            hiddenName:'dataset',
            lazyRender:true,
            typeAhead:false,
            triggerAction:'all',
            listWidth:230,
            allowBlank: false,
            disabled: that.readOnly,        
            mode: 'local',
            //store: that.create_store('reference/datasets/', ['name', 'id'])
            
            store: new Ext.data.JsonStore({
                proxy: new Ext.data.HttpProxy({ url: 'reference/datasets/', method: 'GET'}),
                root: 'data',
                autoLoad: true,
                fields: ['id', 'name']
            })
        }),

         
        {
            fieldLabel: 'Data File',
            id: that.idPrefix + 'datafile',
            xtype: 'fileuploadfield',
            name: 'datafile',
            emptyText: ''
        }
    ],
    buttons: [{
            text: 'Upload',
            id:'requestUploadSubmit',
            handler: function() 
            {
                    Ext.MessageBox.wait("Uploading");
                    var formValues = Ext.getCmp('dataimport_fileimport-panel').getForm().submit(
                    {   
                        successProperty: 'success',
                        success: function (form, action) {
                            if (action.result.success === true) 
                            {
                                //console.log(action.result);
                                Ext.MessageBox.hide(); //hide the 'uploading' box
                                //Hide step 1
                                Ext.getCmp('dataimport_fileimport-panel').hide();
                                
                                //Show step 2
                                Ext.mambomsDataImportStep2_Init(action.result.metadata);
                                Ext.getCmp('dataimport-panel').show(); 
                            } 
                        },
                        failure: function (form, action) 
                        {
                            Ext.MessageBox.hide(); //hide the 'uploading' box
                            Ext.Msg.alert("Data Import failed: " + action.result.text, "(this message will auto-close in 5 seconds)");
                            //setTimeout(function() {Ext.Msg.hide();}, 5000);
                            //do nothing special. this gets called on validation failures and server errors
                        }
                    }
                    );
            }
        }]

};


var createFieldMappingForm = function(metadata){
    
    //Based on the metadata, we create some data to use in the form.
    var fieldsdict = {}
    var alwaysfields = "";
    var sometimesfields = "";
    var jsonfields = {data:[]};
    var count = 0;

    //build a dict of the field names and values
    // and
    //build the contents of a json store for the dropdowns.
    //the display will always be the field name, and the example
    count = 0;
    for (var fieldname in metadata.sampledata) {
        var fullfieldname = "[[Field " + fieldname + "]]";
        var sampledata = metadata.sampledata[fieldname];
        if (sampledata === "")
            sampledata = "--BLANK--"
        var datastr = fullfieldname + " (" + sampledata + ")";
        if (count < metadata.min_fields){
            alwaysfields += "<li>" + datastr + "</li>"; 
        }
        else {
            
            sometimesfields += "<li>" + datastr + "</li>"; 
        }
        //add the data to the fields dict
        fieldsdict[fullfieldname] = metadata.sampledata[fieldname];
        //add the data to the jsonfields
        var fieldentry  = {fielddisplay: datastr, fieldvalue: fullfieldname};
        jsonfields.data.push(fieldentry);
        count += 1;
    }


    var fconftext = "Records to import: " + metadata.num_records + "<br>" +
                    "Dataset Type: " + metadata.dataset + "<br>" +
                    "<b>Fields always present: 0-" + (metadata.min_fields-1) + "<br></b>" + 
                    "<div style='margin-left: 20px'>" +
                    alwaysfields + "</div>" +
                    "<b>Fields sometimes present: " + (metadata.min_fields) + "-" + (metadata.max_fields-1) + "<br></b>" +
                    "<div style='margin-left: 20px'>" +
                    "<i>" + sometimesfields + "</i></div>";
    
    count=0;
    var importable_fields = [
          {
            id: 'importableText',
            html: "These fields are importable from the data file.<br> Select the field from the dropdown, or " +
                  "type a value if no other fields apply.",
                  
            style: {
                'margin' : '0px 0px 5px 0px'
            }
          }
    ];
   
    for (var index = 0; index < metadata.importable_fields.length; index++){
        var field = metadata.importable_fields[index];
        importable_fields.push(that.create_importable_dropdown(field.display, 
                                                               field.id, 
                                                               null, 
                                                               jsonfields));
    }
    
    var methodcombo = null;
    //console.log('Dataset type is ' + metadata.dataset);
    if (metadata.dataset == 'MA LC'){
        methodcombo = new Ext.form.ComboBox({
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
            store: that.create_store('reference/lc_methods/', ['id', 'name', 'platform', 'deriv_agent', 'mz_adducts', 'mass_range', 'ionization_mode', 'instrument_method', 'method_summary'])
        })
    }
    else if (metadata.dataset == 'MA GC'){
        methodcombo = new Ext.form.ComboBox({
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
        })
    }

    var fieldmappingform = {

    xtype:'form', 
    labelWidth: 100, // label settings here cascade unless overridden
    id:'dataimport-panel',
    url:'import/definefields',
    method:'POST',
    frame:true,
    title: 'Data Import Step 2 of 3',
    fileUpload:true,
    bodyStyle:'padding:5px 5px 0',
    width: 370,
    style:'margin-left:30px;margin-top:20px;',
    defaults: {width: 240},
    defaultType: 'textfield',
    items: [{
        xtype: 'fieldset',
        title: 'Field Configuration',
        id: 'dataimportwarning',
        autoHeight : true,
        autoWidth: true,
        items: [{
            id: 'warningText',
            html: fconftext,       
            style: {
                'margin' : '0px 0px 5px 0px'
            }
        }]
    },{ 
        xtype: 'fieldset',
        title: 'Importable Fields',
        id: 'dataimportablefields',
        autoHeight: true,
        autoWidth: true,
        items: [ 
            importable_fields 
        ]
    },{ 
        xtype: 'fieldset',
        title: 'Spectrum Data (optional)',
        id: 'dataspectrumfield',
        autoHeight: true,
        autoWidth: true,
        items: [
            new Ext.form.ComboBox({
                fieldLabel: "Points Field",
                name: 'spectrumfield',
                hiddenName: 'spectrumfield',
                lazyRender:true,
                typeAhead: false,
                triggerAction: 'all',
                listWidth: 230,
                allowBlank: true,
                disabled: false,
                mode: 'local',
                store: new Ext.data.JsonStore({
                    root: 'data',
                    data: jsonfields,
                    fields: ['fielddisplay', 'fieldvalue']}),
                    displayField: 'fielddisplay',
                    valueField: 'fieldvalue',
                    editable: true,
                    forceSelection: false
                })
          ]
    },{ 
        xtype: 'fieldset',
        title: 'Unimportable Fields',
        id: 'dataiunmportablefields',
        autoHeight: true,
        autoWidth: true,
        items: [
        // {
        //    fieldLabel: 'Dataset (NIST, MA GC, MA LC):',
        //    name: 'dataset',
        //    disabled: that.readOnly,        
        //    allowBlank: false
        // },
        {
            id: 'unimportableText',
            html: "These fields are not importable from a data file.<br> Use the dropdown menus to select values to " + 
                  "assign to all records.", 
            style: {
                'margin' : '0px 0px 5px 0px'
            }
        },{
            xtype:'checkbox',
            name: 'known',
            id: 'known',
            inputValue: 'true',
            chedked: true,
            disabled: false,        
            fieldLabel: 'Known'
        }, 
        new Ext.ux.form.SuperBoxSelect({
            allowBlank: true,
            fieldLabel: 'Biological Systems',
            emptyText: '',
            resizable: true,
            name: 'biological_systems',
            store: new Ext.data.JsonStore({
                proxy: new Ext.data.HttpProxy({ url: 'reference/biological_systems', method: 'GET'}),
                root: 'data',
                autoLoad: true,
                fields: ['name', 'id']
            }),
            mode: 'local',
            listWidth: 230,
            displayField: 'name',
            displayFieldTpl: '{name}',
            valueField: 'id',
            disabled: that.readOnly,
            forceSelection : true
        }), 
        new Ext.form.ComboBox({
            fieldLabel: 'Uploading Node',
            name: 'node',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'id',
            hiddenName:'node',
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
                fields: ['name', 'id']
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
        methodcombo,
        new Ext.form.ComboBox({
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
        }), 
        new Ext.form.ComboBox({
            fieldLabel: 'Sample Run By',
            name: 'sample_run_by',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'id',
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
                fields: ['username', 'name', 'id']
            })
        }), 
        new Ext.form.ComboBox({
            fieldLabel: 'Record Uploaded By',
            //id: that.idPrefix + 'metabolite-uploaded-by',
            name: 'record_uploaded_by',
            editable:false,
            forceSelection:true,
            displayField:'name',
            valueField:'id',
            hiddenName:'record_uploaded_by',
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
                fields: ['username', 'name', 'id']
            })
        }),{
            fieldLabel: 'Record Uploaded Date',
            id: that.idPrefix + 'metabolite-uploaded-date',
            name: 'uploaded_date',
            value: 'To be generated on Save',
            disabled: true
        }]
        }],
        buttons: [
            {
                text: 'Back to Step 1',
                id:'requestImportBack',
                handler: function() 
                {
                    //Hide Step 2
                    Ext.getCmp('dataimport-panel').hide(); 
                    //Show step 1
                    Ext.getCmp('dataimport_fileimport-panel').show();

                }
            },
            {
            text: 'Test Import',
            id:'requestImportSubmit',
            handler: function() 
            {
                    Ext.MessageBox.wait("Importing");
                    
                    var displayresults = function(form, action){
                        //Hide Step 2
                        Ext.getCmp('dataimport-panel').hide(); 

                        //Show Step 3
                        Ext.mambomsDataImportStep3_Init(action.result);
                        Ext.getCmp('dataimportconfirm-panel').show(); 
                        Ext.madasChangeMainContent("dataimport");
    
                    }
                    
                    var formValues = Ext.getCmp('dataimport-panel').getForm().submit(
                    {   
                        successProperty: 'success',        
                        success: function (form, action) {
                            Ext.MessageBox.hide();
                            displayresults(form, action);
                        },
                        failure: function (form, action) 
                        {
                            Ext.MessageBox.hide();
                            Ext.Msg.alert("Data Import failed: " + action.result.text, "(this message will auto-close in 5 seconds)");
                            setTimeout(function() {Ext.Msg.hide();}, 5000);
                            displayresults(form, action);
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
    return fieldmappingform;
};    


var createImportConfirmForm = function(import_results, isFinalStep) {
    
    var importinfotext = "<b>Import Dataset: </b>" + import_results["dataset"] + "</br>";
    importinfotext += "<b>Records imported: </b>" + import_results["passed"] + "</br>";
    var failedrecs = 0;
    for (var key in import_results["failed"]){
        if (import_results["failed"].hasOwnProperty(key)) failedrecs++;
    }
    importinfotext += "<b>Failed Imports: </b>" + failedrecs + "</br>";
    if (failedrecs){
        if (isFinalStep){
            importinfotext += "<b>WARNING</b></br>" 
            importinfotext += "There were failed record imports when committing records.</br>" 
            importinfotext += "This indicates a partial record import.</br>" 
            importinfotext += "Since only some records were imported, you may need to restore a database backup to restore database integrity.</br></br>" 
        }
        importinfotext += "<b>Failure Info:</b></br>";
        for (var recordnum in import_results["failed"]){
            importinfotext += "[" + recordnum + "] : " + import_results["failed"][recordnum] + "</br>";
        }
    }

    var panelid = "";
    var paneltitle = "";
    var resultstitle = "";
    var formbuttons = []

    if (isFinalStep){
        panelid = "dataimportfinish-panel";
        paneltitle = "Data Import Finished!";
        resultstitle = "Import Results";
        formbuttons = [{
                    text: "Finished",
                    id: "importfinishedbutton",
                    handler: function()
                    {
                        Ext.getCmp(panelid).hide();
                        //Show step 1
                        Ext.getCmp('dataimport_fileimport-panel').show();

                        Ext.madasChangeMainContent("home");
                    }
                   } ];
    }
    else{
        panelid = "dataimportconfirm-panel";
        paneltitle = "Data Import Step 3 of 3";
        resultstitle = "Pre-Import Results";
        formbuttons = [{
                        text: 'Back to Step 2',
                        id:'requestImportConfirmBack',
                        handler: function() 
                        {
                            //Hide Step 3
                            Ext.getCmp(panelid).hide(); 
                            //Show Step 2
                            Ext.getCmp('dataimport-panel').show(); 
                        }
                    },
                    {
                        text: 'Perform Import',
                        id:'requestImportConfirmSubmit',
                        handler: function() 
                        {
                                Ext.MessageBox.wait("Importing");
                                var displayresults = function(form, action){
                                    //Hide Step 3
                                    Ext.getCmp(panelid).hide(); 
                                    //Show finished
                                    Ext.mambomsDataImportFinished_Init(action.result);
                                    Ext.getCmp('dataimportfinish-panel').show();
                                    form.reset(); 
                                    Ext.madasChangeMainContent("dataimport");
    
                                }
                                
                                var formValues = Ext.getCmp(panelid).getForm().submit(
                                {   
                                    successProperty: 'success',        
                                    success: function (form, action) {
                                        Ext.MessageBox.hide();
                                        displayresults(form, action);   
                                    },
                                    failure: function (form, action) 
                                    {
                                        Ext.MessageBox.hide();
                                        Ext.Msg.alert("Data Import failed: " + action.result.text, "(this message will auto-close in 5 seconds)");
                                        setTimeout(function() {Ext.Msg.hide();}, 5000);
                                        displayresults(form, action); 
                                    }
                                }
                                );
                         }
                    }];
    }


    var importconfirmform = {

    xtype:'form', 
    labelWidth: 100, // label settings here cascade unless overridden
    id: panelid,
    url:'import/confirmimport',
    method:'POST',
    frame:true,
    title: paneltitle, 
    fileUpload:false,
    bodyStyle:'padding:5px 5px 0',
    width: 370,
    style:'margin-left:30px;margin-top:20px;',
    defaults: {width: 240},
    defaultType: 'textfield',
    items: [{
            xtype: 'fieldset',
            title: resultstitle, 
            id: 'dataimportinfo',
            autoHeight : true,
            autoWidth: true,
            items: [{
                id: 'importinfoText',
                html: importinfotext, 
                style: {
                    'margin' : '0px 0px 5px 0px'
                }
            }]
    }],
    buttons: formbuttons

    };

    if (!isFinalStep){
        var warning = {
            xtype: 'fieldset',
             title: "WARNING!", 
             id: 'dataimportwarninginfo',
             autoHeight : true,
             autoWidth: true,
             items: [ {
                id: 'importinfoWaringText',
                html: 'Please make sure you have backed up your database before pressing the \'Import\' button. This is the point of no return.', 
                      
                style: {
                    'margin' : '0px 0px 5px 0px'
                }
            }]};    
        importconfirmform.items.push(warning);
    }


    return importconfirmform;

};

/*
Ext.mambomsDataImportInit = function(params) {
    var form = Ext.getCmp('dataimport-panel').getForm();

    Ext.madasGCLoadCombos(form, params, Ext.emptyFn);
    //form.style.visibility = "hidden";
    //form.hide();
    Ext.getCmp('dataimport-panel').hide();
};
*/
Ext.mambomsDataImportStep2_Init = function(field_metadata) {

    var parentpanel = Ext.getCmp('dataimport-container-panel');
    parentpanel.add(createFieldMappingForm(field_metadata));
    var formcmp = Ext.getCmp('dataimport-panel');
    Ext.madasGCLoadCombos(formcmp.getForm(), undefined, Ext.emptyFn);
    parentpanel.doLayout();
    formcmp.hide();
};

Ext.mambomsDataImportStep3_Init = function(import_results) {

    var parentpanel = Ext.getCmp('dataimport-container-panel');
    parentpanel.add(createImportConfirmForm(import_results, false));
    var formcmp = Ext.getCmp('dataimportconfirm-panel');
    parentpanel.doLayout();
    formcmp.hide();
};

Ext.mambomsDataImportFinished_Init = function(import_results) {
    var parentpanel = Ext.getCmp('dataimport-container-panel');
    parentpanel.add(createImportConfirmForm(import_results, true));
    var formcmp = Ext.getCmp('dataimportfinish-panel');
    parentpanel.doLayout();
    formcmp.hide();
    
};




Ext.mambomsDataImportCmp = {   
    id:'dataimport-container-panel',
    autoScroll: true,
    items:[ 
        Ext.mambomsDataImportFileImportPanel
        //Ext.mambomsDataImportPanel 

    ]
};


