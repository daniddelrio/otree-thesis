        //var div_timer = $("div.otree-timer");
        var div_timer = $('<div class="otree-timer alert alert-warning" style="display: block; margin-right: 2rem;"><p><span style="font-weight: bold"><span class="glyphicon glyphicon-time"></span>&nbsp;<span class="otree-timer__time-left">0:<span id="timer-seconds">{{ seconds_before_flagging }}</span></span></span></p></div>');
        $("form").parent().eq(0).prepend(div_timer);

        var span_timer = div_timer.find("p").children("span");
        var span_timeleft = $(".otree-timer__time-left");
        var span_timeglyph = $(".glyphicon.glyphicon-time");
        var span_timerseconds = $("#timer-seconds");
        var p_old = div_timer.find("p");
        var p_new = $("<p></p>");

        var color = "#b92c28";
        var seconds = {{ seconds_before_flagging }};

        var pad = function(num, size) {
            var s = num+"";
            while (s.length < size) s = "0" + s;
            return s;
        }

        p_new.append(span_timer);
        p_old.remove();
        div_timer.append(p_new);
        div_timer.show();

        var timerDone = function() {
            div_timer.css("background", color);
            span_timeleft.css("color", "white");
            span_timeglyph.css("color", "white");
            span_timeleft.text("Please decide now.");

            setInterval(function() {
                if (color === "#b92c28") {
                    color = "orange";
                } else {
                    color = "#b92c28";
                }
                div_timer.css("background", color);
            }, 500);
        };

        var timerTick = function() {
            seconds -= 1;
            span_timerseconds.text(pad(seconds, 2));

            if (seconds == 0) {
                timerDone();
            } else {
                setTimeout(timerTick, 1000);
            }
        };

        $('.otree-timer__time-left').off('finish.countdown');

        setTimeout(timerTick, 1000);
