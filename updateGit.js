var exec = require('child_process').exec;
console.log('开始执行!')
exec('git pull origin master', function(err, stdout, stderr){
	if(err){
		console.log(stderr);
		return;
	}else {
		console.log('执行成功!')
		console.log(stdout)
	}
})
