var MyClass = require('../src/myClass.js');
var sinon = require("sinon")
var myObj = new MyClass();
var chai = require('chai'); 
var expect = chai.expect;

describe('Test suit', function(){
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


});
