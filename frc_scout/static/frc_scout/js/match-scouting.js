//var backgroundColorRed = "rgb(255, 158, 158)";
var backgroundColorRed = "rgb(255, 204, 204)";
var backgroundColorBlue = "rgb(204, 216, 255)";


var defenses = ["Portcullis","Moat","Drawbridge","Rough Terrain","Rock Wall","Ramparts","Sally Port","Cheval de Frise"]
var schedule = null;
var matchdata = { 
    events : []
};
var matchProperties = {
    startTime:0,
    currentStage:""
};
var isAuton=true;
function imageCallback(x, y){
    matchdata.events[matchdata.events.length-1].x = x;
    matchdata.events[matchdata.events.length-1].y = x;
    $(".location-select").hide();
    $("#events").show();
}
var xPosition, yPosition;
/*
 Get the relative coordinates from start image
 */
$("#auto_start_image").click(function (event) {
    var image = $(this);

    xPosition = (event.pageX - image.offset().left) / image.width();
    yPosition = (event.pageY - image.offset().top) / image.height();

    if((yPosition > 0.18 && yPosition < 0.4) || yPosition > 0.62) {
        changeStage('autonomous_starting_location', 'autonomous');
    } else {
        alert(["Invalid starting location."], false);
    }
});
/*
 Run on page load
 */
$(function() {
    // always hide the loading thing once js is run
    $("#loading").hide();
    $("#prematch").show();

    /* If there's no hash setup a new match */
    if (window.location.hash === "" || !localStorage.pageMatchID) {
        console.log("new match: " + localStorage.pageMatchID);
        window.location.hash = "prematch";
        $("#" + window.location.hash.substring(1)).show();
        /* otherwise grab the old one and reuse it */
    }
    else {
        $(".stage").hide();
        $("#" + window.location.hash.substring(1)).show();
    }

    $("#alert").hide();

    $("input[type=checkbox]").bootstrapSwitch({
        'size': 'large',
        'onText': "YES",
        'offText': "NO"

    });

    if (localStorage.eventSchedule !== null && localStorage.eventSchedule !== undefined) {
        schedule = $.parseJSON(localStorage.eventSchedule);
    }
});
$(".input-location-image").click(function(event){
    var image = $(this);

    var xPosition = (event.pageX - image.offset().left) / image.width();
    var yPosition = (event.pageY - image.offset().top) / image.height();
    $("#displayDot").show();
    $("#displayDot").offset({
        left:image.offset().left + xPosition * image.width(),
        top:image.offset().top + yPosition * image.height()
    });
    if(confirm("Put it here?"))
        imageCallback(xPosition,yPosition);
    $("#displayDot").hide();
});


function getMatchData() {
    try {
        return $.parseJSON(localStorage["match" + localStorage.pageMatchID]);
    } catch (e) {
        return {};
    }
}

$("#match_number").on('keyup', function() {
    var match = parseInt($(this).val());
    var match_array = undefined;

    if(schedule !== null && schedule !== undefined) {
        $.each(schedule, function (k, v) {
            if (v.match_number === match) {
                match_array = schedule[k];
                return;
            }
        });
    }
    console.log('triggered blur');

    $("#select_team_number_select").find('.d').remove();

    if(match_array !== undefined) {
        var blue = match_array.alliances.blue.teams;
        var red = match_array.alliances.red.teams;

        var onetwothree =  [1, 2, 3]

        var index = 0;

        $.each(red, function(k, v) {
            $("#red" + k).text(v.substr(3));
            $("#select_team_number_select").append("<option class='d' data-color='red' value='" + v + "'>Red " + onetwothree[index] + ": " + v.substr(3) + "</option>");
            index++;
        });

        index = 0;

        $.each(blue, function(k, v) {
            $("#select_team_number_select").append("<option class='d' data-color='blue' value='" + v + "'>Blue " + onetwothree[index] + ": " + v.substr(3) + "</option>");
            $("#blue" + k).text(v.substr(3));
            index++;
        });

        $("#type_team_number").hide();
        $("#select_alliance_color").hide();
        $("#select_team_number").show();

        if(getMatchData().prematch) {
            if (getMatchData().prematch.team_number) {
                $("#select_team_number_select").val("frc" + getMatchData().prematch.team_number);
            }
        }
    } else {
        $("#type_team_number").show();
        $("#select_alliance_color").show();
        $("#select_team_number").hide();
    }

});

/*
 This will update the background color of the page based on the alliance selection
 Alliance colors are not stored permanently; they are only used to help scouts remember who they're scouting
 */
$(".alliance-toggle").on('change click', function() {
    var id = this.id;

    var child = $(this).find("option:selected");

    if (id === "blue_alliance" || child.data('color') === "blue") {
        $("body").css("background-color", backgroundColorBlue);
        localStorage.allianceColor = 'blue_alliance';
    }

    else if (id === "red_alliance" || child.data('color') === "red") {
        $("body").css("background-color", backgroundColorRed);
        localStorage.allianceColor = 'red_alliance';
    }


});
var events = {
    LowGoal:0,
    HighGoal:1,
    Crossing:2,
    PickupBall:3,
    BlockedShot:4,
    BlockedCrossing:5
};
$(".btn-add-subtract").click(function(event){
    var data = $(this);
    var eventData = {
        evType:data.attr("data-name"),
        isAuton:$("#autonomous").is(":visible"),
        time:Date.now()-matchProperties.startTime
    };
    $("#events").hide();
    $("#" + data.attr("selector")).show();
    matchdata.events.push(eventData);
});
$(".select-defense").on("change", function(event){
    var obj = $(this);
    $("#defense_select_" + getLast(obj)).text(defenses[obj.prop("selectedIndex")-1]);
});
$(".btn-defense").click(function(event){
    var obj = $(this);
    matchdata.events[matchdata.events.length-1].y = defenses.indexOf(obj.text(defenses));
    matchdata.events[matchdata.events.length-1].x = parseInt(getLast(obj));
    $("#defense_select").hide();
    $("#events").show();
});

function getLast(obj){
    return obj.attr("id")[obj.attr("id").length-1];
}
$("#undo").click(function(){
   if(confirm("Delete the last event\n" + JSON.stringify(matchdata.events[matchdata.events.length-1], null, 2))){
       matchdata.events.pop();
   }
});
/*
 This updates the title of each page with the team number
 */
$("#team_number").keyup(function() {
    $(".team-number").text(": " + $("#team_number").val());
});

function changeStage(fromStage, toStage){
    if(fromStage == "prematch") {
        matchdata.team_number =  parseInt($("#team_number").text());
        matchdata.match_number = parseInt($("#match_number").text());
        matchProperties.startTime = Date.now();
    }
    discardAndChangeStage(fromStage,toStage);
}

function discardAndChangeStage(fromStage, toStage) {
    $("#" + fromStage).hide();
    matchProperties.currentStage = toStage;
    $("#" + toStage).show();
}

function forwards()
{
    if(isAuton){
        isAuton = false;
        $("#scoutMode").text("Teleoperational");
        $("#back").text("autonomous");
        $("#forwards").text("finish");
    }
    else{
        changeStage("events","finish");
    }
}
function backwards(){
    if(isAuton){
        changeStage("events","prematch");
    }else{
        isAuton = true;
        $("#scoutMode").text("Autonomous");
        $("#back").text("prematch");
        $("#forwards").text("teleoperated");
    }
}
function cancelImage(){
    if(confirm("Are you sure?")){
        matchdata.events.pop();
        $(".stage").hide();
        $("#events").show();
    }
}
function saveData(){
    var matches = JSON.parse(localStorage.getItem("matches"));
    matches.push(matchdata);
    localStorage.setItem("matches", JSON.stringify(matches));
}

function attemptMatchSubmission(){
    if(localStorage.getItem("matches")){
        $.ajax({
            url: '/scouting/match/submit/',
            method: "POST",
            data: {
                csrfmiddlewaretoken: $.cookie('csrftoken'),
                data: localStorage.getItem("matches")
            },
            statusCode:{
                500:function(){
                    alert("Internal Server error");
                },
                400:function(){
                    alert("Your data had an issue");
                },
                403:function(){
                    alert("You're forbidden");
                }
            }
        });
    }
}




/*
 Check to make sure that the person didnt unintentionally leave
*/
window.onbeforeunload = function() {
    return "Are you sure you want to leave the page? If your internet connection is spotty, you may be unable to scout again.";
}