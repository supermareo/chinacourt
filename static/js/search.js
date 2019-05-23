$('#search_input').bind('keypress', function (event) {
    if (event.keyCode === 13) {
        search();
    }
});
$('#search_btn').click(function () {
    search();
});

function search() {
    var question = $('#search_input').val();
    if (question === '') {
        new $.flavr({
            content: '请先输入你的问题',
            autoclose: true,
            timeout: 1000 /* Default timeout is 3 seconds */
        });
        return
    }
    doSearch(question)
}

var totalCount = 0;
var questionList = [];
var totalPages = 0;
var curPage = 1;

function doSearch(question) {
    console.log('do search', question);
    questionList = [];
    $.ajax({
        url: '/search/' + question,
        beforeSend: function (xhr) {
            console.log('before send');
            $('#empty-content').hide();
            $('#content').hide();
            $('#loading').show();
        },
        success: function (result, status, xhr) {
            console.log('success', result);
            questionList = result['data'];
            refreshQuestionList();
        },
        error: function (xhr, status, error) {
            console.log('error', status, error, xhr)
        },
        complete: function (xhr, status) {
            console.log('complete', status, xhr);
            $('#loading').hide();
        }
    });
}

function refreshQuestionList() {
    totalCount = questionList.length;
    console.log('total length', length);
    if (totalCount === 0) {
        $('#content').hide();
        $('#empty-content').show();
        return false;
    } else {
        $('#empty-content').hide();
        $('#content').show();
    }

    totalPages = Math.ceil(totalCount / 7);
    curPage = 0;
    showPage(curPage)
}

function showPage(pageNum) {
    curPage = pageNum;
    if (curPage < 0 || curPage >= totalPages) {
        return
    }
    //清空列表
    $('#question-list').children().remove();
    var start = pageNum * 7;
    var end = start + 7;
    end = end > totalCount ? totalCount : end;
    for (var i = start; i < end; i++) {
        var q = questionList[i];
        var question = q['sentence'];
        $('#question-list').append('<li onclick="showDetail(\'' + question + '\')">' + question + '</li>');
    }
    var preEnable = curPage === 0 ? '' : 'enable';
    var nextEnable = curPage === totalPages - 1 ? '' : 'enable';
    var preEnabled = preEnable === 'enable' ? '' : 'disabled';
    var nextEnabled = nextEnable === 'enable' ? '' : 'disabled';
    console.log('curPage', curPage, 'preEnable', preEnable, preEnabled, 'nextEnable', nextEnable, nextEnabled);
    if (preEnable==='enable') {
        $('#question-list').append('<span onclick="prePageQuestion()" class="page-btn previous ' + preEnable + '" ' + preEnabled + '>&laquo; 上一页</span>');
    }
    if (nextEnable==='enable') {
        $('#question-list').append('<span onclick="nextPageQuestion()" class="page-btn next ' + nextEnable + '" ' + nextEnabled + '>下一页 &raquo;</span>');
    }
}

function nextPageQuestion() {
    showPage(curPage + 1)
}

function prePageQuestion() {
    showPage(curPage - 1)
}

function showDetail(question) {
    $.ajax({
        url: '/detail/' + question,
        beforeSend: function (xhr) {
            console.log('before send');
        },
        success: function (result, status, xhr) {
            console.log('success', result);
            var data = result['data'];
            new $.flavr({
                title: data['question'],
                // dialog: 'form',
                // form: {
                content:
                // '<div>' + result['question'] + '</div><br>' +
                    '<div style="max-height:400px;overflow-y: auto">' + data['detail'] + '</div>'
                // }
            });
        },
        error: function (xhr, status, error) {
            console.log('error', status, error, xhr)
        },
        complete: function (xhr, status) {
            console.log('complete', status, xhr);
        }
    });
}