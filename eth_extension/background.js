import Web3 from 'Web3';

// console.log("Got Web3: "+Web3);


// <> compile
// C:\scripts-19\truthpipes\extension\skeleton1\hello_web3
// yarn build

// <> debug
// > use extension -- view background.js info


// OPTION 1:  infrua
// var provider = new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/5a2597b2866f40d3b704b8ab2cc234b8');
// var web3 = new Web3(provider);

// OPTION 2:  Meta mask
const PortStream = require('extension-port-stream');
const MetamaskInpageProvider = require('metamask-inpage-provider');

const METAMASK_EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn';
const metamaskPort = chrome.runtime.connect(METAMASK_EXTENSION_ID);
console.log("metamaskPort: "+metamaskPort);

const pluginStream = new PortStream(metamaskPort);
const web3Provider = new MetamaskInpageProvider(pluginStream);
const web3 = new Web3(web3Provider);

console.log("Yes got provider: "+web3);

const abi=[ { "constant": false, "inputs": [ { "name": "_type", "type": "string" }, { "name": "_datum", "type": "string" } ], "name": "addRecord", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [], "name": "getContractID", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [], "name": "getURL", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_contractID", "type": "string" } ], "name": "setContract", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_url", "type": "string" } ], "name": "setUrl", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": true, "inputs": [], "name": "contractID", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "meta", "outputs": [ { "name": "_id", "type": "uint256" }, { "name": "_type", "type": "string" }, { "name": "_datum", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "recordCount", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "url", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" } ];


chrome.browserAction.onClicked.addListener(async (tab) => {
	  const [address] = await web3.eth.getAccounts();
	  console.log("Address: "+address);


	});

// await torus.logout()


//##################################################################
//#  LOGIC  (dev)
//##################################################################
//#



//#  (A)    QUERY 3rd party API
//#########################################################################################

//#https://github.com/gkunthara/cryptostrikers-chrome-app/blob/master/public/background.js

let assets = []

function pingAPI(){
	dev_endpoint="http://www.truthpipes.com:5000/get_rules"; // Can be local too
    fetch(dev_endpoint)
    .then((resp) => resp.json()) // Transform the data into json
    .then(function(data) {
    	    console.log("GOT RESPONSE: "+JSON.stringify(data));

        assets = data.asset_events

        chrome.storage.local.get(['key'], function(result) {
            // console.log('storage currently has ' + result.key); // ie/ undefined
        });
        })
}

pingAPI();





//#  (B)    QUERY web3 contract

// SAMPLE
//#REF# same good tutorial as py:  https://www.dappuniversity.com/articles/web3-js-intro
// https://github.com/dappuniversity/web3_examples/tree/master/examples
//  (read, send transaction, deploy, write, event, inspect, extras
// web3.eth.getBalance(address, (err, wei) => { balance = web3.utils.fromWei(wei, 'ether') })
// contract.methods.totalSupply().call((err, result) => { console.log(result) })
// contract.methods.name().call((err, result) => { console.log(result) })
// contract.methods.symbol().call((err, result) => { console.log(result) })
// contract.methods.balanceOf('0xd26114cd6EE289AccF82350c8d8487fedB8A0C07').call((err, result) => { console.log(result) })
//	var web3_eth_getaccounts=web3.eth.getAccounts



function getURL(){
       	const address = "0x8c17eab5d444e80da64823c455ea608f6588c591"; //ResilientEndpoint mainnet
	    const contract = new web3.eth.Contract(abi, address)
        var promise1= contract.methods.url().call((err, result) => { return console.log("web3 response for URL: "+result); })
        return promise1
}

//getURL();

// re:  javascript async promis
// - chaining:  https://javascript.info/promise-chaining
// - call and wait for a few:  https://stackoverflow.com/questions/41900886/join-all-async-calls-to-return-some-result
// - call many wait for all, return  https://stackoverflow.com/questions/41900886/join-all-async-calls-to-return-some-result

// Promise all
// var promise1 = Promise.resolve(3);
// var promise2 = 42;
// var promise3 = new Promise(function(resolve, reject) {
//   setTimeout(resolve, 100, 'foo');
// });
// 
// Promise.all([promise1, promise2, promise3]).then(function(values) {
//   console.log(values);
// });



//# COMBO:  Use web3 response to query api endpoint
//######################

//# eth string buffered with 000 assume 4 digit port
//######################
function eth_string_patch(url_endpoint0000) {
	// 
	var url_endpoint=url_endpoint0000.replace(/000+$/,"000");
	console.log("NOW: "+url_endpoint);
	return url_endpoint
}

function getRules(url_endpoint){
	console.log("AT get rules...");
	
	url_endpoint=eth_string_patch(url_endpoint);
	console.log("With: "+url_endpoint);

	var fetch_promise=fetch('http://'+url_endpoint+'/get_rules');
	
	return fetch_promise
    .then((resp) => resp.json()) // Transform the data into json
    .then(function(data) {
    	    console.log("GOT RESPONSE using web3 sourced endpoint: "+JSON.stringify(data));
    	    return data
        })
    ;
    
}

var rules_promise=getURL().then(url_endpoint => getRules(url_endpoint)) ;

function failureCallback(error) {
	  console.error("Error j: " + error);
	}



function call_truthpipes() {
	
    rules_promise
      .then(function(rules) { 
    	      console.log("Got rules: "+JSON.stringify(rules));
    	      return rules
    	  })
      .then(function(rules) { 
    	      console.log("Background sending rules message to page/content.js")
    	      sendM(rules);
    	      return rules
    	  })
      ;
};


//     .catch(failureCallback)

//#  (C)  Rule to browser content
//#########################################################################################
// option to send to different tabs?
// REF:  https://stackoverflow.com/questions/14245334/chrome-extension-sendmessage-from-background-to-content-script-doesnt-work

var GLOBAL_SENT=false;

function applyCSSrules(rules) {
//ok            var css2 ="div[data-asin='B07BHNHP9F'] { background-color: yellow; }";
//ok            var insertingCSS2 = chrome.tabs.insertCSS({code: css2});
        var css2 ="";
        var insertingCSS2="";


        var rules_list=rules["rules_list"];
        rules_list.forEach(function(rule) {
//        	    console.log("RULE: "+rule);
        	    	if (typeof rule ==="object") {
            	    if ('highlight_amazon' in rule) {
                    rule['highlight_amazon'].forEach(function(asin) {
                        css2 ="div[data-asin='"+asin+"'] { background-color: red; }";
                        insertingCSS2 = chrome.tabs.insertCSS({code: css2});
                    });
                };
        	    	};
        	});
}

function sendM(message_dict) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
    	console.log("background1 send message: object "+message_dict);

//        chrome.tabs.sendMessage(tabs[0].id, {action: "open_dialog_box"}, function(response) {});  
    	
    	    var tab_zero=tabs[0];
    	    if ((typeof tab_zero !== "undefined") && !(GLOBAL_SENT)) {
    	    	    console.log("Sending message to tab id: "+tab_zero.id);
    	    	    

            chrome.tabs.sendMessage(tab_zero.id, {action: message_dict}, 
            		function(response) {
       	    	        if(chrome.runtime.lastError) {
       	    	        	    console.log("message NOT sent likely no listener loaded");
       	    	        }
       	    	        else {
       	    	        	    console.log("message sent");
       	    	        	    GLOBAL_SENT=true;
       	    	        }
            	
                }
            );  
            
//ok            var css = "body { border: 20px dotted pink; }";
//ok            var insertingCSS = chrome.tabs.insertCSS({code: css});

            applyCSSrules(message_dict);

            // insertingCSS.then(null, onError);
              
    	    }
    	    else {
    	    	    console.log("Waiting for tab...not yet found.");
    	    }
    	console.log("background2 send message");
    });
}

// https://thoughtbot.com/blog/how-to-make-a-chrome-extension

//ok  const interval = setInterval(function() { sendM() }, 5000);

call_truthpipes()

const interval = setInterval(function() { call_truthpipes() }, 5000);


console.log("Got to end");










//#  MISC
//##################################################################
// https://developer.chrome.com/extensions/background_pages
//a)  initialize onInstalled


















