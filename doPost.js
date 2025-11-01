function doPost(e) {
    var jsonData = e.postData.contents;
    var data = JSON.parse(jsonData);
  
    var nome = data.nome;
    var idade = data.idade;
    var email = data.email;
  
    var planilha = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    planilha.appendRow([nome, idade, email]);
  
    var result = { message: 'Dados adicionados com sucesso!' };
    return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(ContentService.MimeType.JSON);
  }
