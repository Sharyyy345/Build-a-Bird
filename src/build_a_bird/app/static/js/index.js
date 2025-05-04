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

    document.getElementById('Submit').onclick = callSendEmailReceipt;

    document.getElementById('Submit2').onclick = callGenerateBirdImg;

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
    if(this.readyState == 4 && this.status == 200)
    {
        // server sent response
        // and our request was successful

        console.log('successfully sent email!');

        var response = document.getElementById("RequestResponse");

        response.innerHTML = "Successfully sent email!";

    }
    else if(this.readyState == 4 && this.status != 200)
    {
        // server sent response
        // and our request was unsuccessful

        console.log('failed to send email');

        var response = document.getElementById("RequestResponse");

        response.innerHTML = "Email not sent. Please try again...";

    }

}

/**
 * Calls the `sendEmailReceipt` asynchronous function
 * with user's order data and establishes a callback to process JSON response
 */
function callSendEmailReceipt()
{
    var gender = null;
    var species = null;
    var size = null;
    var primaryColor = null;
    var secondaryColor = null;


    if(document.getElementById('Male').checked == true)
    {
        gender = document.getElementById('Male').value.toLowerCase()
    }

    else if(document.getElementById('Female').checked == true)
    {
        gender = document.getElementById('Female').value.toLowerCase()
    }
    
    species = document.getElementById('Species').value.toLowerCase()


    if(document.getElementById('Small').checked == true)
    {
        size = document.getElementById('Small').value.toLowerCase()
    }
    
    else if(document.getElementById('Medium').checked == true)
    {
        size = document.getElementById('Medium').value.toLowerCase()
    }

    else if(document.getElementById('Large').checked == true)
    {
        size = document.getElementById('Large').value.toLowerCase()
    }

    primaryColor = document.getElementById('Primary').value.toLowerCase()

    secondaryColor = document.getElementById('Secondary').value.toLowerCase()

    var name = document.getElementById("Name").value.toLowerCase()

    var email = document.getElementById("Email").value.toLowerCase()

    var data = {sex : gender, species : species, size: size, primary_feather_color : primaryColor, secondary_feather_color: secondaryColor, user_name : name, user_email : email} // input json order data
    console.log(data);

    sendEmailReceipt(sendEmailReceiptCallback, data);
}



/**
 * Processes JSON response of call to asynchronous `generateBirdImg` function
 */
function generateBirdImgCallback() 
{
    console.log('hi');

}

/**
 * Calls the `generateBirdImg` asynchronous function
 * with user's order data and establishes a callback to process JSON response
 */
function callGenerateBirdImg() 
{
    var gender = null;
    var species = null;
    var size = null;
    var primaryColor = null;
    var secondaryColor = null;


    if(document.getElementById('Male').checked == true)
    {
        gender = document.getElementById('Male').value.toLowerCase()
    }

    else if(document.getElementById('Female').checked == true)
    {
        gender = document.getElementById('Female').value.toLowerCase()
    }
    
    species = document.getElementById('Species').value.toLowerCase()


    if(document.getElementById('Small').checked == true)
    {
        size = document.getElementById('Small').value.toLowerCase()
    }
    
    else if(document.getElementById('Medium').checked == true)
    {
        size = document.getElementById('Medium').value.toLowerCase()
    }

    else if(document.getElementById('Large').checked == true)
    {
        size = document.getElementById('Large').value.toLowerCase()
    }

    primaryColor = document.getElementById('Primary').value.toLowerCase()

    secondaryColor = document.getElementById('Secondary').value.toLowerCase()

    var name = document.getElementById("Name").value.toLowerCase()

    var email = document.getElementById("Email").value.toLowerCase()

    var data = {sex : gender, species : species, size: size, primary_feather_color : primaryColor, secondary_feather_color: secondaryColor, user_name : name, user_email : email} // input json order data
    console.log(data);

    generateBirdImg(generateBirdImgCallback, data);

}