/*global h337*/
/*global Springy*/
var config = {
  container: document.getElementById('heatmap_container'),
  radius: 200,
  maxOpacity: .5,
  minOpacity: 0,
  blur: .75
};
var can, ctx;
$(function(){
    can = document.getElementById('eventMap');
    ctx = can.getContext('2d');
    $("#tree").springy({graph:graph})
});
function clear(){
    ctx.clearRect (0, 0, can.width, can.height);
}
 function drawLine(x, y, stopX, stopY){
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(stopX, stopY);
    ctx.closePath();
    ctx.stroke();
}

var graph = new Springy.Graph();
    
var events = [
    "LowGoal",
    "HighGoal",
    "Crossing",
    "PickupBall",
    "BlockedShot",
    "BlockedCrossing"
];

// create heatmap with configuration
var heatmap = h337.create(config);
function drawEventMap(data){
    for (var i = 0; i < data.length-1; i++){
        var pos = toPix(data[i],can);
        var posP = toPix(data[i+1], can);
        drawLine(pos.x,pos.y,posP.x,posP.y);
        ctx.fillText(events[data[i].evType] + "; " + i, data[i].x,data[i].y);
    }
    var pp = toPix(data.length-1, can);
    ctx.fillText(events[data[data.length-1].evType] + "; " + i, pp.x,pp.y);
    
}
function drawMatchMap(match_id){
    getEventDataForMatch({
        match:match_id,
        order:["time"],
        columns:["evType", "x", "y", "time"]
    }, drawEventMap);
}

function heatmapMap(data){
    heatmap.setData({min:0,max:1,data:[]});
    for(var point of data){
        heatmap.addData(toPixels(point, "#heatmap_image"));
    }
}
function toPix(obj,img){
  var image = $(img);
    var xPosition = obj.x * image.width();
    var yPosition = obj.y * image.height();
    return {x:xPosition,y:yPosition};
}
function toPixels(obj, img){
    var image = $(img);
    var xPosition = image.offset().left + obj.x * image.width();
    var yPosition = image.offset().top + obj.y * image.height();
    return {x:xPosition,y:yPosition,value:1};
}

function getEventDataForTeam(options, callback){
    $(".team-number").text("" + options.team);
    postRequest('/dev/team_event/', options,callback);
}
function getMatchDataForTeam(options, callback){
    $(".team-number").text("" + options.team);
    postRequest('/dev/team_match/',options,callback);
}
function postRequest(url, data, callback){
    $.ajax({
        url: url,
        method: "POST",
        data: {
            csrfmiddlewaretoken: $.cookie('csrftoken'),
            data: JSON.stringify(data)
        },
        success:function(data,blah,bleh){
            callback(data);
        }
    });
}
function getEventDataForMatch(options, callback){
    $(".team-number").text("" + options.team);
    postMessage('/dev/match_event_data/',options,callback);
}
function displayHeatmap(team,evType){
    getEventDataForTeam({
        team:team,
        filter:{
            evType:evType
        },
        columns:["x","y"]
    }, map);
}
function getCounts(team, callback){
    postRequest("/results/counts/", {
        team:team
        
    }, callback);
}
function getEventsSorted(team){
    getEventDataForTeam({
        team:team,
        order:["match_id","time"],
        columns:["time","match_id","evType"]
    }, createTree);
}
function createTree(data){
    var currentMatch = data[0].match_id;
    var root = graph.newNode({label:"root"});
    root.children = [];
    var lastElement = root;
    for(var event of data){
        if(event.match_id!=currentMatch){
            lastElement=root;
            currentMatch=event.match_id;
        }
        var eventName = events[parseInt(event.evType)];
        var exists = false;
        for(var child of lastElement.children){
            if(child.data.label.startsWith(eventName)){
                child.data.label += "(+1)";
                exists = true;
                lastElement = child;
                break;
            }
        }
        if(!exists){
            var newEvent = graph.newNode({label:eventName});
            lastElement.children.push(newEvent);
            newEvent.children = [];
            graph.newEdge(lastElement, newEvent);
            lastElement = newEvent;
        }
    }
}