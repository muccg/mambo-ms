
Ext.madasUserSearchInit = function(){

	var dataurl = "user/listAllUsers";

    var madasReader = new Ext.data.JsonReader({
        root            : 'response.value.items',
        versionProperty : 'response.value.version',
        totalProperty   : 'response.value.total_count'
        }, [
            { name: 'username', sortType : 'string' },
            { name: 'firstname', sortType : 'string' },
            { name: 'lastname', sortType : 'string' },
            { name: 'email', sortType : 'string' },
            { name: 'telephoneNumber', sortType : 'string' },
            { name: 'physicalDeliveryOfficeName', sortType : 'string' },
            { name: 'title', sortType : 'string' }
        ]);

    var dataStore = new Ext.data.Store({
        id         : 'bSId',
        autoLoad   : true,
        reader     : madasReader,
        sortInfo   : {field: 'username', direction: 'ASC'},
        url        : dataurl
        });
    var gridView = new Ext.grid.GridView({
        loadMask : { msg : 'Please wait...' },
        forceFit: true
        });
    var selectionModel = new Ext.grid.RowSelectionModel({ singleSelect: true });
    var colModel = new Ext.grid.ColumnModel([	
        {header: 'Username', width:185, align : 'left', sortable: true, dataIndex: 'username', sortable: true },
        {header: 'First Name', align : 'left', sortable: true, dataIndex: 'firstname', sortable: true },
        {header: 'Last Name', align : 'left', sortable: true, dataIndex: 'lastname', sortable: true },
        {header: 'Phone', align : 'left', sortable: true, dataIndex: 'telephoneNumber', sortable: true },
        {header: 'Office', align : 'left', sortable: true, dataIndex: 'physicalDeliveryOfficeName', sortable: true },
        {header: 'Title', align : 'left', sortable: true, dataIndex: 'title', sortable: true }
        ]);
    var editHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            Ext.madasChangeMainContent('admin:useredit', [selectionModel.getSelected().data.username]);
        }
    };
    var topToolbar = new Ext.Toolbar({
            items   : [
                { id: 'usersearchEditBtn', text: 'Edit', handler: editHandler, disabled: true }
            ]
        });
    var grid = new Ext.grid.GridPanel({
        id             : 'usersearch-panel',
        ds             : dataStore,
        enableDragDrop : false,
        enableColumnMove: false,
        cm             : colModel,
        sm             : selectionModel,
        loadMask       : { msg : 'Loading...' },
        view           : gridView,
        title          : 'Active User Search',
        tbar           : topToolbar,
        trackMouseOver : false,
        plugins:[new Ext.ux.grid.Search({
            mode:'local',
            iconCls:false,
            dateFormat:'m/d/Y',
            minLength:0,
            width:150,
            position:'top'
        })]
    });
    selectionModel.on('selectionchange', function() { var editBtn = Ext.getCmp('usersearchEditBtn'); if (selectionModel.hasSelection()) { editBtn.enable(); } else { editBtn.disable(); } } );
    grid.on('rowdblclick', editHandler);
    
    //add this component to the center component
    var center = Ext.getCmp('center-panel');
    center.add(grid);

};

// uses components defined in user_edit_cmps.js

Ext.madasAdminUserEditCmp =  Ext.madasCreateUserEditCmp({
    idPrefix: 'admin', 
    formTitle: 'Edit User',
    saveTarget: 'admin:usersearch',
    cancelTarget: 'admin:usersearch'
});
Ext.madasAdminUserEditInit = Ext.madasCreateUserEditInitFunction('admin');


