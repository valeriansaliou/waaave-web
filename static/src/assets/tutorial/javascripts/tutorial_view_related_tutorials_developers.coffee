###
Bundle: Tutorial View Related Tutorials & Developers (assets)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Hakuma Holdings Ltd.
###

__ = window



class TutorialViewRelatedTutorialsDevelopers
    init: ->
        try
            # Selectors
            @_window_sel = $ window
            @_document_sel = $ document
            @_body_sel = @_document_sel.find '.body'
            @_timeline_sel = @_body_sel.find '.timeline'
            @_items_sel = @_timeline_sel.find '.items'
            @_load_more_btn_sel = @_timeline_sel.find '.show-more'

            # States
            @_is_fetching = false
        catch error
            Console.error 'TutorialViewRelatedTutorialsDevelopers.init', error


    event_fetch_page: ->
        try
            @_load_more_btn_sel.find('a.more').click ->
                @_fetch_page()
                return false

            @_window_sel.scroll ->
                if (@_load_more_btn_sel isnt null and @_is_fetching isnt true) and
                   (@_window_sel.scrollTop() >= @_body_sel.height() - @_window_sel.height())
                    @_fetch_page()
        catch error
            Console.error 'TutorialViewRelatedTutorialsDevelopers.event_fetch_page', error


    _fetch_page: ->
        try
            if @_load_more_btn_sel is null
                Console.warn 'TutorialViewRelatedTutorialsDevelopers._fetch_page', 'Nothing more to load...'
                return false

            if @_is_fetching is true
                Console.info 'TutorialViewRelatedTutorialsDevelopers._fetch_page', 'Already fetching data!'
                return false

            @_is_fetching = true

            load_more_url = @_load_more_btn_sel.attr 'data-url'

            if not load_more_url
                Console.warn 'TutorialViewRelatedTutorialsDevelopers._fetch_page', 'Looks like there is nothing to load!'
                return false

            @_load_more_btn_sel.addClass 'loading'

            page_id = LayoutPage.get_id()

            $.get(
                load_more_url,
                (data) ->
                    if page_id isnt LayoutPage.get_id()
                        return

                    data_sel = $ data

                    if data_sel.is '.related_tutorials'
                        data_items_sel = data_sel.find '.items'
                        data_more_btn_sel = data_sel.find '.show-more'
                        data_page_end_sel = data_sel.find '.page-end'

                        if data_items_sel.size()
                            @_items_sel.append data_items_sel

                            if data_more_btn_sel.size()
                                @_load_more_btn_sel.replaceWith data_more_btn_sel

                                @_load_more_btn_sel = data_more_btn_sel
                                @event_fetch_page()

                                @_load_more_btn_sel.removeClass 'loading'
                                @_is_fetching = false
                            else
                                @_load_more_btn_sel.replaceWith data_page_end_sel
                                @_load_more_btn_sel = null
                        else
                            @_load_more_btn_sel.replaceWith data_page_end_sel
                    else
                        Console.error 'TutorialViewRelatedTutorialsDevelopers._fetch_page[async]', "#{data.status}:#{data.message}"

                    # Notify async system that DOM has been updated
                    LayoutPage.fire_dom_updated()
            )
        catch error
            Console.error 'TutorialViewRelatedTutorialsDevelopers _fetch_page', error
        finally
            return true



@TutorialViewRelatedTutorialsDevelopers = new TutorialViewRelatedTutorialsDevelopers



$(document).ready ->
    __.TutorialViewRelatedTutorialsDevelopers.init()
    __.TutorialViewRelatedTutorialsDevelopers.event_fetch_page()

    LayoutRegistry.register_bundle 'TutorialViewRelatedTutorialsDevelopers'
