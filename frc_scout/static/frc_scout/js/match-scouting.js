//var backgroundColorRed = "rgb(255, 158, 158)";
var backgroundColorRed = "rgba(255, 131, 131, 0.862745)";
var backgroundColorBlue = "rgb(199, 208, 255)";

var schedule = null;

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

    $("input[type=checkbox]").bootstrapSwitch({
        'size': 'large',
        'onText': "YES",
        'offText': "NO"

    });

    if(localStorage.eventSchedule !== null && localStorage.eventSchedule !== undefined) {
        schedule = $.parseJSON(localStorage.eventSchedule);
    }
});

/*
 This will update the background color of the page based on the alliance selection
 Alliance colors are not stored permanently; they are only used to help scouts remember who they're scouting
 */
$(".alliance-toggle").on('change click', function() {
    var id = this.id;

    var child = $(this).find("option:selected");

    if(id === "blue_alliance" || child.data('color') === "blue") {
        $("body").css("background-color", backgroundColorBlue);
        localStorage.allianceColor = 'blue_alliance';
    }

    else if(id === "red_alliance" || child.data('color') === "red") {
        $("body").css("background-color", backgroundColorRed);
        localStorage.allianceColor = 'red_alliance';
    }

    if(child.val()) {
        setMatchData('prematch', 'team_number', child.val().substr(3));
    }

    if(getMatchData().prematch) {
        if (getMatchData().prematch.team_number) {
            $(".team-number").text(": " + getMatchData().prematch.team_number);
        }
    }

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

    localStorage.removeItem('allianceColor');
    localStorage.removeItem('totesInPossession');

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
    var stageVariables;

    /**
     * FROM STAGES
     **/

    if(fromStage === "prematch") {
        var teamNumber;

        if($("#team_number").is(':visible')) {
            teamNumber = parseInt($("#team_number").val());
        } else {
            teamNumber = parseInt($("#select_team_number_select").val().substr(3));
        }

        var matchNumber = parseInt($("#match_number").val());

        var override = false;

        if(sender) {
            if(sender.id === "override") {
                override = true;
            }
        }

        if(isNaN(teamNumber) || teamNumber < 1) {
            errorMessage.push("Team number is required and must be a number of one or greater.");
        } else {
            if(localStorage.teamsAtEvent !== undefined) {
                var teams = $.parseJSON(localStorage.teamsAtEvent);
                if(!override) {
                    if(teams.length > 0) {
                        var exists = false;
                        $.each(teams, function(key, value) {
                            if(value['team_number'] === teamNumber) {
                                exists = true;
                                return;
                            }
                        });

                        if(!exists) {
                            errorMessage.push("That team is not present at this event. <button class='btn btn-defaul btn-sm' id='override' onclick='saveAndContinue(\"prematch\", \"autonomous_starting_location\", this);'>Override.</button>");
                        }
                    }
                }
            }
        }



        if(isNaN(matchNumber) || matchNumber < 1) {
            errorMessage.push("Match number is required and must be a number of one or greater.");
        } else if(matchNumber > 150) {
            errorMessage.push("Match number cannot be greater than 150.");
        }

        if(localStorage.allianceColor === null || localStorage.allianceColor === undefined) {
            errorMessage.push("Alliance color is required.");
        }

        stageVariables = {
            team_number: teamNumber,
            match_number: matchNumber
        };


        if(sender) {
            if (sender.id === "no_show") {
                if (confirm("Click OK to confirm that this team was not present for the match."));

                stageVariables['no_show'] = true;
                setMatchDataArray('postmatch', {});
                setMatchData('postmatch', 'scouting_complete', true);
            }
        }
    }

    else if(fromStage === "autonomous_starting_location") {
        stageVariables = {
            auto_start_x: xPosition,
            auto_start_y: yPosition
        };

        if(!confirm("Confirm autonomous starting location.")) {
            return false;
        }
    }

    else if(fromStage === "autonomous") {

        // totes
        var autoStackedYellowTotes = parseInt($("#auto-stacked-yellow-tote-text").text());
        var autoMovedYellowTotes = parseInt($("#auto-moved-yellow-tote-text").text());
        var autoAcquiredGreyTotes = parseInt($("#auto-acquired-grey-tote-text").text());

        if(storedVariables['autonomous']) {
            stageVariables = storedVariables['autonomous'];
        } else {
            stageVariables = {};
        }

        stageVariables['auto_yellow_stacked_totes'] = autoStackedYellowTotes;
        stageVariables['auto_yellow_moved_totes'] = autoMovedYellowTotes;
        stageVariables['auto_grey_acquired_totes'] = autoAcquiredGreyTotes;
        stageVariables['auto_moved_to_auto_zone'] = $("#auto_moved_to_alliance_zone").bootstrapSwitch('state');
    }

    else if(fromStage === "autonomous_containers_unscored" || fromStage === "autonomous_containers_scored") {
        var id = sender.id;

        var autoVariables = storedVariables['autonomous'];

        // assume 1 if nothing else because they obviously did something to get here
        var numberOfThings = 1;

        // if there's already data then set it to that + 1
        if(autoVariables[id]) {
            numberOfThings = autoVariables[id] + 1;
        }

        stageVariables = autoVariables;

        stageVariables[id] = numberOfThings;

        /*
         UNDOING THINGS
         */

        var scoredContainers = 0;

        var thingToUndo = "autonomous_containers_unscored";

        if(fromStage === "autonomous_containers_scored") {
            if(autoVariables['auto_moved_containers']) {
                scoredContainers = autoVariables['auto_moved_containers'];
            }

            console.log("from scored");

            thingToUndo = "autonomous_containers_scored";
            stageVariables['auto_moved_containers'] = scoredContainers + 1;
        }

        var newThingsToUndo;

        if(autoVariables[thingToUndo]) {
            newThingsToUndo = autoVariables[thingToUndo];
        } else {
            newThingsToUndo = [];
        }

        newThingsToUndo.push(id);

        stageVariables[thingToUndo] = newThingsToUndo;

        // hacky
        fromStage = "autonomous";
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



        if(!storedVariables['teleoperated_picked_up_totes'].undoPickedUpTotes) {
            storedVariables['teleoperated_picked_up_totes'].undoPickedUpTotes = [
                id,
            ]
        } else {
            storedVariables['teleoperated_picked_up_totes'].undoPickedUpTotes.push(id);
        }

        var totalThings = sumNumInDict(storedVariables['teleoperated_picked_up_totes']);

        $("#tele_picked_up_totes").text(totalThings);

        stageVariables = storedVariables['teleoperated_picked_up_totes'];


        /*
         Update totes in possession
         */

        console.log('starting');

        if(!isNaN(localStorage.totesInPossession)) {
            var currentTotes = localStorage.totesInPossession;
            localStorage.totesInPossession = parseInt(currentTotes) + 1;
        } else {
            localStorage.totesInPossession = 1;
        }

        $("#totes_in_possession").text(localStorage.totesInPossession);
        updatePossessionColor();
    }

    else if(fromStage === "teleoperated_stacked_totes") {
        var startHeight = $("#start_height").find('.active > input').data('height');
        var endHeight = $("#totes_added").find('.active > input').data('height');

        // $("#start_height").find('.active').removeClass('active');
        // $("#totes_added").find('.active').removeClass('active');

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
                totes_added: endHeight
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

        console.log("COOP STACK = " + coopStack);

        storedVariables['teleoperated_stacked_totes'][latestIndex].coop_stack = coopStack;

        coopStack = false;

        var removedFromPossession = storedVariables['teleoperated_stacked_totes'][latestIndex].totes_added;

        console.log(removedFromPossession);

        var final = localStorage.totesInPossession - removedFromPossession;

        if(final >= 0) {
            localStorage.totesInPossession  = final;
        } else {
            localStorage.totesInPossession = 0;
        }

        $("#totes_in_possession").text(localStorage.totesInPossession);
        updatePossessionColor();

        stageVariables = storedVariables['teleoperated_stacked_totes'];

        // hacky way to make the right variable in localStorage be changed
        fromStage = "teleoperated_stacked_totes";
    }

    else if(fromStage === "teleoperated_picked_up_containers") {
        if(!storedVariables['teleoperated_picked_up_containers']) {
            storedVariables['teleoperated_picked_up_containers'] = {
                tele_picked_up_sideways_containers: 0,
                tele_picked_up_upright_containers: 0,
                tele_picked_up_center_step_containers: 0
            };
        }

        var id = sender.id;

        storedVariables['teleoperated_picked_up_containers'][id] += 1;

        /*
         For undoing things
         */


        if(!storedVariables['teleoperated_picked_up_containers'].undoPickedUpContainers) {
            storedVariables['teleoperated_picked_up_containers'].undoPickedUpContainers = [
                id,
            ]
        } else {
            storedVariables['teleoperated_picked_up_containers'].undoPickedUpContainers.push(id);
        }

        storedVariables['teleoperated_picked_up_containers'].lastChange = id;


        var totalThings = sumNumInDict(storedVariables['teleoperated_picked_up_containers']);

        $("#tele_picked_up_containers_text").text(totalThings);

        stageVariables = storedVariables['teleoperated_picked_up_containers'];

        /*
         For undoing things
         */
        storedVariables['teleoperated_picked_up_containers'].lastChange = id;

    }

    else if(fromStage === "teleoperated_stacked_containers") {
        var startHeight = $("#container_stack_height").find('.active > input').data('height');

        $("#container_stack_height").find('.active').removeClass('active');

        if(isNaN(startHeight)) {
            errorMessage.push("Start height is required.");
        } else {
            /*
             re-append all past arrays to be re-committed to localStorage
             */
            if(storedVariables['teleoperated_stacked_containers']) {
                stageVariables = storedVariables['teleoperated_stacked_containers'];
            } else {
                stageVariables = [];
            }

            /*
             then add our current one
             */
            stageVariables.push(startHeight);

            $("#tele_stacked_containers_text").text(stageVariables.length);

        }
    }

    else if(fromStage === "teleoperated") {
        var pushedLitter = parseInt($("#tele_pushed_litter-text").text());
        var placedInContainerLitter = parseInt($("#tele_placed_in_container_litter-text").text());

        if(isNaN(pushedLitter) || isNaN(placedInContainerLitter)) {
            errorMessage.push("This error should never occur unless you mess with the page, try refreshing it ;)");
        } else {
            stageVariables = {
                tele_pushed_litter: pushedLitter,
                tele_placed_in_container_litter: placedInContainerLitter
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
                'tele_container_fell_off': 0
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
        var matchFinalScore = parseInt($("#match_final_score").val());

        if(isNaN(matchFinalScore) && toStage !== "teleoperated") {
            errorMessage.push("Final alliance score is required.");
        } else if((parseInt(matchFinalScore) < 0 || parseInt(matchFinalScore) > 1000) && toStage !== "teleoperated") {
            errorMessage.push("Final alliance score must be greater than 0 and less than 1000.");
        }

        stageVariables = {
            match_final_score: matchFinalScore,
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

// push it back to localStorage
    setMatchDataArray(fromStage, stageVariables);

// change hash triggering the next stage to show
    window.location.hash = toStage;
}

function discardAndChangeStage(fromStage, toStage) {

    if(fromStage === 'teleoperated_stacked_totes_location') {
        var data = getMatchData()['teleoperated_stacked_totes'];
        data.pop();
        setMatchDataArray('teleoperated_stacked_totes', data);
    }

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

    window.scrollTo(0, 1);
}

function submitData() {
    var pendingMatches = getPendingMatches();

    $("#online_message").hide();
    $("#in_progress_message").show();
    $("#submit_pending").button('loading');

    $.ajax({
        url: '/scouting/match/submit/',
        method: "POST",
        data: {
            csrfmiddlewaretoken: $.cookie('csrftoken'),
            data: JSON.stringify(pendingMatches)
        },
        success: function(response) {
            clearPendingMatches();

            $("#submit_pending").html("<span class='glyphicon glyphicon-saved'></span>&nbsp; Data submitted successfully.");
            window.setTimeout(function() {
                $("#submit_pending").fadeOut(500);
            }, 2000);

            $("#saved").hide();
            $("#submitted").show();
            $("#deleted").hide()
            $("#in_progress_loading").fadeIn(1000);

            window.setTimeout(function() {
                setupNewMatch();
                $("#in_progress_message").hide();
                $("#finished_message").show();

                if(response) {
                    console.log(response);

                    var json = $.parseJSON(response);
                    $("#submit_errors").show();

                    $.each(json, function(key, value) {
                        $("#submit_errors_list").append('<li>Team: ' + value['team_number'] + ", Match: " + value['match_number'] + "</li>");
                    })
                }

            }, 2000);

        },
        error: function() {
            showErrorMessages(["Data submission failed."], false);
            $("#in_progress_message").hide();
            $("#online_message").hide();
            $("#offline_message").show();
            $("#submit_pending").button('reset');
            $("#submit_pending").html("<span class='glyphicon glyphicon-remove'></span>&nbsp; Data submission failed, please try again later.");
        }
    });
}

function saveDataOffline() {
    setupNewMatch();
    $("#offline_message").hide();
    $("#submitted").hide();
    $("#in_progress_message").hide();
    $("#finished_message").show();
    $("#saved").show();
    $("#deleted").hide();
}


function openStage(stage) {
    /**
     * TO STAGES
     **/

    $("#alert").hide();

    if (!getMatchData()) {
        window.location.hash = "prematch";
    }

    if (getMatchData()) {
        if ($.isEmptyObject(getMatchData()) || getMatchData() === undefined || getMatchData() === null) {
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

        $("#match_number").trigger('keyup');

        if ($("#select_team_number").is(':visible')) {
            console.log('runnnning');
            $("#select_team_number_select").find('label > span:contains(' + storedVariables.prematch.team_number + ')').parent().addClass('active');
        } else {
            console.log('niooooo');
        }

        $(".alliance-toggle").removeClass('active');
        if (localStorage.allianceColor) {
            $("#" + localStorage.allianceColor).addClass('active');
        }

        if (getPendingMatches().length !== 0) {
            $("#submit_pending").show();
            $("#submit_pending").text("Submit pending matches (" + getPendingMatches().length + ")")
        } else {
            $("#submit_pending").hide();
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

            // containers


        } catch (e) {
            $("#auto-stacked-yellow-tote-text").text(0);
            $("#auto-moved-yellow-tote-text").text(0);
            $("#auto-acquired-grey-tote-text").text(0);

            // containers
            $("#auto_unscored_container_text").text(0);
            $("#auto_scored_container_text").text(0);
        }


        if (storedVariables.autonomous) {
            if (storedVariables.autonomous.auto_moved_to_auto_zone) {
                $("#auto_moved_to_alliance_zone").bootstrapSwitch('state', true);
            } else {
                $("#auto_moved_to_alliance_zone").bootstrapSwitch('state', false);
            }


            if (storedVariables.autonomous.autonomous_containers_unscored) {
                $("#auto_unscored_container_text").text(storedVariables['autonomous']['autonomous_containers_unscored'].length);
            } else {
                $("#auto_unscored_container_text").text(0);
            }
            if (storedVariables.autonomous.autonomous_containers_scored) {
                $("#auto_scored_container_text").text(storedVariables['autonomous']['autonomous_containers_scored'].length);
            } else {
                $("#auto_scored_container_text").text(0);
            }
        } else {
            $("#auto_moved_to_alliance_zone").bootstrapSwitch('state', false);
        }
    }

    else if(stage === "autonomous_containers_unscored" || stage === "autonomous_containers_scored") {
        if(storedVariables['autonomous']) {
            var autoVariables = storedVariables['autonomous'];
            if(autoVariables['auto_ground_acquired_containers']) {
                if(parseInt(autoVariables['auto_ground_acquired_containers']) >= 3) {
                    $(".auto_ground_acquired_containers").attr('disabled', true);
                } else {
                    $(".auto_ground_acquired_containers").attr('disabled', false);
                }
            }

            if(autoVariables['auto_step_center_acquired_containers']) {
                if(parseInt(autoVariables['auto_step_center_acquired_containers']) >= 4) {
                    $(".auto_step_center_acquired_containers").attr('disabled', true);
                } else {
                    $(".auto_step_center_acquired_containers").attr('disabled', false);
                }
            }
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

        var pickedUpContainers = 0;

        if (storedVariables['teleoperated_picked_up_containers']) {
            pickedUpContainers = sumNumInDict(storedVariables['teleoperated_picked_up_containers'])
            $("#tele_picked_up_containers_text").text(pickedUpContainers);
        } else {
            $("#tele_picked_up_containers_text").text(0);
        }

        if (pickedUpContainers < 1) {
            $(".tele-stacked-containers").attr('disabled', true);
        } else {
            $(".tele-stacked-containers").attr('disabled', false);
        }

        if (storedVariables['teleoperated_picked_up_containers']) {
            if (storedVariables['teleoperated_picked_up_containers'].lastChange) {
                $("#tele_picked_up_totes_subtract").prop('disabled', false);
            } else {
                $("#tele_picked_up_totes_subtract").prop('disabled', true);
            }
        }

        if (storedVariables['teleoperated_stacked_containers']) {
            $("#tele_stacked_containers_text").text(storedVariables['teleoperated_stacked_containers'].length);
        } else {
            $("#tele_stacked_containers_text").text(0);
        }

        try {
            $("#tele_pushed_litter-text").text(storedVariables['teleoperated'].tele_pushed_litter);
            $("#tele_placed_in_container_litter-text").text(storedVariables['teleoperated'].tele_placed_in_container_litter);

        } catch (e) {
            $("#tele_pushed_litter-text").text(0);
            $("#tele_placed_in_container_litter-text").text(0);
            $("#totes_in_possession").text(0);
            updatePossessionColor();
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
            updatePossessionColor();
            if (parseInt(localStorage.totesInPossession) > 0) {
                $("#tele_stacked_totes_button").prop('disabled', false);
            } else {
                $("#tele_stacked_totes_button").prop('disabled', true);
            }
        } else {
            $("#totes_in_possession").text(0);
            $("#tele_stacked_totes_button").prop('disabled', true);

            updatePossessionColor();
        }
    }


    else if (stage === "teleoperated_stacked_totes") {

        $("#totes_added").find('input').parent('label').attr('disabled', false);

        $("#start_height").find('input').parent('label').removeClass('active');
        $("#totes_added").find('input').parent('label').removeClass('active');


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
        $('title').text('Scouting: Postmatch');
        if(storedVariables['postmatch']) {
            $("#tele_foul_context").val(storedVariables['postmatch'].tele_foul_context);
            $("#tele_private_comments").val(storedVariables['postmatch'].tele_private_comments);
            $("#tele_public_comments").val(storedVariables['postmatch'].tele_public_comments);
            $("#match_final_score").val(storedVariables['postmatch'].match_final_score);
        } else {
            $("#tele_foul_context").val("");
            $("#tele_private_comments").val("");
            $("#tele_public_comments").val("");
            $("#match_final_score").val("");
        }
    }

    else if (stage === "finish") {
        $('title').text('Scouting: Finish');

        /**
         * HIDE ALL THE THINGS
         */
        $("#in_progress_message").hide();
        $("#in_progress_loading").hide();
        $("#finished_message").hide();
        $("#online_message").hide();
        $("#offline_message").hide();
        $("#submit_errors").hide();
        $("#submit_errors_list").text("");

        if (navigator.onLine) {
            $("#online_message").show();
        } else {
            $("#offline_message").show();
        }


        if($("#practice_scouting").val() === "true") {
            setMatchData('postmatch', 'practice_scouting', true);
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

    else if (sender.data('operation')  === "subtract") {
        console.log(target.text());
        if (parseInt(target.text()) > 0) {
            if(sender.data('affect') === "moved_to_zone") {
                if(parseInt($("#auto-moved-container-text").text()) > 0) {
                    $("#auto-moved-container-text").text(parseInt($("#auto-moved-container-text").text()) - 1);
                }
            }
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

    if((yPosition > 0.18 && yPosition < 0.4) || yPosition > 0.62) {
        saveAndContinue('autonomous_starting_location', 'autonomous');
    } else {
        showErrorMessages(["Invalid starting location."], false);
    }
});

/*
 Get the relative coordinates from teleop location image
 */

var coopStack = false;

$("#teleoperated_stacked_totes_image").click(function (event) {
    var image = $(this);

    xPosition = (event.pageX - image.offset().left) / image.width();
    yPosition = (event.pageY - image.offset().top) / image.height();

    if(yPosition < 0.09 || (yPosition > 0.3 && yPosition < 0.4 && xPosition < 0.58) || (yPosition > 0.63 && yPosition < 0.73 && xPosition > 0.42)) {
        if(yPosition < 0.09) {
            coopStack = true;
        }
        saveAndContinue('teleoperated_stacked_totes_location', 'teleoperated');
    } else {
        showErrorMessages(["Invalid tote stack location."], false);
    }
});

/*
 Undo last thing from tele_picked_up_totes
 */

$("#tele_picked_up_totes_subtract_button").click(function () {
    var variables = getMatchData()['teleoperated_picked_up_totes'];


    var undoableThings = variables.undoPickedUpTotes;

    /*
     only subtract if it exists and is > 0 (otherwise errors)
     */

    if (undoableThings) {
        var lastThing = undoableThings.pop();
        if(undoableThings.length >= 0 && sumNumInDict(variables) > 0) {
            setMatchData("teleoperated_picked_up_totes", lastThing, variables[lastThing] - 1);
            setMatchData("teleoperated_picked_up_totes", 'undoPickedUpTotes', undoableThings);
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
    updatePossessionColor();
    updateDisabledStackedTotes();

});

/*
 Undo last thing from tele_picked_up_containers
 */

$("#tele_picked_up_containers_subtract").click(function () {
    var variables = getMatchData()['teleoperated_picked_up_containers'];

    var undoableThings = variables.undoPickedUpContainers;

    /*
     only subtract if it exists and is > 0 (otherwise errors)
     */

    if (undoableThings) {
        var lastThing = undoableThings.pop();
        if(undoableThings.length >= 0 && sumNumInDict(variables) > 0) {
            setMatchData("teleoperated_picked_up_containers", lastThing, variables[lastThing] - 1);
            setMatchData("teleoperated_picked_up_containers", 'undoPickedUpContainers', undoableThings);
        }
    }

    var newTotal = sumNumInDict(getMatchData()['teleoperated_picked_up_containers']);

    $("#tele_picked_up_containers_text").text(newTotal);

    if(newTotal < 1) {
        $(".tele-stacked-containers").attr('disabled', true);
    } else {
        $(".tele-stacked-containers").attr('disabled', false);
    }
});

$("#tele_stacked_totes_subtract").click(function () {
    var data = getMatchData()['teleoperated_stacked_totes'];


    var lastIndex = data[data.length - 1];

    if (lastIndex) {
        data = data.slice(0, -1);

        var subtract = parseInt(localStorage.totesInPossession) + lastIndex.totes_added;

        /*
         Can't be < 0
         */
        if (subtract > 0) {
            localStorage.totesInPossession = subtract;
        } else {
            localStorage.totesInPossession = 0;
        }
        $("#totes_in_possession").text(localStorage.totesInPossession);
        updatePossessionColor();

        setMatchDataArray('teleoperated_stacked_totes', data);

        updateDisabledStackedTotes();

        $("#tele_stacked_totes_text").text(data.length);
    }
});

$("#tele_stacked_containers_subtract").click(function () {
    var data = getMatchData()['teleoperated_stacked_containers'];

    data = data.slice(0, -1);

    setMatchDataArray('teleoperated_stacked_containers', data);

    $("#tele_stacked_containers_text").text(data.length);
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
            sender.parent('label').removeClass('active');
        } else {
            sender.parent('label').attr('disabled', false);
        }

    })
});

function getPendingMatches() {
    var pendingMatches = [];

    for (var i = 0; ; i++) {
        if (localStorage["match" + i.toString()]) {
            var match = $.parseJSON(localStorage["match" + i.toString()]);

            if(match.postmatch) {
                if(match.postmatch.scouting_complete === true) {
                    pendingMatches.push(match);
                }
            }
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
            $("#submitted").hide();
            $("#saved").hide();
            $("#deleted").show()
            $("#finished_message").show();
        } else {
            showErrorMessages(['Match deletion cancelled.'], false);
        }
    }
}

$("button[data-name=auto-moved-container]").click(function() {
    var sum = parseInt($("#auto-acquired-step-container-text").text()) + parseInt($("#auto-acquired-ground-container-text").text());

    var thisSum = parseInt($("#auto-moved-container-text").text());
    console.log(sum + " " + thisSum);

    if(thisSum > sum) {
        $("#auto-moved-container-text").text(parseInt($("#auto-moved-container-text").text()) - 1);
    }
})

function updatePossessionColor() {
    var v = parseInt($("#totes_in_possession").text());

    if(v >= 6) {
        $("#totes_in_possession_wrapper").css('color', 'firebrick');
    } else {
        $("#totes_in_possession_wrapper").css('color', '#444444');
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
            $("#select_team_number_select").append("<option style='color:red;' class='d' data-color='red' value='" + v + "'>Red " + onetwothree[index] + ": " + v.substr(3) + "</option>");
            index++;
        });

        index = 0;

        $.each(blue, function(k, v) {
            $("#select_team_number_select").append("<option style='color:blue;' class='d' data-color='blue' value='" + v + "'>Blue " + onetwothree[index] + ": " + v.substr(3) + "</option>");
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

function updateDisabledStackedTotes() {
    if (!isNaN(localStorage.totesInPossession)) {
        $("#totes_in_possession").text(localStorage.totesInPossession);
        updatePossessionColor();
        if(parseInt(localStorage.totesInPossession) > 0) {
            $("#tele_stacked_totes_button").prop('disabled', false);
        } else {
            $("#tele_stacked_totes_button").prop('disabled', true);
        }
    } else {
        $("#totes_in_possession").text(0);
        $("#tele_stacked_totes_button").prop('disabled', true);

        updatePossessionColor();
    }
}

$(".auto-container-undo").click(function() {
    var sender = $(this);

    var affected = sender.data('affect');

    if(getMatchData()['autonomous'][affected]) {
        var affectedArray = getMatchData()['autonomous'][affected];

        if(affectedArray.length > 0) {
            var pop = affectedArray.pop();
            setMatchData('autonomous', affected, affectedArray);
            $("[data-field=" + affected).text(affectedArray.length);

            setMatchData('autonomous', pop, getMatchData()['autonomous'][pop] - 1);
        }
    }
});