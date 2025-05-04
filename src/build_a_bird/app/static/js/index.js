/*
Dynamic home page functionality code
*/

import { sendEmailReceipt, generateBirdImg } from './api.js'

window.onload = init

/**
 * Handles `onload` event of `window`
 */
function init() 
{

    bird();

    var genderMale = document.getElementById('Male');
    genderMale.onclick = bird;

    var genderFemale = document.getElementById('Female');
    genderFemale.onclick = bird;

    var species = document.getElementById('Species');
    species.onchange = bird;

    var sizeSmall = document.getElementById('Small');
    sizeSmall.onclick = bird;

    var sizeMedium = document.getElementById('Medium');
    sizeMedium.onclick = bird;

    var sizeLarge = document.getElementById('Large');
    sizeLarge.onclick = bird;

    var primaryColor = document.getElementById('Primary');
    primaryColor.onchange = bird;

    var secondaryColor = document.getElementById('Secondary');
    secondaryColor.onchange = bird;

    document.getElementById('Submit').onclick = submitfunction;

}

function submitfunction() 
{
    callSendEmailReceipt;
}

/**
 * Live Bird Function
 * Tells customer what the price of their build-a-bird is based on 
 * their current customizations without pressing submit button
 */
function bird() 
{
    var price = 0;

    if(document.getElementById('Male').checked == true) 
        {
            price = price + 25.0
        }
    
    else if(document.getElementById('Female').checked == true) 
        {
            price = price + 25.0
        }

/*-----------------------------------------------------------------------------*/

    if(document.getElementById('Species').value == "Parakeet") 
        {
            price = price + 100.0
        }

    else if(document.getElementById('Species').value == "Conure") 
        {
            price = price + 1000.0
        }

    else if(document.getElementById('Species').value == "Cockatoo") 
        {
            price = price + 3500.0
        }

    else if(document.getElementById('Species').value == "Macaw") 
        {
            price = price + 4000.0
        }

/*-------------------------------------------------------------------------*/
    if(document.getElementById('Small').checked == true) 
        {
            price = price + 50.0
        }

    else if(document.getElementById('Medium').checked == true) 
        {
            price = price + 75.0
        }

    else if(document.getElementById('Large').checked == true) 
        {
            price = price + 100.0
        }
/*------------------------------------------------------------------------------*/
    if(document.getElementById('Primary').value == "Red") 
        {
            price = price + 10.0
        }
    
    else if(document.getElementById('Primary').value == "Blue") 
        { 
            price = price + 10.0  
        }
    
    else if(document.getElementById('Primary').value == "Green") 
        {
            price = price + 10.0
        }
/*------------------------------------------------------------------------------*/
    if(document.getElementById('Secondary').value == document.getElementById('Primary').value) 
        {
            price = price + 0.0
        }

    else
        {

        if(document.getElementById('Secondary').value == "Red") 
            {
                price = price + 10.0
            }
    
        else if(document.getElementById('Secondary').value == "Blue") 
            {
                price = price + 10.0
            }

        else if(document.getElementById('Secondary').value == "Green") 
            {
                price = price + 10.0
            }  

        }
    
    var totalPrice = document.getElementById('Price');
    totalPrice.innerText = "Total: $" + price.toFixed(2)

    console.log(price);
}


/**
 * Processes JSON response of call to asynchronous `sendEmailReceipt` function
 */
function sendEmailReceiptCallback() 
{

}

/**
 * Calls the `sendEmailReceipt` asynchronous function
 * with user's order data and establishes a callback to process JSON response
 */
function callSendEmailReceipt() 
{

}

/**
 * Processes JSON response of call to asynchronous `generateBirdImg` function
 */
function generateBirdImgCallback() 
{

}

/**
 * Calls the `generateBirdImg` asynchronous function
 * with user's order data and establishes a callback to process JSON response
 */
function callGenerateBirdImg() 
{

}