var MyClass = require('../src/myClass.js');
var sinon = require("sinon")
var myObj = new MyClass();
 var chai = require('chai'); 
var expect = chai.expect;
const chaiaspromise = require('chai-as-promised');
chai.use(chaiaspromise);

describe('Test suit', function(){

    before(function(){
        console.log('------Start of test suit------');
    });

    after(function(){
        console.log('-------After the test suit------');
    });

    beforeEach(function(){
        console.log('-------Before each test case-----');
    });

    afterEach(function(){
        console.log('-------After each test case-----');
    });

    it('Test the unit to words method', function(){
        expect(myObj.Unit2Words()).to.be.equal('এক জোড়া রান করা লক্ষ্ণৌ কলকাতাকে এক হালি রানে গুটিয়ে দিয়েছে। দেড় রানের এই জয়ে পয়েন্ট টেবিলের শীর্ষে চলে গেছে লক্ষ্ণৌ। কাগজে-কলমে কুড়ি হলেও এবার প্লে-অফটাও প্রায় নিশ্চিত হয়ে গেল দলটির। ওদিকে সোয়া/সওয়া ম্যাচে দেড় হারে আট পয়েন্ট নিয়ে চৌথা/সিকি/পোয়া থাকল কলকাতা নাইট রাইডার্স।'); 
    });  

    it('Test number to words method', function(){
        expect(myObj.Num2Word()).to.be.equal('চৌত্রিশ শিশুর প্রতি নিষ্ঠুরতার দণ্ড'); 
    });    

    it('Test ordinal number to words method', function(){
        expect(myObj.Ord2Word()).to.be.equal('একবিংশ শতাব্দীর অষ্টম আশ্চর্য কি হতে পারে'); 
    }); 

    it('Test date number to words method', function(){
        expect(myObj.Date2Words()).to.be.equal('আটই এপ্রিল সরকার তদন্ত শুরু করে'); 
    }); 

    it('Test big number to words method', function(){ 
        expect(myObj.NumtoWord()).to.be.equal('এক লক্ষ সাতচল্লিশ হাজার পাঁচশো সত্তর'); 
    });

    it('spy the date to words method', function(){
        var spy = sinon.spy(myObj, "NumtoWord");
        //sinon.assert.calledTwice(spy);
        expect(spy.calledOnce).to.be.true;

    });

    it('mock the say hello method', function(){
        var mock = sinon.mock(myObj);
        var expectation = mock.expects("sayHello");
        expectation.exactly(1);
        myObj.callAnotherFn(10,20);
        mock.verify();
    })

});

beforeEach(function(){
    console.log("====== Root level hook======");
});


describe.skip("Test the promise", function(){
    it('Promise the test case', function(){
        this.timeout(0);
        /*myObj.testPromise().then(function(result){
            expect(result).to.be.equal(6);
            done()*/
        return expect(myObj.testPromise()).to.eventually.equal(6);
        });
    });

describe("Test suit for stub", function(){
    it('stub the add method', function(){
        var stub = sinon.stub(myObj, "add");
        stub.withArgs(10,20).returns(100);
        expect(myObj.callAnotherFn(10, 20)).to.be.equal(  1000);
    });
});    
//});