
/*
 * User editing components used by both the admin user edit form (admin.js)
 * and the My Account form (user.js)
 */

Ext.createPasswordValidator = function (passCmpId, confirmPassCmpId, submitCmpId) {
    return function(textfield, event) {
        var passEl = Ext.getCmp(passCmpId);
        var confirmEl = Ext.getCmp(confirmPassCmpId);
        var submitEl = Ext.getCmp(submitCmpId);

        var passVal = Ext.getDom(passCmpId).value;
        var confirmVal = Ext.getDom(confirmPassCmpId).value;

        if (passVal == confirmVal) {
            confirmEl.clearInvalid();
            submitEl.enable();
            return true;
        } else {
            confirmEl.markInvalid('Password and Confirm Password must match');
            submitEl.disable();
            return false;
        }
    };
};

Ext.madasCreateUserEditCmp = function(params) {
    var cmp = { id: params.idPrefix + 'useredit-container-panel', 
                layout:'absolute', 
                hideMode:'offsets',
                autoScroll: true,
                items:[
                    {  xtype:'form', 
                    labelWidth: 100, // label settings here cascade unless overridden
                    id: params.idPrefix + 'useredit-panel',
                    url: 'user/saveUser',
                    method:'POST',
                    frame:true,
                    reader: Ext.madasJsonReader,
                    title: params.formTitle,
                    bodyStyle:'padding:5px 5px 0',
                    width: 380,
                    x: 50,
                    y: 10,
                    defaults: {width: 230},
                    defaultType: 'textfield',
                    trackResetOnLoad: true,
                    waitMsgTarget: true,
                    
                    items: [
                        {   name: 'originalEmail',
                            inputType: 'hidden'
                        },{
                            fieldLabel: 'Email address',
                            id: params.idPrefix + 'userEditEmailAddress',
                            name: 'email',
                            vtype: 'email',
                            allowBlank:false,
                            maskRe: /[^,-]/
                        },{
                            fieldLabel: 'First name',
                            name: 'firstname',
                            allowBlank:false,
                            maskRe: /[^,=]/
                        },{
                            fieldLabel: 'Last name',
                            name: 'lastname',
                            allowBlank:false,
                            maskRe: /[^,=]/
                        },{
                            fieldLabel: 'Password',
                            name: 'password',
                            id: params.idPrefix + 'userEditPassword',
                            inputType: 'password',
                            allowBlank:true
                        },{
                            fieldLabel: 'Confirm Password',
                            inputType: 'password',
                            id: params.idPrefix + 'userEditConfirmPassword',
                            xtype: 'textfield',
                            allowBlank:true
                        },{
                            fieldLabel: 'Office',
                            name: 'physicalDeliveryOfficeName',
                            allowBlank:true,
                            maskRe: /[^,=]/
                        },{
                            fieldLabel: 'Office Phone',
                            name: 'telephoneNumber',
                            allowBlank:false,
                            maskRe: /[^,=]/
                        },{
                            fieldLabel: 'Home Phone',
                            name: 'homephone',
                            allowBlank:true,
                            maskRe: /[^,=]/
                        },{
                            fieldLabel: 'Position',
                            name: 'title',
                            allowBlank:true,
                            maskRe: /[^,=]/
                        },{
                            xtype:'checkbox',
                            id: params.idPrefix + 'userEditIsAdmin',
                            name: 'isAdmin',
                            inputValue: 'true',
                            fieldLabel: 'Administrator'
                        },{
                            xtype:'checkbox',
                            id: params.idPrefix + 'userEditIsNodeRep',
                            name: 'isNodeRep',
                            inputValue: 'true',
                            fieldLabel: 'Node Rep'
                        }, new Ext.form.ComboBox({
                            fieldLabel: 'Node',
                            id: params.idPrefix + 'userEditNode',
                            name: 'nodeDisplay',
                            editable:false,
                            forceSelection:true,
                            displayField:'name',
                            valueField:'submitValue',
                            hiddenName:'node',
                            lazyRender:true,
                            typeAhead:false,
                            triggerAction:'all',
                            listWidth:230,
                            store: new Ext.data.JsonStore({
                                storeId: 'userEditNodeDS',
                                url: 'user/listAllNodes',
                                root: 'response.value.items',
                                fields: ['name', 'submitValue']
                            })
                        }), new Ext.form.ComboBox({
                            fieldLabel: 'Status',
                            id: params.idPrefix + 'userEditStatus',
                            name: 'statusDisplay',
                            editable:false,
                            forceSelection:true,
                            displayField:'displayLabel',
                            valueField:'submitValue',
                            hiddenName:'status',
                            lazyRender:true,
                            typeAhead:false,
                            mode:'local',
                            triggerAction:'all',
                            listWidth:230,
                            store: new Ext.data.SimpleStore({
                                fields: ['submitValue', 'displayLabel'],
                                data : [['Pending','Pending'],
                                        ['User', 'Active'],
                                        ['Deleted','Deleted'],
                                        ['Rejected','Rejected']]
                            })
                        }),{
                            fieldLabel: 'Department',
                            name: 'dept',
                            allowBlank:true,
                            maskRe: /[^,=]/
                        },{ 
                            fieldLabel: 'Institute',
                            name: 'institute',
                            allowBlank:true,
                            maskRe: /[^,=]/
                        },{
                            fieldLabel: 'Address',
                            name: 'address',
                            allowBlank:true,
                            maskRe: /[^,=]/
                        },{
                            fieldLabel: 'Supervisor',
                            name: 'supervisor',
                            allowBlank:true,
                            maskRe: /[^,=]/
                        },{
                            fieldLabel: 'Area of Interest',
                            name: 'areaOfInterest',
                            allowBlank:true,
                            maskRe: /[^,=]/
                        },new Ext.form.ComboBox({
                            fieldLabel: 'Country',
                            name: 'countryDisplay',
                            editable:false,
                            forceSelection:true,
                            displayField:'displayLabel',
                            valueField:'submitValue',
                            hiddenName:'country',
                            lazyRender:true,
                            typeAhead:false,
                            mode:'local',
                            triggerAction:'all',
                            listWidth:230,
                            store: new Ext.data.SimpleStore({
                                fields: ['submitValue', 'displayLabel'],
                                data : Ext.madasCountries
                            })
                        })
                    ],
                    buttons: [{
                        text: 'Cancel',
                        handler: function(){
                            Ext.getCmp(params.idPrefix + 'useredit-panel').getForm().reset(); 
                            Ext.madasChangeMainContent(params.cancelTarget);
                            }
                        },{
                        text: 'Save',
                        id: params.idPrefix + 'userEditSubmit',
                        handler: function(){
                            Ext.getCmp(params.idPrefix + 'useredit-panel').getForm().submit(
                                {   successProperty: 'success',        
                                    success: function (form, action) {
                                        if (action.result.success === true) {
                                            form.reset(); 
                                            
                                            //display a success alert that auto-closes in 5 seconds
                                            Ext.Msg.alert("User details saved successfully", "(this message will auto-close in 5 seconds)");
                                            setTimeout(function() {Ext.Msg.hide();}, 5000);
                                            
                                            //load up the menu and next content area as declared in response
                                            Ext.madasChangeMainContent(params.saveTarget);
                                        } 
                                    },
                                    failure: function (form, action) {
                                        //do nothing special. this gets called on validation failures and server errors
                                    }
                                });
                            }
                        }
                        ]
                    }
                    ]
              };   

    return cmp;
};

Ext.madasCreateUserEditInitFunction = function (idPrefix) {
    var cmpId = function(id) {
        return idPrefix + id;
    };

    return function(paramArray) {
        params = {};
        var store = null;
        if (paramArray !== undefined) {
            params = {'username': paramArray[0]};
        }
        var userEditCmp = Ext.getCmp(cmpId('useredit-panel'));

        //fetch user details
        userEditCmp.load({url: 'user/loadUser', params: params, waitMsg:'Loading'});

        //attach validator that ext cannot deal with
        var validator = Ext.createPasswordValidator(cmpId('userEditPassword'), cmpId('userEditConfirmPassword'), cmpId('userEditSubmit'));
        Ext.getCmp(cmpId('userEditPassword')).on('blur', validator);
        Ext.getCmp(cmpId('userEditConfirmPassword')).on('blur', validator);
        Ext.getCmp(cmpId('userEditSubmit')).enable();

        Ext.getCmp(cmpId('userEditEmailAddress')).setDisabled(!Ext.madasIsAdmin);
        Ext.getCmp(cmpId('userEditIsAdmin')).setDisabled(!Ext.madasIsAdmin);
        Ext.getCmp(cmpId('userEditIsNodeRep')).setDisabled(!Ext.madasIsAdmin);
        Ext.getCmp(cmpId('userEditStatus')).setDisabled(!Ext.madasIsAdmin);
        Ext.getCmp(cmpId('userEditNode')).setDisabled(!Ext.madasIsAdmin);

        //reload the combobox
        if (Ext.StoreMgr.containsKey('userEditNodeDS')) {
            Ext.StoreMgr.get('userEditNodeDS').reload();
            store = Ext.StoreMgr.get('userEditNodeDS');
        }

        //allow the madas changeMainContent function to handle the rest from here
        return;
    };
};

