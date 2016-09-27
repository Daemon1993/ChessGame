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
    },

    start:function(){
        var ws = new WebSocket("ws://huoor.com:8888/main");
        // if (ws.readyState === WebSocket.OPEN) 
        ws.onopen = function () {
            ws.send("Dall");
        };
        ws.onmessage = function (event) {
            console.log(event.data)
            if (event.data.indexOf('你的牌') >= 0) {
                console.log(event.data)
                return;
            }
            else if (event.data.indexOf('win') >= 0) {
                console.log(event.data)
                return;
            }
        };

        function createRoom() {
            ws.send("createRoom");
        }
        function getPuke1() {
            ws.send('{"code":1}');
        }
        function getPuke2() {
            ws.send('{"code":2}');
        }
    },

    // called every frame
    update: function (dt) {
    },
});
