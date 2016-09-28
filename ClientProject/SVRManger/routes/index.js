var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: '后台管理' });
});

router.get('/updateGit', function(req, res, next) {
	
});


module.exports = router;
