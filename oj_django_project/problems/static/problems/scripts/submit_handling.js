

class Config{
    static logging = true;
    static debug_mode = true; // set it false in prod environment at least
    static last_sub_time_prop_name = 'last-submission-time';
    static min_resub_time_delay = 5; // change in prod
    static sending_submission_text = 'Sending Submission';
    //static NOT_EXISTS = 'value-does-not-exists';

    // element id
    static verdict_element_id = 'verdict-element' ;
    static submitted_verdict_text = 'Code Submitted. Processing '
    static verdict_loading_gif_id = 'verdict-loading-gif' ;
    static code_input_element_id = 'submission-input-textarea';
    static language_selector_element_id = 'language-selector-list';
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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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

        // even if last_sub_time_str is null, or ISO string, it will work in both case automatically
        let last_sub_time = new Date(last_sub_time_str)
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

        
        // code text should be non empty
        if(document.getElementById(Config.code_input_element_id).value === ""){
            alert("Empty Code")
        }
        // check when last submission was made, if more recently than 30 seconds, then say no.
        else if(this.is_submission_delay_enough()){
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

    handleResponse(response){
        
    }

    send_submission_to_server(){
        
        // update verdict to processing
        VerdictManager.instance.set_verdict(Config.sending_submission_text);
        VerdictManager.instance.show_loading_gif();
        
        // send data to server
        // asynchronously update the verdict on recieving from server
        const request = this.create_submission_request();
        fetch(request).then((response) => {
            Logger.log("Response recieved");
            return response.json();
        })
        .then( (data) => {
            const verdict = data.verdict;
            VerdictManager.instance.set_verdict(verdict);
            VerdictManager.instance.hide_loading_gif();
        });
    }

    get_request_body(){
        const code = document.getElementById(Config.code_input_element_id).value ;
        const lang_selector = document.getElementById(Config.language_selector_element_id);
        const language_id = lang_selector.options[lang_selector.selectedIndex].value;
        
        // needs double quotes, needs comma seperation..
        const body_str =  `{
            "language_id" : "${language_id}",
            "problem_id" : "${cur_page_problem_id}",
            "code" : "${code}"
        }`;

        return body_str;
    }

    create_submission_request(){

        Logger.log("create_submission_request() called");
        // read text area
        // read language option
        // read token 
        // set headers and body
        const csrftoken = getCookie('csrftoken');

        const body_str = this.get_request_body();
        

        const request = new Request(
            'http://localhost:8000/submit/',
            {
                method: 'POST',
                //headers: {'X-CSRFToken': csrftoken},
                //mode: 'same-origin', // Do not send CSRF token to another domain.
                body : body_str
            }
        )

        
        if(Config.debug_mode){
            Logger.log("Request - csrftoken : " + csrftoken + 
            "\nlanguage_id : " + language_id + 
            "\nproblem_id : " + cur_page_problem_id +
            "\ncode : " + code);
        }


        // return request
        return request;
    }


}



function handleSubmit(){
    Manager.instance.submit();
}


function onLoad(){
    VerdictManager.instance.hide_loading_gif();
}

onLoad();


