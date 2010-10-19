
Ext.madasChangeMainContent = function(contentName, paramArray){
    if (contentName === undefined) {
        contentName = "home";
    }

    switch (contentName) {
       case "login":
            window.location.href = 'login/';
            break;
            
       case "admin:refdata":
            window.location.href = 'msadmin/';
            break;
             
       case "admin:usersearch":
            Ext.madasUserSearchInit();
            Ext.getCmp('center-panel').layout.setActiveItem('usersearch-panel');
            break;
            
        case "admin:useredit":
            Ext.madasAdminUserEditInit(paramArray);
            Ext.getCmp('center-panel').layout.setActiveItem('adminuseredit-container-panel');
            break;
            
        case "user:myaccount":
            Ext.madasUserEditInit(paramArray);
            Ext.getCmp('center-panel').layout.setActiveItem('useredit-container-panel');
            break;
            
        case "notauthorized":
            Ext.getCmp('center-panel').layout.setActiveItem('notauthorized-panel');
            break;
            
        case "message":
            affectMenu = false;
            Ext.madasMessage(paramArray);
            break;

        case "home": 
        case "search:bykeyword":
        	Ext.madasSearchByKeywordPanelInit();
        	Ext.getCmp('center-panel').layout.setActiveItem('searchbykeyword-container-panel');
        	break;
  
        case "search:byspectra":
        	Ext.getCmp('center-panel').layout.setActiveItem('searchbyspectra-container-panel');
        	break;

        case "search:bykeywordresults":
        	Ext.getCmp('center-panel').layout.setActiveItem('searchbykeyword-results-panel');
        	break;
  
        case "search:byspectraresults":
        	Ext.getCmp('center-panel').layout.setActiveItem('searchbyspectra-results-panel');
        	break;

        case "metabolite:uploadgc":
        	Ext.madasMetaboliteUploadInit();
        	Ext.getCmp('center-panel').layout.setActiveItem('upload-gcmetabolite-container-panel');
        	break;

        case "metabolite:uploadlc":
            Ext.madasLCMetaboliteUploadInit();
            Ext.getCmp('center-panel').layout.setActiveItem('upload-lcmetabolite-container-panel');
            Ext.madasLCMetaboliteUploadPostActivate();
        	break;

        case "metabolite:editgc":
        	Ext.madasMetaboliteEditInit(paramArray);
        	Ext.getCmp('center-panel').layout.setActiveItem('edit-gcmetabolite-container-panel');
        	break;

        case "metabolite:editlc":
        	Ext.madasLCMetaboliteEditInit(paramArray);
        	Ext.getCmp('center-panel').layout.setActiveItem('edit-lcmetabolite-container-panel');
        	break;

        case "metabolite:viewgc":
        	Ext.madasMetaboliteViewInit(paramArray);
        	Ext.getCmp('center-panel').layout.setActiveItem('view-gcmetabolite-container-panel');
        	break;

        case "metabolite:viewlc":
        	Ext.madasLCMetaboliteViewInit(paramArray);
        	Ext.getCmp('center-panel').layout.setActiveItem('view-lcmetabolite-container-panel');
        	break;

        case "dataimport":
            Ext.madasDataImportInit()
            Ext.getCmp('center-panel').layout.setActiveItem('dataimport-container-panel');
            break;
     }
    
};

/**
 * madasInitApplication
 * initializes the main application interface and any required variables
 */
Ext.madasInitApplication = function(appSecureUrl) {
   Ext.BLANK_IMAGE_URL = 'static/js/ext/resources/images/default/s.gif';
   Ext.QuickTips.init();
   // turn on validation errors beside the field globally
   Ext.form.Field.prototype.msgTarget = 'side';

   //the ViewPort defines the main layout for the entire Madas app
   //the center-panel component is the main area where content is switched in and out
   
   var viewport = new Ext.Viewport({
        layout:'border',

        items:[
            new Ext.BoxComponent({
                region:'north',
                el: 'north',
                height:54
            }),
            {
                region:'south',
                contentEl: 'south',
                height:20
            },
            {
                region:'center',
                id:'center-panel',
                layout: 'card',
                activeItem:0,
                items: [Ext.madasSearchByKeywordCmp, Ext.madasSearchByKeywordResultsCmp, Ext.madasSearchBySpectraCmp, 
                        Ext.madasSearchBySpectraResultsCmp, Ext.madasNotAuthorizedCmp, Ext.madasAdminUserEditCmp, Ext.madasUserEditCmp, 
                        Ext.madasMetaboliteUploadCmp, Ext.madasMetaboliteEditCmp, Ext.madasMetaboliteViewCmp, Ext.madasLCMetaboliteUploadCmp, 
                        Ext.madasLCMetaboliteEditCmp, Ext.madasLCMetaboliteViewCmp, Ext.madasDataImportCmp]
            }
        ]
    });

    Ext.madasMenuRender();
    
    Ext.madasGetUserInfo(function() {
        Ext.madasChangeMainContent('home');
    });

};

Ext.madasMessage = function(paramArray) {
    Ext.Msg.alert("", paramArray.message);
};

