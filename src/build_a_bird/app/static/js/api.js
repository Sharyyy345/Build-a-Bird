/*
AJAX Flask app communication code
*/

const API_RECEIPT_ENDPOINT = '/api/receipt';
const API_IMG_ENDPOINT = '/api/img'

/**
 * Sends an HTTP POST request to Flask app's `API_RECEIPT_ENDPOINT` endpoint
 * which is expected to send an email to user via SMTP.
 * 
 * Response Type: JSON
 * 
 * @param {Function} callback 
 * @param {Object} orderData 
 */
function sendEmailReceipt(callback, orderData) {

    var request = new XMLHttpRequest(); // creating new http request object

    request.onreadystatechange = callback; // when request's state is changed, call this function

    request.responseType = 'json'; // indicate we expect json data from the server

    request.open('POST', API_RECEIPT_ENDPOINT); // sets request type and destination attributes

    request.setRequestHeader('Content-Type', 'application/json'); // tells server data enclosed within will be of json type

    request.send(JSON.stringify(orderData));

}

/**
 * Sends an HTTP POST request to Flask app's `API_IMG_ENDPOINT` endpoint
 * which is expected to use a text-to-image model to generate a picture of a bird based on user's order data.
 * 
 * Response Type: JSON
 * 
 * @param {Function} callback 
 * @param {Object} orderData 
 */
function generateBirdImg(callback, orderData) {

    var request = new XMLHttpRequest(); // creating new http request object

    request.onreadystatechange = callback; // when request's state is changed, call this function

    request.responseType = 'json'; // indicate we expect json data from the server

    request.open('POST', API_IMG_ENDPOINT); // sets request type and destination attributes

    request.setRequestHeader('Content-Type', 'application/json'); // tells server data enclosed within will be of json type

    request.send(JSON.stringify(orderData));

}

export { sendEmailReceipt, generateBirdImg };