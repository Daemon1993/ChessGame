//socket连接服务 

//加载协议

//1.连接服务器,得到单例的操作对象
//2.收发心脏包,掉线重连
//3.根据协议发包
//4.根据协议解析包
//5.解析包后找对对应的处理handler
//6.提供注册事件回调

var config = {
	"url": "huoor.com:8888/main",
	//协议类型
	"Protocol":{
		"code":{

		}
	}
}

var ws = null
var SocketService = {};

SocketService.init = function() {

}

//连接服务器
SocketService.connect = function(){
	if(ws)return ws;
	ws = new WebSocket('ws://' + config.url); //连接服务器
	ws.onopen = function () {
        console.log('连接:' + config.url + " 成功!")
    };
    ws.onmessage = function (event) {  //服务器返回消息
    	SocketService.parseData(event.data);
    };
    return ws;
}

SocketService.sendPack = function(data){
	//TODO
	ws.send(JSON.stringify(data))
}

SocketService.parseData = function(data){
	cc.log(data)
	return data
}



module.exports = SocketService;