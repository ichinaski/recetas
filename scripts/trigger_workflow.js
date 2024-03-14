// Script defined on Apps Script, that triggers the Github Workflow to build/deploy the site.
// It is configured to run on every edit on the sheet (every time a new response is added from the form)
function triggerWorkflow() {
  var token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  var url = "https://api.github.com/repos/ichinaski/recetas/dispatches";
  var payload = {
    "event_type": "trigger-workflow"
  };
  var options = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload),
    "headers": {
      "Authorization": "token " + token
    }
  };
  UrlFetchApp.fetch(url, options);  
}
