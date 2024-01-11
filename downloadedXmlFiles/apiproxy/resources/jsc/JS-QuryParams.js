var requestBody = JSON.parse(context.getVariable('request.content'));

const username = requestBody.username;
const password = requestBody.password;
const mobile = requestBody.mobile;
const messageQuery = requestBody.message;
const sendername = requestBody.sendername;

context.setVariable("request.queryparam.username",username)
context.setVariable("request.queryparam.password",password)
context.setVariable("request.queryparam.mobile",mobile)
context.setVariable("request.queryparam.message",messageQuery)
context.setVariable("request.queryparam.sendername",sendername)
context.setVariable("request.verb", "GET");
context.setVariable("request.content", null);



