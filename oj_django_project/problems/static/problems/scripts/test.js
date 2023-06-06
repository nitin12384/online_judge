function test_localstorage(){
    console.log("scripts started");
    localStorage.setItem('submission_id', 1234);
    console.log( localStorage.getItem('submission_id'));
}


// now we test classes

class Test{
    constructor(){
        this.var1 = 'a';
    }

    func1(){
        console.log("Test.var = " + this.var1);
    }

    static staticVar = 'staticVal';
}

function test_classes1(){
    test_var = new Test();
    test_var.func1();
    console.log("Test.staticVar : " + Test.staticVar)
}







test_classes1();
test_localstorage();
