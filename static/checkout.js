function sumTotalAmount() {
    var product1amount = document.getElementById("product1").value;
    var product2amount = document.getElementById("product2").value; 
    var product3amount = document.getElementById("product3").value;
    var product4amount = document.getElementById("product4").value;
    var result = +product1amount + +product2amount + +product3amount + +product4amount;
    return document.getElementById('amount').value = parseFloat(result).toFixed(2);
}

function showShippingInfo() {
    var sameadr = document.getElementById("sameadr");
    var stinfo = document.getElementById("stinfo");
    if (sameadr.checked) {
        stinfo.style.display = "none";
        document.getElementById("stfname").value = document.getElementById("fname").value;
        document.getElementById("stlname").value = document.getElementById("lname").value;
        document.getElementById("stadr").value = document.getElementById("adr").value;
        document.getElementById("stcity").value = document.getElementById("city").value;
        document.getElementById("ststate").value = document.getElementById("state").value;
        document.getElementById("stzip").value = document.getElementById("zip").value;
        return;
    } else
        return stinfo.style.display = "block";
}

function autoFill() {
    let  userInfo  = document.getElementById("savedtoken").value;
    if(userInfo!="") {
        const request = new XMLHttpRequest()
        request.open("POST", `/views/processUserInfo/${userInfo}`)
    
        request.onload = () => {
            let return_data = JSON.parse(request.responseText);
            if(return_data.card.expirationMonth === undefined) {} else {document.getElementById("expmonth").value = return_data.card.expirationMonth;}
            if(return_data.card.expirationYear === undefined) {} else {document.getElementById("expyear").value = return_data.card.expirationYear;}
            if(return_data.billTo.firstName === undefined) {} else {document.getElementById("fname").value = return_data.billTo.firstName;}
            if(return_data.billTo.lastName === undefined) {} else {document.getElementById("lname").value = return_data.billTo.lastName;}
            if(return_data.billTo.address1 === undefined) {} else {document.getElementById("adr").value = return_data.billTo.address1;}
            if(return_data.billTo.locality === undefined) {} else {document.getElementById("city").value = return_data.billTo.locality;}
            if(return_data.billTo.country === undefined) {} else {document.getElementById("state").value = return_data.billTo.country;}
            if(return_data.billTo.postalCode === undefined) {} else {document.getElementById("zip").value = return_data.billTo.postalCode;}
            if(return_data.billTo.email === undefined) {} else {document.getElementById("email").value = return_data.billTo.email;}
            if(return_data.billTo.phoneNumber === undefined) {} else {document.getElementById("phone").value = return_data.billTo.phoneNumber;}
            if(return_data._embedded.instrumentIdentifier.card.number === undefined) {} else {document.getElementById("ccnum").value = return_data._embedded.instrumentIdentifier.card.number;}
            document.getElementById(return_data.card.type).checked = true;
        }
        return request.send();
    }
}

function trimNumber() {
    originalCreditCard = document.getElementById("ccnum").value;
    originalCreditCard = originalCreditCard.replaceAll('-','');
    originalCreditCard = originalCreditCard.replaceAll(' ','');
    
    originalPhone = document.getElementById("phone").value;
    originalPhone = originalPhone.replaceAll('-','');
    originalPhone = originalPhone.replaceAll(' ','');

    document.getElementById("ccnum").value = originalCreditCard;
    document.getElementById("phone").value = originalPhone;

    // document.getElementById("savedtoken").value = "";

    return;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function checkTokenization() {
    var tokenization = document.getElementById("tokenization");
    if (!tokenization.checked) {
        document.getElementById("savedtoken").value = "";
    }
    return;    
}