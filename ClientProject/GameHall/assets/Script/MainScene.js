var SocketService = require('SocketService')

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
        this.ws = SocketService.connect();
    },
    testLogin:function(){
        var pack = {}
        this.ws.send(JSON.stringify(pack))
        this.label.string = '正在登陆...';
    },
    // called every frame
    update: function (dt) {
    },
});
