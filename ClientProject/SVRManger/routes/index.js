var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: '后台管理' });
});

router.get('/updateGit', function(req, res, next) {
	var cmd = '';
	exec('git pull origin master', function(err, stdout, stderr){
		if(err){
			res.write(stderr)
			console.log(stderr);
			return;
		}else {
			console.log('执行成功!')
			res.writeln(stdout)
			console.log(stdout)
		}
	})
});


module.exports = router;
