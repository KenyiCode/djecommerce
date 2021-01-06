// Query through html for buttons with desired class
var updateBtns = document.getElementsByClassName('update-cart')

// Loop through all buttons retrieved and add click event listeners
for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function() {
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log("productID: ", productID, "Action: ", action)

        // Verifies if user is logged in
        console.log("USER: ", user)
        if (user == "AnonymousUser"){
            addCookieItem(productID, action)
        }
        else{
            updateUserOrder(productID, action)
        }
    })
}

function addCookieItem(productID, action){
    console.log("User is not authenticated...")

    if (action == 'add'){
        if (cart[productID] == undefined){
            cart[productID] = {'quantity': 1}
        }
        else {
            cart[productID]['quantity'] += 1
        }

    }
    if (action == 'remove'){
        cart[productID]['quantity'] -= 1

        if (cart[productID]['quantity'] <= 0){
            console.log('Removed item...')
            delete cart[productID]
        }
    }

    console.log('Cart: ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}

function updateUserOrder(productID, action){
    console.log("User is authenticated, sending data...")
    var url = '/update_item/'

    fetch(url, {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productID': productID, 'action': action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('Data: ', data)
        location.reload()
    });
}