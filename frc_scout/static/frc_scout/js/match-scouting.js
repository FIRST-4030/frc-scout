var backgroundColorRed = "rgb(255, 221, 221)";
var backgroundColorBlue = "rgb(199, 208, 255)";

/*
 Run on page load
 */
$(function() {
    // always hide the loading thing once js is run
    $("#loading").hide();

    /* If there's no hash setup a new match */
    if(window.location.hash === "" || !localStorage.pageMatchID) {
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
        if (!localStorage["match" + i.toString()]) {
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
    var stageVariables = undefined;

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
            team_number: teamNumber,
            match_number: matchNumber
        }
    }

    else if(fromStage == "autonomous_starting_location") {
        stageVariables = {
            auto_start_x: xPosition,
            auto_start_y: yPosition
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
        var autoMovedBins = parseInt($("#auto-moved-bin-text").text());

        stageVariables = {
            auto_yellow_stacked_totes: autoStackedYellowTotes,
            auto_yellow_moved_totes: autoMovedYellowTotes,
            auto_grey_acquired_totes: autoAcquiredGreyTotes,

            auto_step_center_acquired_bins: autoAcquiredStepBins,
            auto_ground_acquired_bins: autoAcquiredGroundBins,
            auto_moved_bins: autoMovedBins,
            auto_moved_to_auto_zone: $("#auto_moved_to_alliance_zone").bootstrapSwitch('state')
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

        if(!storedVariables['autonomous_fouls_and_other']) {
            storedVariables['autonomous_fouls_and_other'] = {
                'auto_fouls': 0,
                'auto_interference': 0,
                'auto_no_auto': false
            }
        }

        // auto_no_auto is the only thing that's not a number
        if(id !== "auto_no_auto") {
            storedVariables['autonomous_fouls_and_other'][id] += 1;
        } else {
            storedVariables['autonomous_fouls_and_other'][id] = true;
        }

        // push to stage variables
        stageVariables = storedVariables['autonomous_fouls_and_other'];
    }

    else if(fromStage === "teleoperated_picked_up_totes") {
        var id = sender.id;

        /*
         Create the variable store if it doesn't yet exist
         */
        if(!storedVariables['teleoperated_picked_up_totes']) {
            storedVariables['teleoperated_picked_up_totes'] = {
                tele_picked_up_ground_upright_totes: 0,
                tele_picked_up_upside_down_totes: 0,
                tele_picked_up_sideways_totes: 0,
                tele_picked_up_human_station_totes: 0
            };
        }

        /*
         Add 1 to the sender's variable, the button's ID is the same as the one in localStorage
         */
        storedVariables['teleoperated_picked_up_totes'][id] += 1;

        /*
         For undoing things
         */
        storedVariables['teleoperated_picked_up_totes'].lastChange = id;
        $("#tele_picked_up_totes_subtract_button").prop('disabled', false);


        var totalThings = sumNumInDict(storedVariables['teleoperated_picked_up_totes']);

        $("#tele_picked_up_totes").text(totalThings);

        stageVariables = storedVariables['teleoperated_picked_up_totes'];
    }

    else if(fromStage === "teleoperated_stacked_totes") {
        var startHeight = $("#start_height").find('.active > input').data('height');
        var endHeight = $("#end_height").find('.active > input').data('height');

        $("#start_height").find('.active').removeClass('active');
        $("#end_height").find('.active').removeClass('active');

        if(isNaN(startHeight) || isNaN(endHeight)) {
            errorMessage.push("Both start and end height are required.");
        } else if(startHeight >= endHeight) {
            errorMessage.push("End height must be greater than start height.");
        } else {
            /*
             re-append all past arrays to be re-committed to localStorage
             */
            if(storedVariables['teleoperated_stacked_totes']) {
                stageVariables = storedVariables['teleoperated_stacked_totes'];
            } else {
                stageVariables = [];
            }

            /*
             then add our current one
             */
            stageVariables.push({
                start_height: startHeight,
                end_height: endHeight,
                coop_stack: $("#coop_stack").bootstrapSwitch('state')
            });

            $("#tele_stacked_totes_text").text(stageVariables.length);

        }

    }

    else if(fromStage === "teleoperated_stacked_totes_location") {

        /*
         add things to the latest one
         */

        var latestIndex = storedVariables['teleoperated_stacked_totes'].length - 1;

        storedVariables['teleoperated_stacked_totes'][latestIndex].x = xPosition;
        storedVariables['teleoperated_stacked_totes'][latestIndex].y = yPosition;

        stageVariables = storedVariables['teleoperated_stacked_totes'];

        // hacky way to make the right variable in localStorage be changed
        fromStage = "teleoperated_stacked_totes";
    }

    else if(fromStage === "teleoperated_picked_up_bins") {
        if(!storedVariables['teleoperated_picked_up_bins']) {
            storedVariables['teleoperated_picked_up_bins'] = {
                tele_picked_up_sideways_bins: 0,
                tele_picked_up_upright_bins: 0,
                tele_picked_up_center_step_bins: 0
            }
        }

        var id = sender.id;

        storedVariables['teleoperated_picked_up_bins'][id] += 1;

        /*
         For undoing things
         */
        storedVariables['teleoperated_picked_up_bins'].lastChange = id;
        $("#tele_picked_up_bin_subtract").prop('disabled', false);


        var totalThings = sumNumInDict(storedVariables['teleoperated_picked_up_bins']);

        $("#tele_picked_up_bins_text").text(totalThings);

        stageVariables = storedVariables['teleoperated_picked_up_bins'];

        /*
         For undoing things
         */
        storedVariables['teleoperated_picked_up_bins'].lastChange = id;
        $("#tele_picked_up_bins_subtract").prop('disabled', false);
    }

    else if(fromStage === "teleoperated_stacked_bins") {
        var startHeight = $("#bin_stack_height").find('.active > input').data('height');

        $("#bin_stack_height").find('.active').removeClass('active');

        if(isNaN(startHeight)) {
            errorMessage.push("Start height is required.");
        } else {
            /*
             re-append all past arrays to be re-committed to localStorage
             */
            if(storedVariables['teleoperated_stacked_bins']) {
                stageVariables = storedVariables['teleoperated_stacked_bins'];
            } else {
                stageVariables = [];
            }

            /*
             then add our current one
             */
            stageVariables.push(startHeight);

            $("#tele_stacked_bins_text").text(stageVariables.length);

        }
    }

    else if(fromStage === "teleoperated") {
        var pushedLitter = parseInt($("#tele_pushed_litter-text").text());
        var placedInBinLitter = parseInt($("#tele_placed_in_bin_litter-text").text());

        if(isNaN(pushedLitter) || isNaN(placedInBinLitter)) {
            errorMessage.push("This error should never occur unless you mess with the page, try refreshing it ;)");
        } else {
            stageVariables = {
                tele_pushed_litter: pushedLitter,
                tele_placed_in_bin_litter: placedInBinLitter
            };
        }
    }

    else if(fromStage === "teleoperated_fouls_and_other") {

        var id = sender.id;

        if(!storedVariables['teleoperated_fouls_and_other']) {
            storedVariables['teleoperated_fouls_and_other'] = {
                'tele_fouls': 0,
                'tele_knocked_over_stacks': 0,
                'tele_dead_bot': false,
                'tele_shooter_jam': 0
            }
        }

        // auto_no_auto is the only thing that's not a number
        if(id !== "tele_dead_bot") {
            storedVariables['teleoperated_fouls_and_other'][id] += 1;
        } else {
            storedVariables['teleoperated_fouls_and_other'][id] = true;
        }

        // push to stage variables
        stageVariables = storedVariables['teleoperated_fouls_and_other'];
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
        $(".team-number").text(": " + storedVariables.prematch.team_number);
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
            $("#team_number").val(storedVariables.prematch.team_number);
            $("#match_number").val(storedVariables.prematch.match_number);
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
            $("#auto-stacked-yellow-tote-text").text(storedVariables.autonomous.auto_yellow_stacked_totes);
            $("#auto-moved-yellow-tote-text").text(storedVariables.autonomous.auto_yellow_moved_totes);
            $("#auto-acquired-grey-tote-text").text(storedVariables.autonomous.auto_grey_acquired_totes);

            // bins
            $("#auto-acquired-step-bin-text").text(storedVariables.autonomous.auto_step_center_acquired_bins);
            $("#auto-acquired-ground-bin-text").text(storedVariables.autonomous.auto_ground_acquired_bins);
            $("#auto-moved-bin-text").text(storedVariables.autonomous.auto_moved_bins);

            if(storedVariables.autonomous.auto_moved_to_auto_zone) {
                $("#auto_moved_to_alliance_zone").bootstrapSwitch('state', true);
            }
        } catch(e) {}
    }

    else if(stage === "teleoperated") {
        $('title').text('Scouting: Teleoperated');

        /*
         Update totals for picked up totes
         */
        $("#tele_picked_up_totes").text(sumNumInDict(storedVariables['teleoperated_picked_up_totes']));

        if(storedVariables['teleoperated_picked_up_totes']) {
            if(storedVariables['teleoperated_picked_up_totes'].lastChange) {
                $("#tele_picked_up_totes_subtract_button").prop('disabled', false);
            }
        }

        if(storedVariables['teleoperated_stacked_totes']) {
            $("#tele_stacked_totes_text").text(storedVariables['teleoperated_stacked_totes'].length);
        }

        if(storedVariables['teleoperated_picked_up_bins']) {
            $("#tele_picked_up_bins_text").text(sumNumInDict(storedVariables['teleoperated_picked_up_bins']));
        }

        if(storedVariables['teleoperated_picked_up_bins']) {
            if(storedVariables['teleoperated_picked_up_bins'].lastChange) {
                $("#tele_picked_up_totes_subtract").prop('disabled', false);
            }
        }

        if(storedVariables['teleoperated_stacked_bins']) {
            $("#tele_stacked_bins_text").text(storedVariables['teleoperated_stacked_bins'].length);
        }

        try {
            $("#tele_pushed_litter-text").text(storedVariables['teleoperated'].tele_pushed_litter);
            $("#tele_placed_in_bin_litter-text").text(storedVariables['teleoperated'].tele_placed_in_bin_litter);
        } catch(e) {}

    }

    else if(stage === "teleoperated_stacked_totes") {
        $("#coop_stack").bootstrapSwitch({
            onText: "YES",
            offText: "NO"
        })
    }

    else if(stage === "teleoperated_fouls_and_other") {
        if(storedVariables['teleoperated_fouls_and_other'].tele_dead_bot) {
            //$("#tele_dead_bot").text("resurrected bot");
            $("#died_during_match_text").show();
            //} else {
            //    $("#tele_dead_bot").text("dead bot");
        }
    }

    $("#" + window.location.hash.substring(1)).show();
}

function getMatchData() {
    return $.parseJSON(localStorage["match" + localStorage.pageMatchID]);
}

function setMatchData(stage, name, value) {
    var data  = getMatchData();

    data[stage][name] = value;

    localStorage["match" + localStorage.pageMatchID] = JSON.stringify(data);
}

function setMatchDataArray(stage, value) {
    var data = getMatchData();

    data[stage] = value;

    localStorage["match" + localStorage.pageMatchID] = JSON.stringify(data);
}

/*
 Sum together all the values in dictionaries that are numbers
 */
function sumNumInDict(array) {
    var totalThings = 0;

    /*
     Iterate over in any manner IFF it's not undefined
     */
    if(array) {
        $.each(array, function(key, value) {
            if(!isNaN(value)) {
                totalThings += value;
            }
        });
    }

    return totalThings;
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

/*
 Get the relative coordinates from teleop location image
 */
$("#teleoperated_stacked_totes_image").click(function(event) {
    var image = $(this);

    xPosition = (event.pageX - image.offset().left) / image.width();
    yPosition = (event.pageY - image.offset().top) / image.height();

    saveAndContinue('teleoperated_stacked_totes_location', 'teleoperated');
});

/*
 Undo last thing from tele_picked_up_totes
 */

$("#tele_picked_up_totes_subtract_button").click(function() {
    var variables = getMatchData()['teleoperated_picked_up_totes'];

    var lastChange = variables.lastChange;

    /*
     only subtract if it exists and is > 0 (otherwise errors)
     */

    if(variables.lastChange) {
        if (variables[lastChange] > 0) {
            setMatchData("teleoperated_picked_up_totes", lastChange, variables[lastChange] - 1);
            setMatchData("teleoperated_picked_up_totes", 'lastChange', undefined);

            $("#tele_picked_up_totes_subtract_button").prop('disabled', true);
        }
    }

    $("#tele_picked_up_totes").text(sumNumInDict(getMatchData()['teleoperated_picked_up_totes']));

});

/*
 Undo last thing from tele_picked_up_bins
 */

$("#tele_picked_up_bins_subtract").click(function() {
    var variables = getMatchData()['teleoperated_picked_up_bins'];

    var lastChange = variables.lastChange;

    /*
     only subtract if it exists and is > 0 (otherwise errors)
     */

    if(variables.lastChange) {
        if (variables[lastChange] > 0) {
            setMatchData("teleoperated_picked_up_bins", lastChange, variables[lastChange] - 1);
            setMatchData("teleoperated_picked_up_bins", 'lastChange', undefined);

            $("#tele_picked_up_bins_subtract").prop('disabled', true);
        }
    }

    $("#tele_picked_up_bins_text").text(sumNumInDict(getMatchData()['teleoperated_picked_up_bins']));

});

$("#tele_stacked_totes_subtract").click(function() {
    var data = getMatchData()['teleoperated_stacked_totes'];

    data = data.slice(0, -1);

    setMatchDataArray('teleoperated_stacked_totes', data);

    $("#tele_stacked_totes_text").text(data.length);
});

$("#tele_stacked_bins_subtract").click(function() {
    var data = getMatchData()['teleoperated_stacked_bins'];

    data = data.slice(0, -1);

    setMatchDataArray('teleoperated_stacked_bins', data);

    $("#tele_stacked_bins_text").text(data.length);
});
