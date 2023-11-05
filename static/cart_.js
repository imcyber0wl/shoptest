if (user=='AnonymousUser')
    {

    function getCookie_2(name) {
        //split cookie string and get all name:value pairs in an array
        var cookiearr=document.cookie.split(";")

        //loop through the array elements
        for (var i=0; i<cookiearr.length;i++) {
            var cookiepair=cookiearr[i].split("=")
            //compare it with given string
        
            if (name==cookiepair[0].trim()){
                //return decoded cookie value 
                return decodeURIComponent(cookiepair[1])
                }
            }

        //if not found,return null
        return null
        }

    var cart=JSON.parse(getCookie_2('cart'))
    if (cart==undefined){
    cart= {} //empty js object
    }

    var shipinfo=JSON.parse(getCookie_2('shipinfo'))
    if (shipinfo==undefined){
    shipinfo= {} //empty js object
    }

    var dcart="cart="+JSON.stringify(cart)+";domain=;path=/" 
    document.cookie="cart="+JSON.stringify(cart)+";domain=;path=/" 
    document.cookie="shipinfo="+JSON.stringify(shipinfo)+";" 

    //set cookie for all website not just a page

    console.log(document.cookie)

    function addcookieitem(productid, action,color){
console.log('x',color)
        if (color==undefined){color='None'}

        if (action=="add"){

            if(cart[productid]==undefined){
                cart[productid]={}
                console.log(cart[productid])
            }

            if (cart[productid][color]==undefined){
                cart[productid][color]={'quantity':1}
                console.log(cart[productid][color])
            }
        
            else {
                cart[productid][color]['quantity'] +=1 }
        }


        if (action=="remove"){
            cart[productid][color]['quantity'] -=1
            if (cart[productid][color]['quantity'] <= 0) {
                delete cart[productid][color] 
             }
        }

    document.cookie="cart="+JSON.stringify(cart)+";domain=;path=/" 
    location.reload()
    }

}
// ************ important! for guest cart sometimes csrf token doesnt work
//so we go to the top of html and put {% csrftoken %} and then put this JS to get the django csrf token!
if (csrftoken==null){
casrftoken=document.getElementsByTagName("input")[0].value }

var updateBtns=document.getElementsByClassName("update-cart")
    
for (var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){

        var productid=this.dataset.product
        var action=this.dataset.action
var page=document.getElementById("cart_token").value
console.log(page)
if(page!='cart'){
var color='color1'

try{if(document.getElementById('color1').checked){color='color1'}}
catch(err){ console.log(1==1) }

try{if(document.getElementById('color2').checked){color='color2'}}
catch(err){ console.log(1==1)}

try{if(document.getElementById('color3').checked){color='color3'}}
catch(err){ console.log(1==1)}

try{if(document.getElementById('color4').checked){color='color4'}}
catch(err){ console.log(1==1) }
}

else{var color=this.dataset.color
console.log(1==1)}

        console.log('productid:',productid,'action:',action,color)

        if (user=='AnonymousUser'){
            console.log('User is not logged in')
            addcookieitem(productid, action,color)
        }

        else{
            updateUserOrder(productid,action,color)
        }

    }
    )

}

function updateUserOrder(productId,action,color){
    console.log(user=='AnonymousUser','User is logged in, sending data...')
    var url='/update-item/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productid':productId,'action':action,'color':color})
        })

    .then((response)=>{
        return response.json()

      })

    .then((data) => {
        location.reload()
    })

}
