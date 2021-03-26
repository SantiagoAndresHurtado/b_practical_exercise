function load_list() {
    let xmlhttp = new XMLHttpRequest();
    baseurl = "http://localhost:2222/api";
    xmlhttp.open("POST", baseurl + "/list", true);      //Header information along with the request
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    let aux = document.getElementById("name").selectedIndex;        //Variables from de html view
    let name = document.getElementById("name").options;
    let initial = document.getElementById("initial").value;
    let final = document.getElementById("final").value;

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            let response = JSON.parse(xmlhttp.responseText);        //Recieve a JSON response

            let empTable = document.getElementById("empTable").getElementsByTagName("tbody")[0];
            empTable.innerHTML = "";
            for (item = 0; item < response.length; item++) {        //If there are more than 1 order id
                    let val = response[item];
        
                    let NewRow = empTable.insertRow(0);     // insert new row
                    let creation = NewRow.insertCell(0); 
                    let order_id = NewRow.insertCell(1); 
                    let total = NewRow.insertCell(2); 
                    let delivery = NewRow.insertCell(3); 
                    let products = NewRow.insertCell(4); 
                    
                    creation.innerHTML = val['Creation_Date']; 
                    order_id.innerHTML = val['Order_ID']; 
                    total.innerHTML = val['Total'];
                    delivery.innerHTML = val['Delivery_Address'];
                    
                    let product = val['Products'];
                    if (product == 0) {
                        products.innerHTML = 0
                    }
                    else{
                        let list = "";
                        for (key in product){       //Add products to each order
                            let aux = product[key]
                            list += "<li>"+aux+" x "+key+"</li>"
                        }
                        products.innerHTML = list;
                    }
            };
        };
    };
    xmlhttp.send(JSON.stringify({ "name": name[aux].text, "initial_date": initial, "final_date": final }));     //Send petition to the web service
} 
