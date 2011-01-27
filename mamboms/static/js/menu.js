Ext.madasMenuShowHideItems = function() {
    
     Ext.getCmp('search:byspectra').show(); //available to all
     Ext.getCmp('dataimport').hide();
    
    if (Ext.madasIsAdmin) {
        Ext.get('admin').show();
        Ext.getCmp('admin:usersearch').show();
        Ext.getCmp('metabolite:upload').show();
        Ext.getCmp('search:byspectra').show();
    } else if (Ext.madasIsNodeRep) {
        Ext.get('admin').show();
        Ext.getCmp('admin:usersearch').hide();
        Ext.getCmp('metabolite:upload').show();
    } else {
        Ext.get('admin').hide();
        Ext.getCmp('metabolite:upload').hide();
    }
    
    if (Ext.madasIsClient) {
        Ext.getCmp('metabolite:upload').hide();
    }

    //show data import for CCG users
    if ( /.*\@ccg.murdoch.edu.au/.test(Ext.madasUserInfo.username))
    {
        Ext.getCmp('dataimport').show();
    }
    

    
};


Ext.madasMenuRender = function() {
    Ext.madasOnAuthCallbacks.push(function() {
            Ext.getCmp('userMenu').setText('User: ' + Ext.madasUserInfo.username);
        });
    Ext.madasOnAuthCallbacks.push(Ext.madasMenuShowHideItems);


    var tb = new Ext.Toolbar(
        {
            id: 'toolbar-cmp',
            items: [
                {
                    xtype: 'tbbutton', text:'Search', id:'search', menu:{
                        items: [
                            {text:'Search by Keyword', id:'search:bykeyword', handler: Ext.madasMenuHandler},
                            {text:'Search by Spectra', id:'search:byspectra', handler: Ext.madasMenuHandler}
                        ]
                    }
                },{
                    xtype: 'tbbutton', text:'Admin', id:'admin', menu:{
                    items: [
                          {text:'MAMBO MS Users', id:'admin:usersearch', handler: Ext.madasMenuHandler},
                          {text:'Reference Data', id:'admin:refdata', handler: Ext.madasMenuHandler}
                    ]}
                 }, {
                    xtype: 'tbbutton', text:'Upload', id:'metabolite:upload', menu:{
                    items: [
                          {text:'GCMS MA Metabolite Record', id:'metabolite:uploadgc', handler: Ext.madasMenuHandler},
                          {text:'LCMS MA Metabolite Record', id:'metabolite:uploadlc', handler: Ext.madasMenuHandler},
                          {text:'File Import', id:'dataimport', handler: Ext.madasMenuHandler}
                    ]}
                 },

               
               { xtype: 'tbfill'},
                { xtype: 'tbbutton', text: 'User: (unknown)', id: 'userMenu', menu:{
                    items: [
                        {text:'My Account', id:'user:myaccount', handler: Ext.madasMenuHandler}
                    ]
                    }
                }
            ]
        }
    );
    tb.render('toolbar');

};

Ext.madasMenuHandler = function(item) {
    Ext.madasChangeMainContent(item.id);

};

