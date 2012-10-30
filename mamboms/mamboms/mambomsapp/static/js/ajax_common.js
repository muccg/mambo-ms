
// Declaring Ajax stuff that applies to all Ajax requests.

// Needed to avoid timeout on search by spectra
Ext.Ajax.timeout = 90000;

Ext.Ajax.disableCaching = false;

// Handling Unauthorized and Forbidden HTTP Responses
Ext.Ajax.on('requestexception', function(conn, response, options) {
    // Unauthorized
    if (response.status == 401) {
        Ext.madasChangeMainContent('login');
    } 
    // Forbidden
    if (response.status == 403) {
        Ext.madasChangeMainContent('notauthorized');
    } else {
        Ext.Msg.alert('Server Error', 'An unknown error occured while communicating with the server.');
    } 

}, this);

