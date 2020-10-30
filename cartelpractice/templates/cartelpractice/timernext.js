        var div_timer = $("div.otree-timer");
        var span_timer = div_timer.find("p").children("span");
        var span_timeleft = $(".otree-timer__time-left");
        var span_timeglyph = $(".glyphicon.glyphicon-time");
        var p_old = div_timer.find("p");
        var p_new = $("<p></p>");

        p_new.append(span_timer);
        p_old.remove();
        div_timer.append(p_new);
        div_timer.show();

        $(function () {
            $('.otree-timer__time-left').off('finish.countdown');
            $('.otree-timer__time-left').on('finish.countdown', function(event) {
                $('input[type="text"]').prop("disabled", true);
                div_timer.css("background", "#b92c28");
                span_timeleft.css("color", "white");
                span_timeglyph.css("color", "white");
                span_timeleft.text("0:00");
                setTimeout(function() {
                    $("button:not(.report-button)").click();
                }, 2000);
            });
        });
