var http = require('http')
var mq = require('mq')
var fs = require('fs')
var path = require('path')
var coroutine = require('coroutine')
var process = require('process')

//console.debug(process.argv)
var port = 9090
if(process.argv.length>2) {
  port = 1*process.argv[2]
}

var mkdir = function(dir, root) {
  if(!dir) {
    return;
  }
  root = root||''
  root = path.fullpath(root)
  var r = path.normalize(root+'/'+dir)
  var ps = dir.split(/\//)
  var d = root;
  for(var i in ps) {
    d = path.normalize(d+'/'+ps[i])

    if(!fs.exists(d)) {
      console.log('mkdir:'+d)
      fs.mkdir(d);
    }
  }
}

var write2fs = function(buffer, req) {

  var host = req.firstHeader('host')
  host = host.replace(':',"_")
  var root = '.'

  mkdir(host, root)

  var val = req.value==null||req.value==''||req.value=='/'?'index.html':req.value;
  if(val.lastIndexOf('/')==val.length-1) {
    val += 'index.html';
  }
  console.debug('req.value='+req.value+', ['+val+']')

  var p = path.normalize(val)  //默认页面index.html
  var index = p.lastIndexOf('/')
  if(index>0) {
    var d = p.substring(0, index)
    mkdir(host+'/'+d, root)
  }

  var f = path.fullpath(path.normalize(root+'/'+host+'/'+p))
  if(!fs.exists(f)) {
    console.log('write to: '+f)
    var file = fs.open(f, "a+")
    if(file) {
      file.truncate(0)
      file.write(buffer)
      file.close()
    }
  }

}

var proxy = function(resp, req) {
  if(resp) {
    //if(resp.status==300 || resp.status==301) {
    //  console.log('status:'+resp.status)
    //  return
    //}


    var headers = resp.headers
    var hs = {}
    for(var k in headers) {
      if(headers.has(k)) {
        //console.log(k+':'+headers[k])
        hs[k] = headers[k]
      }
    }

    var flag = 0;
    var ct = resp.firstHeader('Content-Type');
    console.debug('proxy status:'+resp.status+', Content-Type:'+ct)
    if(ct
      && (ct.match(/^text\/.*/gi)
          ||ct.match(/^image\/.*/gi)
          ||ct.match(/^application\/.*javascript.*/gi)
          ||ct.match(/^application\/.*json.*/gi)
          ||ct.match(/^application\/.*xml.*/gi))) {
      //console.log('flag++')
      flag++
    }
    if(req.value && (
      req.value.match(/\.ogg/i) 
      || req.value.match(/\.mp3/i)
      || req.value.match(/\.ttf/i)
      )) {
      flag++
    }

    var host = req.firstHeader('host')
    //console.log(host)
    if(host) {// && host.match(/.*\.cn/gi)) {
      flag++
      //console.log('flag++')
    }

    if(resp.status==200 && flag>1) {
      //resp.body.rewind()
      var buf = resp.readAll()
      //console.debug(buf)
      write2fs(buf, req)
    }
    resp.body.rewind()

    req.response.addHeader(hs)
    req.response.write(resp.body.readAll())
  }else {
    req.response.status = 501
  }
}

//console.log(route)
var routing = new mq.Routing({
  '^(.*)':function(r) {
    var method = r.method
    var url = r.address
    if(r.queryString && r.queryString.length>0) {
      url += '?'+r.queryString;
    }
    //r.removeHeader('host')
    console.log(method+' '+url) //r.protocol

/*
    if(url.indexOf('ddztest')>0) {
      console.log('sssssffffffs')
      var fff = fs.open('/Users/miro/work/work/game/code/httpproxy/9g.game6.cn/ddztest/game.html', "a+")
      r.response.addHeader("Content-Type","text/html")
      r.response.write(fff.readAll())
      return
    }
*/
    var headers = r.headers
    var hs = {}
    for(var k in headers) {
      if(!k.match(/host/i) && headers.has(k)) {
        console.log(k+':'+headers[k])
        hs[k] = headers[k]
      }
    }

    if(port==9999) {
      r.response.write('hello')
      return;
    }



    var body = r.body

    var resp = 	http.request(method, url, body, hs)
    proxy(resp, r);
  }
})

console.log('start http proxy server at '+port)
var svr = new http.Server(port, routing)
svr.run()
