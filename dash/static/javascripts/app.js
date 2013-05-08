$(function() {
        var languages = ['javascript', 'ruby', 'python', 'c', 'php', 'java'];
        var lists = $('ul.square');

        function filterByLanguage(language) {
            // check that we can filter by that language (safe guard)
            if (languages.indexOf(language) > -1) {
              // select all li's in each of the lists
              var items = $('li', lists);

              // filter by the given language
              items.not('.lang-' + language).removeClass('hilighted');
              items.not('.lang-' + language).addClass('dehilighted');


              items.filter('.lang-' + language).addClass('hilighted');
              items.not('.lang-' + language).removeClass('dehilighted');
            }
          }

    $('.lang-selector').bind('click', function(e) {
        var language = $(this).attr('data-lang');

        filterByLanguage(language);

        e.preventDefault();
      })

    });