               
Ext.madasNotAuthorizedCmp = { id: 'notauthorized-panel', title: 'Not Authorized', html: 'You are not authorized to access this page' };

Ext.madasOnAuthCallbacks = [];

/**
 * call after used logged in to update user groups/menus etc.
 */
Ext.madasGetUserInfo = function(callback) {
   
    Ext.Ajax.request({
        url: 'user/getUserInfo',
        
        success: function(result, request) {
            var resultData = Ext.util.JSON.decode(result.responseText);
            //Ext.getCmp('userMenu').setText('User: ' + resultData.username);
            Ext.madasUserInfo = {username: resultData.username, fullName: resultData.fullname, node: resultData.node, nodeId: resultData.nodeId};
            Ext.madasIsAdmin = resultData.isAdmin;
            Ext.madasIsNodeRep = resultData.isNodeRep;
            Ext.madasIsClient = resultData.isClient;                
            callback();
            for (i = 0; i < Ext.madasOnAuthCallbacks.length; i++) {
                Ext.madasOnAuthCallbacks[i]();
            }
        },
        failure: function(result, request) {
            Ext.MessageBox.alert('Communication to the server failed.', result.responseText);
        }
    });
   
};
