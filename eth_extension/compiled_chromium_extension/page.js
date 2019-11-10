//ok alert("HELLO from extension alert");
console.log("Start page.js  (expend End)");


//######################################################################
//####  GIVEN RULES -- apply via javascript on page (css or js)
//####  - ideally apply from external css injection
//######################################################################
function ApplyRules(rules) {
	// Got rules: {"rules_list":["a","b"],"rules_report":"Rules count: 1"}
	  console.log("--> BB : "+JSON.stringify(rules));

	rules_list=rules["rules_list"];
	rules_list.forEach(function(rule) {
		console.log("Apply rule: "+rule);

//ok		document.body.style.backgroundColor = "red"; //yes

		//css_command="<style>" +
		//background-color: lightblue;
		
		//jquery
		// $('.xd_top_box').css('display', 'inline-block');

	});
}

//content.js
//######################################################################
//####  Message listener.  Expect background to pass message. Can send response.
//######################################################################
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
	  // request == {alert:request}
	  // so here:  request.alert is unknown
	  console.log("Hello from web3: "+JSON.stringify(request));
	  ApplyRules(request["action"]);
//ok	  alert("GOT MESSAGE: "+request)
//    if( request.message === "clicked_browser_action" ) {
	  //chrome.runtime.sendMessage
    sendResponse({counter: request.counter+1});
//     port.postMessage({counter: msg.counter+1});
  });


console.log("End page.js");


//
// One work-around, if you want to avoid injecting inline style rules, is the following (I'm using jQuery for the actual insertion, but it could be done with straight Javascript):
// 
// 		$(document).ready(function() {
// 		var path = chrome.extension.getURL('styles/myExtensionRulz.css');
// 		$('head').append($('<link>')
// 		    .attr("rel","stylesheet")
// 		    .attr("type","text/css")
// 		    .attr("href", path));
// 		});

