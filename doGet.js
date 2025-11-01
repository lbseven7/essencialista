 function doGet() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var rows = sheet.getDataRange().getValues();
    var headers = rows[0];
    var jsonData = [];
    
    for (var i = 1; i < rows.length; i++) {
      var data = rows[i];
      var row = {};
      
      for (var j = 0; j < headers.length; j++) {
        row[headers[j]] = data[j];
      }
      
      jsonData.push(row);
    }
    
    var jsonString = JSON.stringify(jsonData);
  
    
    return ContentService.createTextOutput(jsonString).setMimeType(ContentService.MimeType.JSON)
    
  }
  
  
  
