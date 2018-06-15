// Load recent notices from the Federal Register
var notices = {
    init: function() {
        notices.loading();
        notices.call();
    },

    call: function() {
        $.ajax({
            type: 'GET',
            url: notices.config.apiUrl,
            data: {
                'per_page': notices.config.totalNotices,
                'order': notices.config.order,
                'conditions[agencies]': notices.config.agency
                },
            contentType: 'application/json',
            dataType: 'jsonp',
            cache: 'true',
            success: function(data) {
                notices.stopLoading();
                notices.successLoad(data);
            },
            error: function() {
                notices.stopLoading();
                notices.errorMessage();
            }
        });
    },

    loading: function(){
        notices.config.$container.addClass('loading-spinner');
    },

    stopLoading: function(){
        notices.config.$container.removeClass('loading-spinner');
    },

    successLoad: function(data) {
        var results = data.results;
            for(var i = 0; i < results.length; i++) {
                var url = results[i].html_url,
                    title = results[i].title;
                notices.config.$container.append(
                  '<li><a class="external" href="' + url + '" target="_blank" rel="noopener noreferrer">' + title + '</a></li>'
                );
            }

            notices.config.$container.after(
              '<p class="sub-text"><a class="go" href="'+ notices.config.agencyNoticeURL + '">' +
              '<strong>More ' + notices.config.agencyAbbr + ' notices</strong></a></p>'
            );
    },

    errorMessage: function() {
        $('.recent-rules .sub-text').hide();
        notices.config.$container.append('<li>See all of ' + notices.config.agencyAbbr + '\'s recently issued rules at' +
        ' <a class="external" href="' + notices.config.agencyNoticeUR + '">'+ notices.config.agencyURL +'</a></li>'
        );
    }

};

// Toggle the mobile navigation
var navToggle = {
    init: function() {
        $('.mobile-nav-trigger').on( 'click', function(e) {
            e.preventDefault();
            $('.app-nav-list, .mobile-nav-trigger').toggleClass('open');
        });
    }
};

notices.config = {
    $container: $('.notices'),
    apiUrl: 'https://www.federalregister.gov/api/v1/articles.json',
    totalNotices: '10',
    order: 'newest',
    agency: 'consumer-financial-protection-bureau',
    agencyAbbr: 'CFPB',
    agencyNoticeURL: 'http://www.consumerfinance.gov/regulations/#finalrules',
    agencyURL: 'consumerfinance.gov/regulations'
};

$(document).ready(navToggle.init);
$(document).ready(notices.init);
