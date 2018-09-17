/**
 * Created by adagio on 2018-09-04.
 */

/* SVM implementation */

//##################################################################

$(function () {

    var textBlock = $('#text');
    var resultBlock = $('#result');

    $('#check-btn').click(check);
    $('#clear-btn').click(clear);

    function check() {
        var text = textBlock.val();
        if (text === '') {
            return;
        }

        $.ajax({
            url: '/svm/check',
            data: {
                text: text
            },
            success: function (data) {
                console.log(data);
                setResult(data);
            },
            error: function () {
                console.error('Cannot check text')
            }
        });
    }

    function setResult(value) {
        //resultBlock.removeClass('placeholder');

        var html = '<dl><dt>Fixed difficulty level</dt><dd>';
        console.log(value.found);
        for (var i=0; i<value.found.length; i++) {
            if (i===0) {
                html +=  value.found[i][0] + '(' + value.found[i][1] + ')';
            } else {
                html +=  ', ' + value.found[i][0] + '(' + value.found[i][1] + ')';
            }
        }
        html += '</dd>';

        console.log(html);

        html += '<dt>Estimated difficulty level</dt><dd>';
        console.log(value.not_found);
        for (i=0; i<value.not_found.length; i++) {
            if (i===0) {
                html +=  value.not_found[i][0] + '(' + value.not_found[i][1] + ')';
            } else {
                html +=  ', ' + value.not_found[i][0] + '(' + value.not_found[i][1] + ')';
            }
        }
        html += '</dd></dl>';

        resultBlock.html(html);
    }

    function clear() {
        textBlock.val('');
        resultBlock.empty();
    }
});