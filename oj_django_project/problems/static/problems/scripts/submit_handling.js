

class Config{
    static logging = true;
    static last_sub_time_prop_name = 'last-submission-time';
    static min_resub_time_delay = 30;
    static NOT_EXISTS = 'value-does-not-exists';

    // element id
    static verdict_element_id = 'verdict-element' ;
    static submitted_verdict_text = 'Code Submitted. Processing '
    static verdict_loading_gif_id = 'verdict-loading-gif' ;
}

class Assertions{
    static assertTrue(bool_expr){
        if(!bool_expr){
            throw new Error('Assertion Error : assertTrue() failed.')
        }
    }
}



class Logger{
    static log(message){
        // check if logging is on
        if(!Config.logging) return;
        
        // log message with timestamp.
        console.log("[" + (new Date().toLocaleString()) + "] " + message);
    }
}

class VerdictManager{

    static instance = new VerdictManager();

    constructor(){
        this.verdict_element = document.getElementById(Config.verdict_element_id);
        this.verdict_loading_gif = document.getElementById(Config.verdict_loading_gif_id);
    }

    show_loading_gif(){
        this.verdict_loading_gif.style.display = "inline";
    }

    hide_loading_gif(){
        this.verdict_loading_gif.style.display = "none";
    }

    set_verdict(verdict){
        // set verdict message in HTML DOM element.
        this.verdict_element.innerHTML = verdict;
    }

}


class Manager{

    static instance = new Manager();

    // return Date object or null
    get_last_sub_time(){
        const last_sub_time_str = localStorage.getItem(Config.last_sub_time_prop_name);
        let last_sub_time = null;
        // convert from string to object
        if(last_sub_time_str !== Config.NOT_EXISTS){
            last_sub_time = new Date(last_sub_time_str);
        }

        return last_sub_time;
    }

    is_submission_delay_enough(){

        const cur_time = new Date();
        let diff_time_sec = Number.MAX_VALUE;

        const last_sub_time = this.get_last_sub_time();
        Logger.log("last_sub_time : " + last_sub_time);

        if(last_sub_time !== null){
            Assertions.assertTrue( cur_time >= last_sub_time ) ;
            diff_time_sec = Math.floor( (cur_time - last_sub_time) / 1000) ;
        }

        Logger.log("diff_time_sec : " + diff_time_sec);

        return (diff_time_sec >= Config.min_resub_time_delay);
    }

    set_last_sub_time(datetime){
        localStorage.setItem(Config.last_sub_time_prop_name, datetime.toISOString());
    }


    submit(){

        Logger.log("Manager.submit() called.")

        // check when last submission was made, if more recently than 30 seconds, then say no.
        if(this.is_submission_delay_enough()){
            // save the submission time
            this.set_last_sub_time(new Date());
            // do the submission
            this.send_submission_to_server();
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
        // update verdict to processing
        // asynchronously update the verdict on recieving from server
    }


}



function handleSubmit(){
    Manager.instance.submit();
}


function onLoad(){
    VerdictManager.hide_loading_gif();
}

onLoad();


