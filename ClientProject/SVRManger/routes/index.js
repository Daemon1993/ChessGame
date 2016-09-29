var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: '脆弱的后台管理' });
});
//拉取github代码
router.all('/updateGit', function(req, res, next) {
	console.log('start --------------updateGit------------------')
	var cmd ='cd /home/git/ChessGame/ && git pull origin master';   //'cd ~ && ls' 
	exec(cmd, function(err, stdout, stderr){
		if(err){
			res.jsonp({code:1, msg:stderr})
			console.log(stderr);
			return;
		}else {
			res.jsonp({code:0, msg:stdout})
			console.log(stdout)
			console.log('end --------------updateGit------------------')
		}
	})
});
//移动项目文件到指定位置
router.all('/updateGame', function(req, res, next){
	console.log('start ---------------updateGame-----------------')
	var target = '/home/git/ChessGame/ClientProject/GameHall/build/web-desktop'
	var endDir = '/home/git/ChessGame/ClientProject/SVRManger/public/web-desktop'
	var cmd ='cp -rf ' + target + ' ' + endDir;
	exec(cmd, function(err, stdout, stderr){
		if(err){
			res.jsonp({code:1, msg:stderr})
			console.log(stderr);
			return;
		}else {
			res.jsonp({code:0, msg:"成功更新文件夹!"})
			console.log(stdout)
			console.log('end --------------updateGame------------------')
		}
	})
})

module.exports = router;
