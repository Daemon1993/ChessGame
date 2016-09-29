var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: '后台管理' });
});

router.all('/updateGit', function(req, res, next) {
	// res.render('index', { title: '后台管理' });
	console.log('start --------------------------------')
	var cmd ='cd /home/git/ChessGame/ && git pull origin master';   //'cd ~ && ls' 
	exec(cmd, function(err, stdout, stderr){
		if(err){
			res.jsonp({code:1, msg:stderr})
			console.log(stderr);
			return;
		}else {
			res.jsonp({code:0, msg:stdout})
			console.log(stdout)
			console.log('end --------------------------------')
		}
	})
});


module.exports = router;
