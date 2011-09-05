Ext.mambomsSearchResultsClickBehaviour = function(grid, rowIndex, evt) {
    var record = grid.store.getAt(rowIndex);
    if (record.get('dataset') === 'NIST') {
        Ext.getCmp('searchDeleteBtn').setDisabled(true);
    } else {
        if (Ext.madasIsAdmin || 
            (Ext.madasIsNodeRep && record.get('node') === Ext.madasUserInfo.node)) {
            Ext.getCmp('searchDeleteBtn').setDisabled(false);
        } else {
            Ext.getCmp('searchDeleteBtn').setDisabled(true);
        }
    }
};

Ext.madasCreateSearchResultsGridCmp = function(params) {
    var i;
    var extraCol;
    var columns = [
        {
            fieldLabel: 'Id',
            hidden: true,
            name: 'id'
        },{
            header: "Compound Name",
            dataIndex: 'compound_name',
            sortable: true,
            width: 35
         },{
            id: 'cas_name_col',
            header: "CAS Name",
            dataIndex: 'cas_name',
            sortable: true
         },{
            header: "Node",
            dataIndex: 'node',
            width: 15
         },{
            header: "Molecular Formula",
            dataIndex: 'mol_formula',
            width: 20,
            sortable: true
        },{
            header: "Molecular Weight",
            dataIndex: 'mol_weight',
            width: 20,
            align: 'right',
            sortable: true
         },{
            header: "CAS Registry Number",
            dataIndex: 'cas_regno',
            width: 20,
            sortable: true
         },{
            header: "Record Type",
            dataIndex: 'dataset',
            width: 15,
            sortable: true
        }
    ];

    function insertElement(arr, pos, elem) {
        var extendedArr = [];
        var i;
        for (i = 0; i < pos; i++) {
            extendedArr[i] = arr[i];
        } 
        extendedArr[extendedArr.length] = elem;
        for (i = pos; i < arr.length; i++) {
            extendedArr[i+1] = arr[i];
        } 
        return extendedArr;
    }

    if (params.extraColumns) {
        for (i = 0; i < params.extraColumns.length; i++) {
            extraCol =  params.extraColumns[i];
            columns = insertElement(columns, extraCol.position, extraCol.column);
        }
    }

    var bbarCmp = null;
    if (params.pagingOn) {
        bbarCmp = new Ext.PagingToolbar({
            pageSize: params.limit,
            store: params.store,
            displayInfo: true,
            displayMsg: 'Displaying results {0} - {1} of {2}',
            emptyMsg: "No results",
            items:['-']
        });
    }


    var selectionModel = new Ext.grid.RowSelectionModel({ singleSelect: true });

   var viewGraphHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            madasShowGraphWindow(selectionModel.getSelected().data.id, 'compound_id');
        }
    };

    var editHandler = function(el, ev) {
        var compound;
        var gcparams;
        var type = '';
        if (selectionModel.hasSelection()) {
            compound = selectionModel.getSelected().data;
            if (compound.dataset == 'MA GC') {
                type = 'gc';
            } else if (compound.dataset == 'MA LC') {
                type = 'lc';
            } else {
                viewGraphHandler(el, ev);
                return;
            }

            params = {
                    id: compound.id, 
                    referrerCmpName: params.componentName,
                    type: type
                };
            if ((Ext.madasIsAdmin || Ext.madasIsNodeRep) &&
                Ext.madasUserInfo.username === compound.record_uploaded_by) {
                    Ext.madasChangeMainContent('metabolite:edit' + type, params);
            } else {
                Ext.madasChangeMainContent('metabolite:view' + type, params);
            }
        }
    };

    var deleteRecord = function(row) {
       Ext.Ajax.request({
            url: 'mamboms/metabolite/delete/',
            params: { id: row.data.id },
            success: function(result, request) {
                if (!selectionModel.selectPrevious()) {
                    selectionModel.selectNext();
                }
                selectionModel.grid.getStore().remove(row);
            },
            failure: function(result, request) {
                Ext.Msg.alert("Failed to delete the selected Metabolite Record");
            }
        });
    };

    var deleteHandler = function(el, ev) {
        var compound;
        if (selectionModel.hasSelection()) {
            Ext.Msg.confirm('Delete Metabolite Record?',
                'Are you sure you want to delete the selected Metabolite Record?',
                function (btn) {
                    if (btn === 'yes') {
                       deleteRecord(selectionModel.getSelected());
                    }
                }
            );
        }
    };

    var topToolbar = new Ext.Toolbar({
            items   : [
                { id: 'searchDeleteBtn', text: "Delete", handler: deleteHandler, disabled: true }
            ]
        });

    var resultsGridCmp = {
        xtype: 'grid',
        id: params.idPrefix + 'results-grid',
        store: params.store,
        trackMouseOver:false,
        disableSelection:true,
        loadMask: true,
        autoExpandColumn: 'cas_name_col',
        forceFit: true,
        sm: selectionModel,
        // grid columns
        columns: columns,
        // customize view config
        viewConfig: {
            forceFit:true,
            enableRowBody:true,
            showPreview:true
        },

        tbar: topToolbar,

        bbar: bbarCmp,

        listeners: {
            rowclick: function(grid, rowIndex, evt) {
                Ext.mambomsSearchResultsClickBehaviour(grid, rowIndex, evt);
            },
            rowdblclick: editHandler
        }

    };

    return {
        id: params.idPrefix + 'results-panel-cmp',
        region: 'center',
        layout: 'fit',
        margins: '5 5 5 5',
        //sel: selectionModel,
        items: [
            resultsGridCmp 
        ]
    };

};

Ext.madasCreateSearchResultsInfoPanel = function (params) {
    function cmpId(id) {
        return params.idPrefix + id;
    }

    return {
        id: cmpId('results-info-panel'),
        height: 70,
        fontsize: '80%',
        region: 'north',
        margins: '5 5 5 5',
        defaults: {
            deferredRender: false,
            forceLayout: true
        },
        deferredRender: false,
        forceLayout: true,
        items: [
            {   
                id: cmpId('results-info-panel-text'),
                html: 'Displaying your search results. Please click the button below to search again.<br/>',
                bodyStyle: 'padding: 5px 15px',
                fontSize: '80%',
                border: false
            },{
                border: false,
                bodyStyle: 'padding: 5px 15px',
                items: [
            {
                xtype: 'button',
                text: params.button.text,
                id: cmpId('search-again'),
                handler: function() {
                        Ext.getCmp('center-panel').layout.setActiveItem(params.button.searchCmpId);
                    }
            }]}
        ]
    };
};

Ext.mambomsCreateSearchResultsHeadToTailPanel = function (params) {
    function cmpId(id) {
        return params.idPrefix + id;
    }

    var theid =  cmpId('results-htt-panel');
    var ifr =  new Ext.ux.MambomsGraphIFrameComponent({
                        url: 'about:none',
                        id: params.idPrefix + 'graphiframe'
                    });
    var clickfn = function(el){
        mambomsShowHeadToTailWindow(ifr.compoundid, ifr.stb); 
    };

    ifr.setParams('100%', '100%', 'mamboms/graph/htt_image/', clickfn);
    return {
        id: theid,
        height: 300,
        fontsize: '80%',
        region: 'south',
        margins: '5 5 5 5',
        defaults: {
            deferredRender: false,
            forceLayout: true
        },
        deferredRender: false,
        forceLayout: true,
        items: [ifr
        ]
    };
};

