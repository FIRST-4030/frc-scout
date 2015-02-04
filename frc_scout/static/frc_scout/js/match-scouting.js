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

window.onbeforeunload = function() {
    return "Are you sure you want to leave the page? If your internet connection is spotty, you may be unable to scout again.";
}

/*
 This will create a match ID in localStorage and save it to localStorage.pageMatchID
 */
function setupNewMatch() {
    console.log('setting up new match');
    localStorage.allianceColor = undefined;
    localStorage.totesInPossession = undefined;

    /* Iterate through all matches currently in localStorage until we find an empty one */
    $("#team-number").text("");
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
 This function handles stage changes (will persist after page refresh)
 */
function saveAndContinue(fromStage, toStage, sender) {

    var storedVariables = getMatchData();

    // assume no errors
    var errorMessage = [];
    var userCorrectionRequired = true;

    // no variables for now
    var stageVariables = undefined;

    /**
     * FROM STAGES
     **/

    if(fromStage == "prematch") {
        var teamNumber = parseInt($("#team_number").val());
        var matchNumber = parseInt($("#match_number").val());

        if(isNaN(teamNumber) || teamNumber < 1) {
            errorMessage.push("Team number is required and must be a number of one or greater.");
        }

        if(isNaN(matchNumber) || matchNumber < 1) {
            errorMessage.push("Match number is required and must be a number of one or greater.");
        }

        if(!($("#red_alliance").hasClass('active') || $("#blue_alliance").hasClass('active'))) {
            errorMessage.push("Alliance color is required.");
        }

        stageVariables = {
            team_number: teamNumber,
            match_number: matchNumber
        };
    }

    else if(fromStage == "autonomous_starting_location") {
        stageVariables = {
            auto_start_x: xPosition,
            auto_start_y: yPosition
        };

        if(!confirm("Confirm autonomous starting location.")) {
            return false;
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
        };

        $.each(stageVariables, function(index, variable) {
            if(isNaN(variable)) {
                errorMessage.push("One or more of your variables are not numbers, what are you doing?");
                return false;
            }
        });
    }

    else if(fromStage === "autonomous_fouls_and_other") {

        var id = sender.id;

        if(!storedVariables['autonomous_fouls_and_other']) {
            storedVariables['autonomous_fouls_and_other'] = {
                'auto_fouls': 0,
                'auto_interference': 0,
                'auto_no_auto': false
            };
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


        /*
         Update totes in possession
         */

        console.log('starting');

        if(!isNaN(localStorage.totesInPossession) || localStorage.totesInPossession === undefined) {
            var currentTotes = localStorage.totesInPossession;
            localStorage.totesInPossession = parseInt(currentTotes) + 1;
        } else {
            localStorage.totesInPossession = 1;
        }

        $("#totes_in_possession").text(localStorage.totesInPossession);
    }

    else if(fromStage === "teleoperated_stacked_totes") {
        var startHeight = $("#start_height").find('.active > input').data('height');
        var endHeight = $("#totes_added").find('.active > input').data('height');

        $("#start_height").find('.active').removeClass('active');
        $("#totes_added").find('.active').removeClass('active');

        if(isNaN(startHeight) || isNaN(endHeight)) {
            errorMessage.push("Both start and end height are required.");
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
                totes_added: endHeight,
                coop_stack: $("#coop_stack").bootstrapSwitch('state')
            });

            $("#tele_stacked_totes_text").text(stageVariables.length);

        }

    }

    else if(fromStage === "teleoperated_stacked_totes_location") {

        /*
         add things to the latest one
         */


        if(!confirm("Confirm teleoperated stacked totes location.")) {
            return false;
        }

        var latestIndex = storedVariables['teleoperated_stacked_totes'].length - 1;

        storedVariables['teleoperated_stacked_totes'][latestIndex].x = xPosition;
        storedVariables['teleoperated_stacked_totes'][latestIndex].y = yPosition;

        var removedFromPossession = storedVariables['teleoperated_stacked_totes'][latestIndex].totes_added;

        console.log(removedFromPossession);

        var final = localStorage.totesInPossession - removedFromPossession;

        if(final >= 0) {
            localStorage.totesInPossession  = final;
        } else {
            localStorage.totesInPossession = 0;
        }

        $("#totes_in_possession").text(localStorage.totesInPossession);

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
            };
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
            };
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

    else if(fromStage === "postmatch") {
        var teleFoulContext = $("#tele_foul_context").val();
        var telePrivateComments = $("#tele_private_comments").val();
        var telePublicComments = $("#tele_public_comments").val();

        stageVariables = {
            tele_foul_context: teleFoulContext,
            tele_private_comments: telePrivateComments,
            tele_public_comments: telePublicComments,
            scouting_complete: true
        };
    }

// show alerts and bail if they exist
    if(errorMessage.length !== 0) {
        showErrorMessages(errorMessage, userCorrectionRequired);
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

function showErrorMessages(messages, correctErrors) {
    $("#alert-text").html(messages.join('<br>'));
    $("#alert").show();

    console.log('pushing errors');

    if(correctErrors) {
        $("#correct_errors").show();
    } else {
        $("#correct_errors").hide();
    }
}

function submitData() {
    var pendingMatches = getPendingMatches();

    $("#online_message").hide();
    $("#in_progress_message").show();

    $.ajax({
        url: '/scouting/match/submit/',
        method: "POST",
        data: {
            csrfmiddlewaretoken: $.cookie('csrftoken'),
            data: JSON.stringify(pendingMatches)
        },
        success: function() {
            clearPendingMatches();

            $("#saved").hide();
            $("#submitted").show();
            $("#in_progress_loading").fadeIn(1000);

            window.setTimeout(function() {
                setupNewMatch();
                $("#in_progress_message").hide();
                $("#finished_message").show();
            }, 2000);

        },
        error: function() {
            showErrorMessages(["Data submission failed."], false);
            $("#in_progress_message").hide();
            $("#online_message").hide();
            $("#offline_message").show();
        }
    });
}

function saveDataOffline() {
    setupNewMatch();
    $("#submitted").hide();
    $("#in_progress_message").hide();
    $("#saved").show();
}

function openStage(stage) {
    /**
     * TO STAGES
     **/

    $("#alert").hide();

    if (!getMatchData()) {
        window.location.hash = "prematch";
    }

    if(getMatchData()) {
        if($.isEmptyObject(getMatchData()) || getMatchData() === undefined || getMatchData() === null) {
            window.location.hash = "prematch";
        }
    }

    // pull things out of localStorage as JSON
    var storedVariables = getMatchData();

    try {
        $(".team-number").text(": " + storedVariables.prematch.team_number);
    } catch (e) {
        $(".team-number").text("");
    }

    if (localStorage.allianceColor) {
        if (localStorage.allianceColor === "blue_alliance") {
            $("body").css("background-color", backgroundColorBlue);
            $("#blue_alliance").addClass('active');
        }
        else if (localStorage.allianceColor === "red_alliance") {
            $("body").css("background-color", backgroundColorRed);
            $("#red_alliance").addClass('active');
        } else {
            $("body").css("background-color", "white");
        }
    } else {
        $("body").css("background-color", "white");
    }

    if (stage === "prematch") {
        $('title').text('Scouting: Prematch');

        try {
            $("#team_number").val(storedVariables.prematch.team_number);
            $("#match_number").val(storedVariables.prematch.match_number);
        } catch (e) {
            $("#team_number").val("");
            $("#match_number").val("");
        }

        $(".alliance-toggle").removeClass('active');
        if (localStorage.allianceColor) {
            $("#" + localStorage.allianceColor).addClass('active');
        }
    }

    else if (stage === "autonomous") {
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

        } catch (e) {
            $("#auto-stacked-yellow-tote-text").text(0);
            $("#auto-moved-yellow-tote-text").text(0);
            $("#auto-acquired-grey-tote-text").text(0);

            // bins
            $("#auto-acquired-step-bin-text").text(0);
            $("#auto-acquired-ground-bin-text").text(0);
            $("#auto-moved-bin-text").text(0);
        }

        if (storedVariables.autonomous) {
            if (storedVariables.autonomous.auto_moved_to_auto_zone) {
                $("#auto_moved_to_alliance_zone").bootstrapSwitch('state', true);
            }
        } else {
            $("#auto_moved_to_alliance_zone").bootstrapSwitch('state', false);
        }
    }

    else if (stage === "teleoperated") {
        $('title').text('Scouting: Teleoperated');

        /*
         Update totals for picked up totes
         */
        $("#tele_picked_up_totes").text(sumNumInDict(storedVariables['teleoperated_picked_up_totes']));

        if (storedVariables['teleoperated_picked_up_totes']) {
            if (storedVariables['teleoperated_picked_up_totes'].lastChange) {
                $("#tele_picked_up_totes_subtract_button").prop('disabled', false);
            } else {
                $("#tele_picked_up_totes_subtract_button").prop('disabled', true);
            }
        }

        if (storedVariables['teleoperated_stacked_totes']) {
            $("#tele_stacked_totes_text").text(storedVariables['teleoperated_stacked_totes'].length);
        } else {
            $("#tele_stacked_totes_text").text(0);
        }

        if (storedVariables['teleoperated_picked_up_bins']) {
            $("#tele_picked_up_bins_text").text(sumNumInDict(storedVariables['teleoperated_picked_up_bins']));
        } else {
            $("#tele_picked_up_bins_text").text(0);
        }

        if (storedVariables['teleoperated_picked_up_bins']) {
            if (storedVariables['teleoperated_picked_up_bins'].lastChange) {
                $("#tele_picked_up_totes_subtract").prop('disabled', false);
            } else {
                $("#tele_picked_up_totes_subtract").prop('disabled', true);
            }
        }

        if (storedVariables['teleoperated_stacked_bins']) {
            $("#tele_stacked_bins_text").text(storedVariables['teleoperated_stacked_bins'].length);
        } else {
            $("#tele_stacked_bins_text").text(0);
        }

        try {
            $("#tele_pushed_litter-text").text(storedVariables['teleoperated'].tele_pushed_litter);
            $("#tele_placed_in_bin_litter-text").text(storedVariables['teleoperated'].tele_placed_in_bin_litter);

        } catch (e) {
            $("#tele_pushed_litter-text").text(0);
            $("#tele_placed_in_bin_litter-text").text(0);
            $("#totes_in_possession").text(0);
        }

        if (storedVariables['teleoperated_fouls_and_other']) {
            if (storedVariables['teleoperated_fouls_and_other'].tele_dead_bot) {
                $("#died_during_match_text").show();
            } else {
                $("#died_during_match_text").hide();
            }
        } else {
            $("#died_during_match_text").hide();
        }

        if (!isNaN(localStorage.totesInPossession)) {
            $("#totes_in_possession").text(localStorage.totesInPossession);
        } else {
            $("#totes_in_possession").text(0);
        }
    }

    else if (stage === "teleoperated_stacked_totes") {
        $("#coop_stack").bootstrapSwitch({
            onText: "YES",
            offText: "NO"
        })

        if (localStorage.totesInPossession) {
            $("#totes_added").find('input[data-height=' + localStorage.totesInPossession + "]").parent('label').addClass('active');
        } else {
            $("#totes_added").find('input').parent('label').removeClass('active');
        }
    }

    else if (stage === "teleoperated_fouls_and_other") {
        /*
         Nothing to speak of
         */
    }

    else if (stage === "postmatch") {
        if(storedVariables['postmatch']) {
            $("#tele_foul_context").val(storedVariables['postmatch'].tele_foul_context);
            $("#tele_private_comments").val(storedVariables['postmatch'].tele_private_comments);
            $("#tele_public_comments").val(storedVariables['postmatch'].tele_public_comments);
        } else {
            $("#tele_foul_context").val("");
            $("#tele_private_comments").val("");
            $("#tele_public_comments").val("");
        }
    }

    else if (stage === "finish") {

        /**
         * HIDE ALL THE THINGS
         */
        $("#in_progress_message").hide();
        $("#in_progress_loading").hide();
        $("#finished_message").hide();
        $("#online_message").hide();
        $("#offline_message").hide();

        if (navigator.onLine) {
            $("#online_message").show();
        } else {
            $("#offline_message").show();
        }

    }
    $("#" + window.location.hash.substring(1)).show();
}

function getMatchData() {
    try {
        return $.parseJSON(localStorage["match" + localStorage.pageMatchID]);
    } catch (e) {
        return {};
    }
}

function setMatchData(stage, name, value) {
    var data = getMatchData();

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
    if (array) {
        $.each(array, function (key, value) {
            if (!isNaN(value)) {
                totalThings += value;
            }
        });
    }

    return totalThings;
}

/*
 universal function that will add/subtract things from labels appended with -text from their respective buttons
 */
$(".btn-add-subtract").click(function () {
    var sender = $(this);
    var name = sender.data('name');

    var target = $("#" + name + "-text");

    if (target.data('max')) {
        var max = parseInt(target.data('max'));
    }

    if (sender.data('operation') === "add") {
        if (typeof max !== 'undefined' && parseInt(target.text()) < max || typeof max === 'undefined') {
            target.text(parseInt(target.text()) + 1);
        }
    }

    else if (sender.data('operation' == "subtract")) {
        if (parseInt(target.text()) > 0) {
            target.text(parseInt(target.text()) - 1);
        }
    }
});

var xPosition, yPosition;
/*
 Get the relative coordinates from start image
 */
$("#auto_start_image").click(function (event) {
    var image = $(this);

    xPosition = (event.pageX - image.offset().left) / image.width();
    yPosition = (event.pageY - image.offset().top) / image.height();

    saveAndContinue('autonomous_starting_location', 'autonomous');
});

/*
 Get the relative coordinates from teleop location image
 */
$("#teleoperated_stacked_totes_image").click(function (event) {
    var image = $(this);

    xPosition = (event.pageX - image.offset().left) / image.width();
    yPosition = (event.pageY - image.offset().top) / image.height();

    saveAndContinue('teleoperated_stacked_totes_location', 'teleoperated');
});

/*
 Undo last thing from tele_picked_up_totes
 */

$("#tele_picked_up_totes_subtract_button").click(function () {
    var variables = getMatchData()['teleoperated_picked_up_totes'];

    var lastChange = variables.lastChange;

    /*
     only subtract if it exists and is > 0 (otherwise errors)
     */

    if (variables.lastChange) {
        if (variables[lastChange] > 0) {
            setMatchData("teleoperated_picked_up_totes", lastChange, variables[lastChange] - 1);
            setMatchData("teleoperated_picked_up_totes", 'lastChange', undefined);

            $("#tele_picked_up_totes_subtract_button").prop('disabled', true);
        }
    }

    $("#tele_picked_up_totes").text(sumNumInDict(getMatchData()['teleoperated_picked_up_totes']));

    if(localStorage.totesInPossession) {
        if(localStorage.totesInPossession > 0) {
            localStorage.totesInPossession = localStorage.totesInPossession - 1;
        } else {
            localStorage.totesInPossession = 0;
        }
    }

    $("#totes_in_possession").text(localStorage.totesInPossession);

});

/*
 Undo last thing from tele_picked_up_bins
 */

$("#tele_picked_up_bins_subtract").click(function () {
    var variables = getMatchData()['teleoperated_picked_up_bins'];

    var lastChange = variables.lastChange;

    /*
     only subtract if it exists and is > 0 (otherwise errors)
     */

    if (variables.lastChange) {
        if (variables[lastChange] > 0) {
            setMatchData("teleoperated_picked_up_bins", lastChange, variables[lastChange] - 1);
            setMatchData("teleoperated_picked_up_bins", 'lastChange', undefined);

            $("#tele_picked_up_bins_subtract").prop('disabled', true);
        }
    }

    $("#tele_picked_up_bins_text").text(sumNumInDict(getMatchData()['teleoperated_picked_up_bins']));

});

$("#tele_stacked_totes_subtract").click(function () {
    var data = getMatchData()['teleoperated_stacked_totes'];


    var lastIndex = data[data.length - 1];

    if (lastIndex) {
        data = data.slice(0, -1);

        var subtract = localStorage.totesInPossession - lastIndex.totes_added;

        /*
         Can't be < 0
         */
        if (subtract > 0) {
            localStorage.totesInPossession = subtract;
        } else {
            localStorage.totesInPossession = 0;
        }
        $("#totes_in_possession").text(localStorage.totesInPossession);

        setMatchDataArray('teleoperated_stacked_totes', data);

        $("#tele_stacked_totes_text").text(data.length);
    }
});

$("#tele_stacked_bins_subtract").click(function () {
    var data = getMatchData()['teleoperated_stacked_bins'];

    data = data.slice(0, -1);

    setMatchDataArray('teleoperated_stacked_bins', data);

    $("#tele_stacked_bins_text").text(data.length);
});

/*
 Clarify coloration for tote stack height
 */
$(".start-height-group-wrapper").click(function () {
    var startHeight = $(this).find('input').data('height');
    var maxHeight = 6 - startHeight;


    $.each($("[name=totes_added_group]"), function () {
        var sender = $(this);

        if (sender.data('height') > maxHeight) {
            sender.parent('label').attr('disabled', true);
        } else {
            sender.parent('label').attr('disabled', false);
        }

    })

});

function getPendingMatches() {
    var pendingMatches = [];

    for (var i = 0; ; i++) {
        if (localStorage["match" + i.toString()]) {
            pendingMatches.push($.parseJSON(localStorage["match" + i.toString()]));
        }
        else {
            break;
        }
    }

    return pendingMatches;
}

function clearPendingMatches() {
    for (var i = 0; ; i++) {
        if (localStorage["match" + i.toString()]) {
            localStorage.removeItem("match" + i.toString());
        }
        else {
            break;
        }
    }
}

function discardData() {
    if (confirm("Are you sure? This will delete your data IRREVERSIBLY!")) {
        if (prompt("Enter the scouted team's number to confirm your choice:") === getMatchData().prematch.team_number.toString()) {
            localStorage.removeItem("match" + localStorage.pageMatchID);
            setupNewMatch();
            $("#offline_message").hide();
            $("#online_message").hide();
            $("#in_progress_message").hide();
            $("#finished_message").show();
        } else {
            showErrorMessages(['Match deletion cancelled.'], false);
        }
    }
}

$("button[data-name=auto-moved-bin]").click(function() {
    var sum = parseInt($("#auto-acquired-step-bin-text").text()) + parseInt($("#auto-acquired-ground-bin-text").text());

    var thisSum = parseInt($("#auto-moved-bin-text").text());
    console.log(sum + " " + thisSum);

    if(thisSum > sum) {
        $("#auto-moved-bin-text").text(parseInt($("#auto-moved-bin-text").text()) - 1);
    }
})