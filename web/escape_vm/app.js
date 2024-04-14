const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const { VM } = require('vm2');
const uuid = require('uuid');
const morgan = require('morgan');

const app = express();
const vm = new VM();
const vmtokenPath = path.join(__dirname,'/img/vmtoken.txt');


app .use(bodyParser.urlencoded({extended: true}))
    .use(bodyParser.json())
    .use(morgan('dev'));

app.all('/', (req, res)=>{
    try{
        if(!fs.existsSync(vmtokenPath)){
            fs.writeFileSync(vmtokenPath, uuid.v4());
        }
        res.status(200).send("Welcome to easy VM challenge")
    }catch (e){
        res.status(500).send("error")
    }


});


app.all('/show', (req, res)=>{
    try{
        if(req.query.path.includes("flag")){
            res.status(403).send("no!!flag is not allowed");
        }

        if(req.query.path.split(".")[1] === "png" || req.query.path.split(".")[1] === "jpg"){
            res.sendFile(path.resolve('./img/' + req.query.path));
        }else{
            res.status(403).send('kidding me? this only allows images');
        }
    }catch(e){
        return res.redirect('/show?path=img1.jpg')
    }

});

app.all('/sandbox', (req, res) => {
    if(!fs.existsSync(vmtokenPath)){
        res.status(500).send("empty vm token file");
    }
    var token = fs.readFileSync(path.join(__dirname,'/img/vmtoken.txt'), 'utf8');
    fs.unlinkSync(vmtokenPath);
    if (req.query.vmtoken === token){
        try {
            var code = req.query.code || '';
            result = vm.run((code));
            res.status( 200).send(result);
        }catch (e){
            res.status(500).send("error")
        }

    } else{
        res.status(403).send("give me your token plz!")
    }

});

app.all('/', (req, res) => {
    return res.redirect('/show?path=img1.jpg')
});

app.listen(3000, () => console.log(`listening on port 3000!`));