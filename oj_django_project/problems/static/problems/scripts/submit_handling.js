

class Assertions{
    static assertTrue(bool_expr){
        if(!bool_expr){
            throw new Error('Assertion Error : assertTrue() failed.')
        }
    }
}


class Config{
    static logging = true;
    static last_sub_time_prop_name = 'last-submission-time';
    static last_sub_id_prop_name = 'last-submission-id';
    static min_resub_time_delay = 30;
    static NOT_EXISTS = 'value-does-not-exists';
    static verdict_element_id = 'verdict-element' ;
    static submitted_verdict_text = 'Your code is submitted to the server.'
    static no_submission_verdict_text = 'You have not submitted anything yet.'
    
}

class Logger{
    static log(message){
        // check if logging is on
        if(!Config.logging) return;
        
        // log message with timestamp.
        console.log("[" + (new Date().toLocaleString()) + "] " + message);
    }
}


class Manager{

    static instance = new Manager();

    constructor(){
        // reset any submission data in the localStorage.
        // happens of each page refresh
        localStorage.setItem(Config.last_sub_time_prop_name, Config.NOT_EXISTS);
        localStorage.setItem(Config.last_sub_id_prop_name,   Config.NOT_EXISTS);
    }


    submit(){

        Logger.log("Manager.submit() called.")

        // check when last submission was made, if more recently than 30 seconds, then say no.
        const last_sub_time_str = localStorage.getItem(Config.last_sub_time_prop_name);
        let last_sub_time = null;
        // convert from string to object
        if(last_sub_time_str !== Config.NOT_EXISTS){
            last_sub_time = new Date(last_sub_time_str);
        }

        const cur_time = new Date();
        let diff_time_sec = Config.min_resub_time_delay;

        Logger.log("last_sub_time : " + last_sub_time);
        //Logger.log(typeof(last_sub_time));
        //Logger.log(last_sub_time[0]);
        if(last_sub_time !== null){

            //Logger.log("Afer chcek. last_sub_time : " + last_sub_time)
            // equality case for instantaneous clicks
            Assertions.assertTrue( cur_time >= last_sub_time ) ;
            
            diff_time_sec = Math.floor( (cur_time - last_sub_time) / 1000) ;
        }

        Logger.log("diff_time_sec : " + diff_time_sec);
        
        if(last_sub_time === null || 
            diff_time_sec >= Config.min_resub_time_delay
        ){
            // save the submission time
            localStorage.setItem(Config.last_sub_time_prop_name, cur_time.toISOString());
            // do the submission
            // read the text area and POST to server 
            let submission_id = this.send_submission() ;
            
            // save the submission id recieved
            Logger.log("Submission sent . id : " + submission_id);
            localStorage.setItem(Config.last_sub_id_prop_name, submission_id );
            // set the verdict
            this.set_verdict(Config.submitted_verdict_text);
        }
        else{
            // deny submission
            alert("Can only submit once in every " + Config.min_resub_time_delay + "sec.");
        }
   
    }

    send_submission_to_server(){
        // read text area
        // read language option
        // send data to server
        
        // return submission_id
    }

    refresh_verdict(){
        // get submission_id from localstorage
        // if no submission then say no submission
        let last_sub_id = localStorage.getItem(Config.last_sub_id_prop_name) ;
        Assertions.assertTrue( last_sub_id !== null )

        if(last_sub_id === Config.NOT_EXISTS){
            this.set_verdict(Config.no_submission_verdict_text);
        }
        else{
            // otherwise get_verdict_from_server 
            // and set it in html element
            let verdict = this.get_verdict_from_server(last_sub_id);
            this.set_verdict(verdict);
        }
    }

    set_verdict(verdict){
        // set verdict message in HTML DOM element.
        document.getElementById(Config.verdict_element_id).innerHTML = verdict;
    }

    get_verdict_from_server(submission_id){
        // request server for verdict
        // return verdict
    }

    

}



function handleSubmit(){
    Manager.instance.submit();
}

function handleVerdictRefresh(){
    Logger.log("handleVerdictRefresh() called");
    Manager.instance.verdict();
}


function test_sm(){
    Logger.log("msg");
}

test_sm();

