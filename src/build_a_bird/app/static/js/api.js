/*
AJAX Flask app communication code
*/

const API_RECEIPT_ENDPOINT = '/api/receipt';
const API_IMG_ENDPOINT = '/api/img'

/**
 * Sends an HTTP request to Flask app's `API_RECEIPT_ENDPOINT` endpoint
 * which is expected to send an email to user via SMTP.
 * 
 * Response Type: JSON
 * 
 * @param {Function} callback 
 * @param {Object} orderData 
 */
function sendEmailReceipt(callback, orderData) {

}

/**
 * Sends an HTTP request to Flask app's `API_IMG_ENDPOINT` endpoint
 * which is expected to use a text-to-image model to generate a picture of a bird based on user's order data.
 * 
 * Response Type: image
 * 
 * @param {Function} callback 
 * @param {Object} orderData 
 */
function generateBirdImg(callback, orderData) {

}

export { sendEmailReceipt, generateBirdImg };