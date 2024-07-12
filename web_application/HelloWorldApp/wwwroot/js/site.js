// Please see documentation at https://learn.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.
document.addEventListener('DOMContentLoaded', function() {
    console.log('Hello from site.js!');
    // Your JavaScript code here

    function get_data_from_server() {
        const timeElapsed = Date.now();
        const today = new Date(timeElapsed);
        const current_date = today.toDateString();
        return data = {
            "machine": "Stroj 1",
            "date": current_date,
            "timestamp": Date.now(),
            "status": [{
                "control": "I",
                "label": "napajeni zapnuto",
                "state": Math.floor(Math.random() * 2),
                "max_states": 1
            }, {
                "control": "START",
                "label": "START produkce",
                "state": Math.floor(Math.random() * 2),
                "max_states": 1
            }, {
                "control": "STOP",
                "label": "STOP produkce",
                "state": Math.floor(Math.random() * 3),
                "max_states": 2
            }, {
                "control": "sipka nahoru a dolu",
                "label": "zvedani krytu",
                "state": Math.floor(Math.random() * 2),
                "max_states": 1
            }]
        }
    }
    get_data_from_server()
    
    function save_data_to_server(data) {
        
        console.log(data);
    }
    function current_controls(no_alert){
        var list = "";
        for (let i = 0; i < data.status.length; i++) {
            list += ("(č.: " + (i + 1) + ") " + data.status[i].control + ": " + data.status[i].label + ": " + data.status[i].state + " " + state_behaviour.label[data.status[i].state].Task + "\n")
        }
        if(no_alert == false){
            alert(list)
        } 
        return list;
    }
    function current_logic(no_alert){
        var list = "";
        for (let i = 0; i < state_data.logic.length; i++) {
            list += ("(č.: " + i + ") " + state_data.logic[i].state_label + ", " + state_data.logic[i].combination + " (" + current_state_by_words(state_data.logic[i].combination) + ")" + "\n")
        }
        if(no_alert == false){
            alert(list)
        }
        return list;
    }
    var more_columns = 0;
    function add_control(){
        var correct_name = false;
        var cancelled = false;
        while(correct_name == false){
            var control_name = prompt("Zadejte nazev nove kontrolky")
            if(chosen_ok_input(control_name)==true){
                for (let i = 0; i < data.status.length; i++) {
                    if(control_name == data.status[i].control){
                        console.log("Nazev nove kontrolky: " + control_name + " je jiz zabrany")
                        alert("Nazev nove kontrolky: " + control_name + " je jiz zabrany")
                        i = data.status.length;
                    } else if(i == data.status.length-1){
                        correct_name = true;
                    }
                }
            }else{
                correct_name = true;
                cancelled = true;
            }
        }
        var correct_label = false;
        while(correct_label == false && cancelled == false){
            var control_label = prompt("Zadejte popis nove kontrolky")
            if(chosen_ok_input(control_label)==true){
                for (let i = 0; i < data.status.length; i++) {
                    if(control_label == data.status[i].label){
                        console.log("Popis nove kontrolky: " + control_label + " je jiz zabrany")
                        alert("Popis nove kontrolky: " + control_label + " je jiz zabrany")
                        i = data.status.length;
                    } else if(i == data.status.length-1){
                        correct_label = true;
                    }
                }
            }else{
                correct_label = true;
                cancelled = true;
            }
        }
        if(cancelled == false){
            control_states = "";
            var finished = false;
            var end_add_control = false;
            var right_input = false;
            while (control_states != null && finished == false  && end_add_control == false){
                var control_states = prompt("Zadejte pocet stavu nove kontrolky (1-3), [nesviti,sviti,blika]")
                if(chosen_ok_input(control_states) == true){
                    if(range_input_right(control_states,1,3) == true){
                        //nastaveni logiky s novou kontrolkou u vsech kombinaci
                        var manually = confirm("Prejete si prednastavit u nove kontrolky pro kazdou logiku zakladni stav, 0 (nesviti)?\nNebo nastavit manualne? ")
                        if(manually == false){
                            for (let i = 0; i < state_data.logic.length; i++) {
                                //pro pripadne preruseni for cylku:
                                if(end_add_control == false){
                                    var new_logic_set = prompt("Nastavte logiku s novou kontrolkou pro:\n" + state_data.logic[i].state_label + " (č.: " + i + ")"
                                    + "\n(s novou kontrolkou jiz: " + (data.status.length+1) +" stavu)\nZadejte cislo v rozsahu stavu kontrolky, tedy: 0-" + (control_states-1));
                                    if(chosen_ok_input(new_logic_set) == true){
                                        //right_input = logic_verification(new_logic_set,false,true,i,0,2);
                                        //aby sedel pocet stavu dane kontrolky
                                        right_input = range_input_right(new_logic_set,0,control_states-1);
                                        if(right_input == false){ 
                                            //vratime se o krok zpet...
                                            i -=1;
                                        } else{
                                            //prenastaveni logiky v pripade spravneho inputu: (nutne predelat na pole)
                                            var new_logic_comb = state_data.logic[i].combination
                                            new_logic_comb = new_logic_comb.toString().replace(/\./g, '');
                                            new_logic_comb = new_logic_comb.toString().replace(/\,/g, '');
                                            new_logic_comb = new_logic_comb.toString().replace(/\ /g, '');
                                            new_logic_comb += new_logic_set; //pridame nove nastaveny stav pro kontrolku
                                            new_logic_comb = String(new_logic_comb).split("").map((new_logic_comb)=>{
                                                return Number(new_logic_comb);
                                            })
                                            state_data.logic[i].combination = new_logic_comb;
                                        }
                                    } else {
                                        end_add_control = confirm("Veskere nastaveni, co jste doted provedli bude zruseno, opravdu si prejete prerusit zadavani?");
                                        if(end_add_control == false){
                                            //vratime se o krok zpet... pokud true, operace prerusena...
                                            i -=1;
                                        }
                                    }
                                }
                            }
                        } else { 
                            for (let i = 0; i < state_data.logic.length; i++) {
                                new_logic_set = state_data.logic[i].combination
                                new_logic_set = new_logic_set.toString().replace(/\./g, '');
                                new_logic_set = new_logic_set.toString().replace(/\,/g, '');
                                new_logic_set = new_logic_set.toString().replace(/\ /g, '');
                                new_logic_set += 0; //pridame nulu pro vsechny logiky
                                new_logic_set = String(new_logic_set).split("").map((new_logic_set)=>{
                                    return Number(new_logic_set);
                                })
                                
                                state_data.logic[i].combination = new_logic_set;
                            }
                            console.log("Pro novou kontrolku byly prednastaveny logiky se stavem 0 (nesviti)" +"\n\n"+ current_logic(true));
                            alert("Pro novou kontrolku byly prednastaveny logiky se stavem 0 (nesviti)" +"\n\n"+ current_logic(true));
                            right_input = true;
                        }                       
                        
                        if(end_add_control == false && right_input == true){
    
                            //logika prenastavena, muzeme pridat novou kontrolku...
                            //posledni status stroje...
                            data.status[data.status.length] = {
                            "control": String(control_name),
                            "label": String(control_label),
                            "state": Math.floor(Math.random() * control_states),
                            "max_states": control_states-1
                            }
    
                            console.log("Byla pridana nova kontrolka: " + control_name + " (" + control_label + ") s poctem stavu: " + control_states)
                            alert("Byla pridana nova kontrolka: " + control_name + " (" + control_label + ") s poctem stavu: " + control_states)
                            //Refresh stranky:
                            more_columns +=1;
                            result = main();
                            logic_table();
                            finished = true; 
                        }  
                    }
                }                              
            }
        }                
    }
    
    function delete_control(){
        var completed = false;
        while(completed != true && completed != "cancelled"){
            var which = prompt("Kterou kontrolku si prejete odstranit? \nVyberte v rozsahu od: 1 do: " + data.status.length + "\n\n" + current_controls(true));
            if(chosen_ok_input(which) == true){
                if(range_input_right(which,1,data.status.length) == true){
                    var really = confirm("Opravdu si prejete samzat kontrolku s nazvem: " + data.status[which - 1].label + " ?");
                    if(really == true){
                        var name_to_delete = data.status[which - 1].label;
                        if(which < data.status.length) {
                            //posun ostatnich kontrolek, pokud je predesla podminka rovna, staci jen smazat...
                            for(let i = which; i < data.status.length; i++){
                                data.status[i-1].control = data.status[i].control;
                                data.status[i-1].label = data.status[i].label;
                                data.status[i-1].state = data.status[i].state;
                                data.status[i-1].max_states = data.status[i].max_states;
                            }
                        }
                        //mazani logiky s danou kontrolkou:
                        for(let i = 0; i < state_data.logic.length; i++){
                            //pro splice funkci bylo potreba predelat do pole, protoze s novou kontrolkou uz to bralo jako string
                            var no_comma = state_data.logic[i].combination;
                            no_comma = no_comma.toString();
                            no_comma = no_comma.replace(/\,/g, ' ');
                            no_comma = no_comma.replace(/\ /g, '');
                            const array = Array.from(no_comma);
                            //console.log(array)
                            array.splice((which-1),1)
                            //console.log(array)
                            state_data.logic[i].combination = array;
                        }
                        //smazani
                        alert("Byla smazana kontrolka s nazvem: " + name_to_delete);
                        console.log("Byla smazana kontrolka s nazvem: " + name_to_delete);
                        data.status.length -=1;
                        //REFRESH
                        result = main();
                        logic_table();
                        completed = true;
    
                    }else {
                        alert("Mazani zruseno")
                        console.log("Mazani zruseno")
                        completed = "cancelled";
                    }
                } 
            } else {
                completed = "cancelled";
            }
        }
        return completed;
    }
    
    function delete_logic(){
        var which_one = prompt("Jakou logiku kontrolek si preje odstranit? Vepiste cislo od 0 do: "+(state_data.logic.length-1)+ "\n\n" + current_logic(true));
        if(chosen_ok_input(which_one) == true){
            if(range_input_right(which_one,0,(state_data.logic.length-1)) == true){
                logic_to_delete = state_data.logic[which_one].state_label
                var really = confirm("Opravdu si prejete odstranit logiku s nazvem: " + state_data.logic[which_one].state_label);
                if(really == true){
                    if(which_one < state_data.logic.length) {
                        for(let i = Number(which_one); i < state_data.logic.length-1; i++){
                            state_data.logic[i].combination = state_data.logic[i+1].combination
                            state_data.logic[i].state_label = state_data.logic[i+1].state_label
                        }
                        alert("Byla smazana logika s nazvem: " + logic_to_delete)
                        state_data.logic.length -= 1;
                        //REFRESH
                        result = main();
                        logic_table();
                    }        
                }
            }
        }
    }
    
    function logic_verification(input,add,change,chosen_logic,logic_name,adding_new_control){
        var correct_numbers = 0;
        var right_input = false;
        var change_successful = false;
        var cancel_cycle = false;
        
        input = input.replace(/\ /g, '');
        input = input.replace(/\./g, '');
        input = input.replace(/\,/g, '');
        input = String(input).split("").map((input)=>{
            return Number(input);
        })
        state_data.logic[chosen_logic].combination = state_data.logic[chosen_logic].combination.toString().replace(/\ /g, '');
        state_data.logic[chosen_logic].combination = state_data.logic[chosen_logic].combination.toString().replace(/\,/g, '');
        state_data.logic[chosen_logic].combination = state_data.logic[chosen_logic].combination.toString().replace(/\./g, '');
        const comb = state_data.logic[chosen_logic].combination
        
        state_data.logic[chosen_logic].combination = String(comb).split("").map((comb)=>{
            return Number(comb);
        })
    
        for (let i = 0; i < (state_data.logic[chosen_logic].combination.length + adding_new_control); i++) {
            if(cancel_cycle == false){
    
                //aby nebylo dovoleno zadat vetsi stav, nez dovoluje nastaveni kontrolky:
                if (input[i] > data.status[i].max_states){
                    console.log(input[i] + " je mimo rozsah moznych stavu kontrolky: " + data.status[i].label + " ("+ data.status[i].control + ")\n(zadejde cislo v rozsahu: 0-"+ data.status[i].max_states + ")");
                    alert(input[i] + " je mimo rozsah moznych stavu kontrolky: " + data.status[i].label + " ("+ data.status[i].control + ")\n(zadejde cislo v rozsahu: 0-"+ data.status[i].max_states + ")");
                    cancel_cycle = true;
                } else {
                    correct_numbers +=1;
                } 
            }
        }
        
        
        //adding new control uz vyzaduje logiku o 1 delsi...
        if ((input.length == state_data.logic[chosen_logic].combination.length + adding_new_control) && (correct_numbers == state_data.logic[chosen_logic].combination.length + adding_new_control)){
            right_input = true;
        } else {
            console.log("spatne zadano, zkuste to prosim znovu");
            alert("spatne zadano, zkuste to prosim znovu");
        }
        change_successful = false;
        if(right_input == true) {
            //Probiha overovani...
            if(add == true){
                var match = false;
                for (let i = 0; i < state_data.logic.length; i++) {
                    if (input.toString() == state_data.logic[i].combination.toString()){
                        var colision = state_data.logic[i].state_label;
                        match = true;
                    }
                }
                if (match == false){
                    change_successful = true;
                    
                } else {
                    console.log("Kombinace: " + input + " je jiz zabrana")
                    var repeat = confirm("Kombinace: " + input + " je jiz zabrana pro stav: "+ colision + "\nPrejete si zmenit zadanou odpoved(OK)? Nebo ponechat stejnou? ")
                    if(repeat == true){
                        right_input = false;
                    } else {
                        change_successful = true;
                    }
                }
                         
            }else if (change == true){
                if (state_data.logic[chosen_logic].combination != input){
                var match = false;
                for (let i = 0; i < state_data.logic.length; i++) {
                    if (input.toString() == state_data.logic[i].combination.toString()){
                        match = true;
                    }
                }
                if (match == false){
                    change_successful = true;
                    
                } else {
                    console.log("Kombinace: " + input + " je jiz zabrana")
                    var repeat = confirm("Kombinace: " + input + " je jiz zabrana." + "\nPrejete si zmenit zadanou odpoved(OK)? Nebo ponechat stejnou? ")
                    if(repeat == true){
                        right_input = false;
                    } else {
                        change_successful = true;
                    }
                }
                
                } else if(change == true) {
                    console.log("Kombinace je stejna, netreba menit");
                    var repeat = confirm("Kombinace je stejna, netreba menit.\nPrejete si zkusit znovu? ")
                    if(chosen_ok_input(repeat) == true){
                        right_input = false;
                    } else{
                        change_successful = "cancelled";
                    }
                }
            }
        }
        if(change_successful == true){
            if(add == true){
                console.log("Byla pridana nova logika: " + logic_name + " s kombinaci: " + input + " (" + current_state_by_words(input) + ")");
                alert("Byla pridana nova logika: " + logic_name + " s kombinaci: " + input + " (" + current_state_by_words(input) + ")");
            }
            if(change == true){
                console.log("Kombinace " + state_data.logic[chosen_logic].combination + " (" + current_state_by_words(state_data.logic[chosen_logic].combination) + ") " +
                " pro stav s nazvem: " +  state_data.logic[chosen_logic].state_label + " (č.:" + chosen_logic + ")" + " ,byla zmenena na: " + input + " (" + current_state_by_words(input) + ") ");
                alert("Kombinace " + state_data.logic[chosen_logic].combination + " (" + current_state_by_words(state_data.logic[chosen_logic].combination) + ") " +
                " pro stav s nazvem: " +  state_data.logic[chosen_logic].state_label + " (č.:" + chosen_logic + ")" + " ,byla zmenena na: " + input + " (" + current_state_by_words(input) + ") ");
            }
        }
        
        
        return change_successful;
    }
    
    function add_logic(){
        var cancelled = false;
        var correct_name = false;
        while(correct_name == false){
            var logic_name = prompt("Zadejte popis funkce nove logiky")
            if(chosen_ok_input(logic_name) == true){
                for (let i = 0; i < state_data.logic.length; i++) {
                    if(logic_name == state_data.logic[i].state_label){
                        console.log("Zadany nazev logiky " + logic_name + " je jiz zabrany")
                        alert("Zadany nazev logiky " + logic_name + " je jiz zabrany")
                        i = state_data.logic.length; //skocim pryc z for cyklu
                    } else if(i == state_data.logic.length-1){
                        correct_name = true;
                    }
                }
            }else{
                //chceme vyskocit z while cyklu
                correct_name = true;
                cancelled = true;
            }
        }
        if(cancelled == false){
            var right_input = false;
            var logic_combination = "";
            while(right_input == false && logic_combination != null){
                var max_states_arr ="";
                for (let i = 0; i < data.status.length; i++) {
                    max_states_arr =  max_states_arr + " " + data.status[i].label +" ("+ data.status[i].control + "): "  + data.status[i].max_states + " stavu\n";
                }
                logic_combination = prompt("Zadejte funkce kontrolek ve formatu: \"0,0,0\"..." + " aktualne pro: " + data.status.length + " kontrolek \n s maximalnim poctem stavu jednotlivych kontrolek:\n\n" + max_states_arr);
                if(chosen_ok_input(logic_combination) == true){
                    //kdyz pridavame novou, tak pro provnani zvolena prvni, jiz ulozena kombinace (chosen_logic = 0)... irelevantni
                    right_input = logic_verification(logic_combination,true,false,0,logic_name,0);
                } 
            }
            
            //Kdyz je uspesne vlozen input, je vlozena nova logika...
            if (right_input == true){
                logic_combination = logic_combination.replace(/\./g, '');
                logic_combination = logic_combination.replace(/\,/g, '');
                logic_combination = logic_combination.replace(/\ /g, '');
                logic_combination = String(logic_combination).split("").map((logic_combination)=>{
                    return Number(logic_combination)
                })
                state_data.logic[state_data.logic.length] = {
                "state_label": String(logic_name),
                "combination": logic_combination//.split("")
                }
                //REFRESH
                result = main();
                logic_table();
            }
        }   
    }
    //Jiz nevyuzita funkce, nahrazeno primou zmenou klikem na policko v tabulce
    function customise_logic(){
    
        var pick_successful = false;
        var state_pick = "";
        while(pick_successful == false && state_pick != null){
            var state_pick = prompt("U jakeho stavu chcete zmenit logiku kontrolek? \n(Vepiste cislo od 0 nebo cely nazev bez diakritiky)" + "\n\n" + current_logic(true));
            //pokud nebylo zruseno...
            if (chosen_ok_input(state_pick) == true) {
                for (let i = 0; i < state_data.logic.length; i++) {
                    if (state_pick.toString() == state_data.logic[i].state_label.toString() || state_pick == i){
    
                        console.log("Pro upravu byl zvolen stav s nazvem: " + state_data.logic[i].state_label + " a logikou stavu: " + state_data.logic[i].combination + 
                        " (" + current_state_by_words(state_data.logic[i].combination) + ") ");
                        alert("Pro upravu byl zvolen stav s nazvem: " + state_data.logic[i].state_label + " a logikou stavu: " + state_data.logic[i].combination + 
                        " (" + current_state_by_words(state_data.logic[i].combination) + ") ");
    
                        selected_state = i;
                        pick_successful = true
                    }
                }
                if (pick_successful == false){
                    console.log("mimo rozsah...")
                    alert("mimo rozsah...")
                }
            }
        }
        
        // Pokud bylo zvoleni uspesne, tak se definuji zmeny:
        if (pick_successful == true){
            //Osetreni pro spravny input ze strany uzivatele:
            var right_input = false;
            var combination_change = "";
    
            while (right_input == false && right_input != "cancelled" && combination_change != null){
                combination_change = prompt("Jak si prejete zmenit zvolenou kombinaci? " + state_data.logic[selected_state].combination + 
                " ,tedy:\n "+ current_state_by_words(state_data.logic[selected_state].combination) + " ,vyuzijte stejneho ciselneho formatu")
                if (chosen_ok_input(combination_change) == true){
                    right_input = logic_verification(combination_change,false,true,selected_state,0,0);        
                }  
            }
            //Kdyz je uspesne vlozen input je prepsana logika kontrolek...
            if (right_input == true) {
                combination_change = combination_change.replace(/\ /g, ',');
                combination_change = combination_change.replace(/\./g, ',');
                state_data.logic[selected_state].combination = combination_change;
                //REFRESH
                //kvuli aktualnimu zvyrazneni vysledku musim volat i main...
                result = main();
                logic_table();
            }        
        } 
    }
    
    function current_state_by_words(input){
    
        var combination_by_words = [];
        for (let i = 0; i < input.length; i++) {
            if(input[i] == 0){
                combination_by_words[i] =  state_behaviour.label[0].Task
            }
            if(input[i] == 1){
                combination_by_words[i] =  state_behaviour.label[1].Task
            }
            if(input[i] == 2){
                combination_by_words[i] =  state_behaviour.label[2].Task
            }         
        }
        combination_by_words = combination_by_words.toString().replace(/\,\,/g, ',');
        return combination_by_words;
    }
    
    function chosen_ok_input(input){
        if(input == null || input == ""){
            console.log("Zadavani zruseno uzivatelem");
            alert("Zadavani zruseno uzivatelem");
        } else {
            return true;
        }
    }
    
    function range_input_right(input,range_from,range_to){
        if(input <= range_to && input >= range_from){
            return true;
    
        } else {
            console.log("Zadane cislo neni v danem rozsahu: " + range_from + " - " + range_to);
            alert("Zadane cislo neni v danem rozsahu: " + range_from + " - " + range_to);
            return false;
        }
    }
    
    //Vyjadreni chovani kontrolek slovy:
    state_behaviour = {
        "label":[{
            "Task": "nesviti"
        },{
            "Task": "sviti"
        },{
            "Task": "blika"
        }]
    }
    
    //Urceni zadane logiky:
    state_data = {
        "logic": [{
            "state_label": "vypnuti hlavniho vypinace",
            "combination": [0,0,0,0]
        }, {
            "state_label": "napeti vypnuto",
            "combination": [0,0,1,1]
        }, {
            "state_label": "napeti zapnuto",
            "combination": [1,0,0,1]
        }, {
            "state_label": "stroj vyrabi",
            "combination": [1,1,0,0]
        }, {
            "state_label": "chyba stroje",
            "combination": [1,0,2,1]
        }, {
            "state_label": "havarijni stop 1",
            "combination": [0,1,1,0]
        }, {
            "state_label": "havarijni stop 2",
            "combination": [0,0,2,1]
        }, {
            "state_label": "zaucovani stroje",
            "combination": [1,1,0,1]
        }]
    }
    
    //MAIN---------------------------------------------------------------------------------------------------------------------
    function main() {
        //vytvareni hlavni tabulky aktualniho stavu
        var table = document.createElement('table');
        table.setAttribute('border', '2');
        var tRow = document.createElement('tr');
        var tData = document.createElement("td");
        tData.className = "bold";
        //flexibilne spojuji bunky podle poctu kontrolek
        tData.colSpan = 5 + more_columns;
        tData.textContent = "Stav stroje (" + data.machine + ")";
    
        tRow.appendChild(tData);
        table.appendChild(tRow);
    
        var tRow = document.createElement('tr');
        var tData = document.createElement('td');
        tData.className = "bold2";
        tData.textContent ="Kontrolka:"
        tRow.appendChild(tData);
        //vytvareni pole proporovnavani se spravnou delkou
        var current_combination = [];
        for (let i = 0; i < data.status.length; i++) {
            current_combination += i;
        }
        var current_combination_arr = Array.from(current_combination)
        //vypisovani kontrolek
        for (let i = 0; i < data.status.length; i++) {
            current_combination_arr[i] = data.status[i].state;
    
            var tData = document.createElement('td');
            tData.textContent = data.status[i].control + "\n (" + data.status[i].label + ")";
            tRow.appendChild(tData);
        }
    
        table.appendChild(tRow);
        var tRow = document.createElement('tr');
        var tData = document.createElement('td');
        tData.className = "bold2";
        tData.textContent ="Stav:"
        tRow.appendChild(tData);
        //vypisovani stavu kontrolek
        for (let i = 0; i < data.status.length; i++) {
        var tData = document.createElement('td');
            if(data.status[i].state == 0){
                tData.className = "nesviti"; 
            } else if(data.status[i].state==1){
                tData.className = "sviti"; 
            } else if(data.status[i].state==2){
                tData.className = "blika"; 
            }
            
            tData.textContent = state_behaviour.label[data.status[i].state].Task + " (" + data.status[i].state + ")" ;
            tRow.appendChild(tData);
        }
        table.appendChild(tRow);
        //vypisovani a overovani vysledku
        var tRow = document.createElement('tr');
        var tData = document.createElement('td');
        tData.className = "bold2";
        tData.textContent = "Vysledek: ";
        tRow.appendChild(tData);
        var tData = document.createElement("td");
        tData.className = "result";
        tData.colSpan = 4 + more_columns;
        var sum_of_bad_combinations = 0;
        var result = "";
        for (let i = 0; i < state_data.logic.length; i++) {
            if (current_combination_arr.toString() == state_data.logic[i].combination.toString()){
                result = state_data.logic[i].state_label;
                tData.textContent = state_data.logic[i].state_label ;  
            } else {
                sum_of_bad_combinations += 1;
            }
        }
        if (sum_of_bad_combinations == state_data.logic.length){
            tData.textContent =  "neplatny stav" ;       
        }
    
        tRow.appendChild(tData);
        table.appendChild(tRow);
    
        document.getElementById("main_table").innerHTML = table.outerHTML;
        
    
        if (result == "chyba stroje"){
            //Nastavit timeout aby se nacetla stranka
            setTimeout(() => {
                var error_message =  "Vepiste poznamku/duvod chyby: ";   
                custom_prompt(error_message);
            }, 500);
        }
        return result;
    }
        
    result = main();
    
    //zvlastni okno pro zapsani duvodu chyby stroje
    function custom_prompt(text){
        document.querySelector("#prompttext").innerText = text;
        document.querySelector("#custom_prompt").classList.remove("hidden");
        return new Promise((resolve, reject) => {
            document.querySelector("#promptbutton").onclick = () =>{
                resolve(document.querySelector("#promptinput").value);
                document.querySelector("#custom_prompt").classList.add("hidden");
    
                save_data_to_server("timestamp: " + data.timestamp + ", datum: " + data.date + ", stroj: " + data.machine + 
                ", stav stroje: "+ state_data.logic[4].state_label + ", poznamka: "+ document.querySelector("#promptinput").value);
            }
        });
    }
    
    //Vypis aktualni logicke tabulky
    
    function logic_table(){
        var table = document.createElement('table');
        table.setAttribute('border', '2');
        //Nadpis
        var tRow = document.createElement('tr');
        var tData = document.createElement("td");
        tData.className = "bold";
        tData.colSpan = 5 + more_columns;
        tData.textContent = "Tabulka nastavene logiky  ";
    
        const btn = document.createElement("button");
        btn.setAttribute("id", "info_button");
        btn.textContent = "INFO";
        btn.className = "info_btn";
       
        tData.appendChild(btn);
        tRow.appendChild(tData);
        table.appendChild(tRow);
    
        var tRow = document.createElement('tr');
        var tData = document.createElement('td');
        tData.className = "bold2";
        tData.textContent ="Kontrolka:"
        tRow.appendChild(tData);
        for (let i = 0; i < data.status.length; i++) {
            var tData = document.createElement('td');
            tData.textContent = data.status[i].control + " (" + data.status[i].label + ")";
            tRow.appendChild(tData);
        }
    
        table.appendChild(tRow);
        id_for_cells = 0;
    
        for(let i = 0; i < state_data.logic.length; i++) {
            var tRow = document.createElement('tr');
            var tData = document.createElement('td');
            if(state_data.logic[i].state_label == result){
                //zvyrazneni vysledku
                tData.className = "result";
            }else{
                tData.className = "bold2";
            }
            tData.textContent = state_data.logic[i].state_label;
            tRow.appendChild(tData);
    
            for (let j = 0; j < state_data.logic[i].combination.length; j++) {
                var tData = document.createElement('td');
                if(state_data.logic[i].combination[j] != ","){
                    if(state_data.logic[i].combination[j] == 0){
                        tData.className = "nesviti";
                    } else if(state_data.logic[i].combination[j]==1){
                        tData.className = "sviti"; 
                    } else if(state_data.logic[i].combination[j]==2){
                        tData.className = "blika"; 
                    }
                    //nastaveni id jednotlivych policek tabulky od nuly
                    id_for_cells++;
                    tData.setAttribute('id',id_for_cells)
                    
                    if(id_for_cells == logic_to_change && logic_to_change != 0){
                        const old_combination = state_data.logic[i].combination.toString();
                        if(tData.className == "nesviti" && logic_to_change != 0){
                            state_data.logic[i].combination[j] = 1;
                            console.log("U logiky \"" + state_data.logic[i].state_label + "\" byla zmenena kombinace " + old_combination + " na: " + state_data.logic[i].combination)
                            tData.className = "sviti";
                            result = main();
                            logic_to_change = 0;
                            
                        }else if(tData.className == "sviti" && logic_to_change != 0){
                            state_data.logic[i].combination[j] = 2;
                            console.log("U logiky \"" + state_data.logic[i].state_label + "\" byla zmenena kombinace " + old_combination + " na: " + state_data.logic[i].combination)
                            tData.className = "blika";
                            result = main();
                            logic_to_change = 0;
    
                        }else if(tData.className == "blika" && logic_to_change != 0){
                            state_data.logic[i].combination[j] = 0;
                            console.log("U logiky \"" + state_data.logic[i].state_label + "\" byla zmenena kombinace " + old_combination + " na: " + state_data.logic[i].combination)
                            tData.className = "nesviti";
                            result = main();
                            logic_to_change = 0;
                        }
                    }
                    tData.textContent = state_behaviour.label[state_data.logic[i].combination[j]].Task + " (" + state_data.logic[i].combination[j] + ")" ;
                    tRow.appendChild(tData);
                }         
            }
        table.appendChild(tRow);
        }
        document.getElementById("logic_table").innerHTML = table.outerHTML;
        
        btn_read();
    }
    logic_table();
    
    
    var logic_to_change = 0
    var id_for_cells = 32;
    
    function btn_read(){
        const btn_info = document.getElementById("info_button");
        if(btn_info){
            btn_info.addEventListener("click", function(){
                info();
            });
        }
        for(let i = 1;i<id_for_cells+1;i++){
            const btn = document.getElementById(i);
            if(btn){
                btn.addEventListener("click", function(){
                    //Pro jakou pozici v kombinaci bude provadena zmena (jake tl. z tabulky bylo zmacknuto)
                    logic_to_change = i;    
                    logic_table();
                    logic_table();
                });
            }
        }
    }
    
    function info(){
        alert("Zmena logiky lze primym klikem na policko v tabulce");
        console.log("Zmena logiky lze primym klikem na policko v tabulce");
    }
    
    
});
