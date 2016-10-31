cc.Class({
    extends: cc.Component,
    properties: {
        uidEdit:{
            default:null,
            type:cc.EditBox
        },
        label: {
            default: null,
            type: cc.Label
        },
        loginBtn: {
            default: null,
            type: cc.Button
        },
    },
    // use this for initialization
    onLoad: function () {
        var ws = new WebSocket("ws://huoor.com:8888/main");
        ws.onopen = function () {
            console.log('连接成功!   ' + "ws://huoor.com:8888/main")
        };
        ws.onmessage = function (event) {  //服务器返回消息
            console.log(event.data)
        };
        this.ws = ws;
    },
    testLogin:function(){
        var pack = {}
        pack.code = "11"
        pack.uid = 12
        this.ws.send(JSON.stringify(pack))
        this.label.string = '正在登陆...';
    },
    // called every frame
    update: function (dt) {
    },
});
