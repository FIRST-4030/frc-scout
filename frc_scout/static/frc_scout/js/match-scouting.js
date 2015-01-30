var backgroundColorRed = "rgb(255, 221, 221)";
var backgroundColorBlue = "rgb(199, 208, 255)";

/*
 Run on page load
 */
$(function() {
    // always hide the loading thing once js is run
    $("#loading").hide();

    /* If there's no hash setup a new match */
    if(window.location.hash === "" || localStorage.pageMatchID === undefined) {
        setupNewMatch();
        console.log("new match: " + localStorage.pageMatchID);
        window.location.hash = "prematch";
        $("#" + window.location.hash.substring(1)).show();
        /* otherwise grab the old one and reuse it */
    } else {
        $(".stage").hide();
        $("#" + window.location.hash.substring(1)).show();
    }

    $("#alert").hide();
});

/*
 This will update the background color of the page based on the alliance selection
 Alliance colors are not stored permanently; they are only used to help scouts remember who they're scouting
 */
$(".alliance-toggle").click(function() {
    var id = this.id;

    if(id === "blue_alliance") {
        $("body").css("background-color", backgroundColorBlue);
    }

    else if(id === "red_alliance") {
        $("body").css("background-color", backgroundColorRed);
    }

    localStorage.allianceColor = id;
});

/*
 This updates the title of each page with the team number
 */
$("#team_number").keyup(function() {
    $(".team-number").text(": " + $("#team_number").val());
});


/*
 Function to run on page load or hash change

 On page load or hash change, hide everything then
 */
$(window).on('load hashchange', function() {
    console.log('reloaded: ' + window.location.hash);
    $(".stage").hide();

    openStage(window.location.hash.substring(1));
});

/*
 This will create a match ID in localStorage and save it to localStorage.pageMatchID
 */
function setupNewMatch() {
    /* Iterate through all matches currently in localStorage until we find an empty one */
    localStorage.allianceColor = undefined;
    for(var i = 0;; i++) {
        if (localStorage["match" + i.toString()] === undefined) {
            /* Then set our current match to a new one, storing the new one in localStorage */
            localStorage.pageMatchID = i;
            localStorage["match" + localStorage.pageMatchID.toString()] = JSON.stringify({});
            break;
        }
    }
}

/*
 This function handles stage changes and will be able to deal with page refreshes eventually
 */
function saveAndContinue(fromStage, toStage, sender) {

    var storedVariables = getMatchData();

    // assume no errors
    var errorMessage = [];

    // no variables for now
    var stageVariables = null;

    /**
     * FROM STAGES
     **/

    if(fromStage == "prematch") {
        var teamNumber = parseInt($("#team_number").val());
        var matchNumber = parseInt($("#match_number").val());

        if(isNaN(teamNumber)) {
            errorMessage.push("Team number is required and must be a number.");
        }

        if(isNaN(matchNumber)) {
            errorMessage.push("Match number is required and must be a number.");
        }

        if(!($("#red_alliance").hasClass('active') || $("#blue_alliance").hasClass('active'))) {
            errorMessage.push("Alliance color is required.");
        }

        stageVariables = {
            teamNumber: teamNumber,
            matchNumber: matchNumber
        }
    }

    else if(fromStage == "autonomous_starting_location") {
        stageVariables = {
            autoStartXPosition: xPosition,
            autoStartYPosition: yPosition
        }
    }

    else if(fromStage == "autonomous") {
        // totes
        var autoStackedYellowTotes = parseInt($("#auto-stacked-yellow-tote-text").text());
        var autoMovedYellowTotes = parseInt($("#auto-moved-yellow-tote-text").text());
        var autoAcquiredGreyTotes = parseInt($("#auto-acquired-grey-tote-text").text());

        // bins
        var autoAcquiredStepBins = parseInt($("#auto-acquired-step-bin-text").text());
        var autoAcquiredGroundBins = parseInt($("#auto-acquired-ground-bin-text").text());

        stageVariables = {
            autoStackedYellowTotes: autoStackedYellowTotes,
            autoMovedYellowTotes: autoMovedYellowTotes,
            autoAcquiredGreyTotes: autoAcquiredGreyTotes,

            autoAcquiredStepBins: autoAcquiredStepBins,
            autoAcquiredGroundBins: autoAcquiredGroundBins,
            autoMovedToAllianceZone: $("#auto_moved_to_alliance_zone").bootstrapSwitch('state')
        }

        $.each(stageVariables, function(index, variable) {
            if(isNaN(variable)) {
                errorMessage.push("One or more of your variables are not numbers, what are you doing?");
                return false;
            }
        })
    }

    else if(fromStage === "autonomous_fouls_and_other") {

        var id = sender.id;

        if(storedVariables['autonomous_fouls_and_other'] === undefined) {
            storedVariables['autonomous_fouls_and_other'] = {
                'autoFouls': 0,
                'autoInterference': 0,
                'autoNoAuto': false
            }
        }

        if(id === "auto_fouls") {
            storedVariables['autonomous_fouls_and_other'].autoFouls += 1;
        }
        else if(id === "auto_interference") {
            storedVariables['autonomous_fouls_and_other'].autoInterference += 1;
        }
        else if(id === "auto_no_auto") {
            storedVariables['autonomous_fouls_and_other'].autoNoAuto = true;
        }

        stageVariables = storedVariables['autonomous_fouls_and_other'];
    }


    // show alerts and bail if they exist
    if(errorMessage.length !== 0) {
        $("#alert-text").html(errorMessage.join('<br>'));
        $("#alert").show();
        return;
    }

    // otherwise hide any active alerts
    $("#alert").hide();

    // append our current values to the array that we get
    storedVariables[fromStage] = stageVariables;

    // push it back to localStorage
    localStorage['match' + localStorage.pageMatchID] = JSON.stringify(storedVariables);

    // hide our current stage
    $("#" + fromStage).hide();

    // change hash triggering the next stage to show
    window.location.hash = toStage;
}


function openStage(stage) {
    /**
     * TO STAGES
     **/

    // pull things out of localStorage as JSON
    var storedVariables = getMatchData();

    try {
        $(".team-number").text(": " + storedVariables.prematch.teamNumber);
    } catch(e) {}

    if(localStorage.allianceColor === "blue_alliance") {
        $("body").css("background-color", backgroundColorBlue);
        $("#blue_alliance").addClass('active');
    }

    else if(localStorage.allianceColor === "red_alliance") {
        $("body").css("background-color", backgroundColorRed);
        $("#red_alliance").addClass('active');
    }

    if(stage === "prematch") {
        $('title').text('Scouting: Prematch');
        try {
            $("#team_number").val(storedVariables.prematch.teamNumber);
            $("#match_number").val(storedVariables.prematch.matchNumber);
        } catch(e) {}
    }

    else if(stage === "autonomous") {
        $('title').text('Scouting: Autonomous');
        // moved to zone
        $("#auto_moved_to_alliance_zone").bootstrapSwitch({
            'offText': "NO",
            'onText': "YES"
        });

        // totes
        try {
            $("#auto-stacked-yellow-tote-text").text(storedVariables.autonomous.autoStackedYellowTotes);
            $("#auto-moved-yellow-tote-text").text(storedVariables.autonomous.autoMovedYellowTotes);
            $("#auto-acquired-grey-tote-text").text(storedVariables.autonomous.autoAcquiredGreyTotes);

            // bins
            $("#auto-acquired-step-bin-text").text(storedVariables.autonomous.autoAcquiredStepBins);
            $("#auto-acquired-ground-bin-text").text(storedVariables.autonomous.autoAcquiredGroundBins);

            if(storedVariables.autonomous.autoMovedToAllianceZone) {
                $("#auto_moved_to_alliance_zone").bootstrapSwitch('state', true);
            }
        } catch(e) {}
    }

    $("#" + window.location.hash.substring(1)).show();
}

function getMatchData() {
    return $.parseJSON(localStorage["match" + localStorage.pageMatchID]);
}

/*
 universal function that will add/subtract things from labels appended with -text from their respective buttons
 */
$(".btn-add-subtract").click(function() {
    var sender = $(this);
    var name = sender.data('name');

    var target = $("#" + name + "-text");

    if(target.data('max')) {
        var max = parseInt(target.data('max'));
    }

    if(sender.data('operation') === "add") {
        if(typeof max !== 'undefined' && parseInt(target.text()) < max || typeof max === 'undefined') {
            target.text(parseInt(target.text()) + 1);
        }
    }

    else if(sender.data('operation' == "subtract")) {
        if(parseInt(target.text()) > 0) {
            target.text(parseInt(target.text()) - 1);
        }
    }
});

var xPosition, yPosition;
/*
 Get the relative coordinates from start image
 */
$("#auto_start_image").click(function(event) {
    var image = $(this);

    xPosition = (event.pageX - image.offset().left) / image.width();
    yPosition = (event.pageY - image.offset().top) / image.height();

    saveAndContinue('autonomous_starting_location', 'autonomous');
});


