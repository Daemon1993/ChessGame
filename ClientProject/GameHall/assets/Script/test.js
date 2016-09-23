
var socket = null;

if(cc.sys.isNative) {
    socket = SocketIO.connect('http://huoor.com:8888')
}else {
    socket = io('http://huoor.com:8888');
}

cc.Class({
    extends: cc.Component,
    properties: {
        label: {
            default: null,
            type: cc.Label
        },
    },

    // use this for initialization
    onLoad: function () {
        let self = this;
        this.label.string = '等待连接....';
        socket.on('connect', function(){
            self.label.string = '成功连接服务器'
            console.log('成功连接服务器')
        });
        socket.on('event', function(data){

        });
        socket.on('disconnect', function(){
            self.label.string = '失去连接'
        });
    },

    // called every frame
    update: function (dt) {
    },
});
