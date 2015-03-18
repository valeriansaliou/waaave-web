###
Bundle: Layout (controllers)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Waaave
###

__ = window



class LayoutButtons
    init: ->
        try
            @_waaave_btn_all_sel = $ 'button.waaave-social'
            @_follow_btn_all_sel = $ 'button.follow'
            @_join_btn_all_sel = $ 'button.join'
            @_relevance_all_sel = $ 'div.relevance:has(form.form-relevance)'
        catch error
            Console.error 'LayoutButtons.init', error


    register: ->
        try
            __.LayoutRegistry.register_event 'buttons:init', @init, @
            __.LayoutRegistry.register_event 'buttons:events_all', @events_all, @
            __.LayoutRegistry.register_event 'buttons:load_social', @load_social, @, true
        catch error
            Console.error 'LayoutButtons.register', error


    events_all: (parent) ->
        try
            @_event_waaave parent
            @_event_follow parent
            @_event_join parent
            @_event_relevance parent
        catch error
            Console.error 'LayoutButtons.events_all', error


    _event_waaave: (parent) ->
        try
            self = @

            form_all_sel = @_waaave_btn_all_sel.hasParent(parent).parents 'form.waaave-btn-form'

            @_waaave_btn_all_sel.click ->
                button_sel = $ this
                form_sel = button_sel.parents 'form.waaave-btn-form'

                state_sel = form_sel.find 'input[name="waaave_state"]'
                counter_sel = form_all_sel.find '.waaave-social-counter'

                self._post_form 'waaaved', state_sel, counter_sel, form_sel, button_sel, form_all_sel, self._waaave_btn_all_sel
        catch error
            Console.error 'LayoutButtons._event_waaave', error
        finally
            return false


    _event_follow: (parent) ->
        try
            self = @

            @_follow_btn_all_sel.hasParent(parent).click ->
                try
                    button_sel = $ this
                    form_sel = button_sel.parents 'form.follow-btn-form'

                    # Not myself?
                    if not button_sel.attr('data-is-me')?
                        data_user_id = button_sel.attr 'data-user-id'

                        follow_btn_rel_sel = self._follow_btn_all_sel.filter "[data-user-id='#{data_user_id}']"
                        form_rel_sel = follow_btn_rel_sel.parents 'form.follow-btn-form'

                        state_sel = form_sel.find 'input[name="follow_state"]'
                        counter_sel = form_rel_sel.find '.follow-counter'

                        self._post_form 'following', state_sel, counter_sel, form_sel, button_sel, form_rel_sel, follow_btn_rel_sel
                    else
                        # Vibrate and warn the user
                        form_sel.stop(true).effect(
                            'shake',
                            times: 2, distance: 10,
                            300,
                            ->
                                new Tooltip(
                                    button_sel,
                                    (button_sel.attr 'data-tooltip-is-me'),

                                    [
                                        [
                                            'Got It',
                                            'primary'
                                        ]
                                    ]
                                )
                        )
                catch _error
                    Console.error 'LayoutButtons._event_follow[async]', _error
                finally
                    return false
        catch error
            Console.error 'LayoutButtons._event_follow', error


    _event_join: (parent) ->
        try
            self = @

            @_join_btn_all_sel.hasParent(parent).click ->
                try
                    button_sel = $ this
                    form_sel = button_sel.parents 'form.join-btn-form'

                    data_spot_id = button_sel.attr 'data-spot-id'

                    join_btn_rel_sel = self._join_btn_all_sel.filter "[data-spot-id='#{data_spot_id}']"
                    form_rel_sel = join_btn_rel_sel.parents 'form.join-btn-form'

                    state_sel = form_sel.find 'input[name="join_state"]'
                    counter_sel = form_rel_sel.find '.join-counter'

                    self._post_form 'joined', state_sel, counter_sel, form_sel, button_sel, form_rel_sel, join_btn_rel_sel
                catch _error
                    Console.error 'LayoutButtons._event_join[async]', _error
                finally
                    return false
        catch error
            Console.error 'LayoutButtons._event_join', error


    _post_form: (class_active, state_sel, counter_sel, form_sel, button_sel, form_all_sel, button_all_sel) ->
        try
            state_sel.val (if button_sel.hasClass(class_active) then '0' else '1')

            post_id = __.LayoutPage.get_id()

            form_sel.ajaxSubmit (data) ->
                if post_id isnt __.LayoutPage.get_id()
                    return

                try
                    if data.status is 'success'
                        status_now = data.contents.status
                        count_next = data.contents.count

                        if status_now is 1
                            button_all_sel.addClass class_active
                        else
                            button_all_sel.removeClass class_active

                        counter_sel.text count_next
                    else if data.contents.redirect
                        __.LayoutMisc.authenticate_tooltip button_sel, data.contents.redirect

                    button_all_sel.removeAttr 'disabled'
                    form_all_sel.removeClass 'loading-mask'

                    # Notify async system that DOM has been updated
                    __.LayoutPage.fire_dom_updated()
                catch _error
                    Console.error 'LayoutButtons._post_form[async]', _error

            form_all_sel.addClass 'loading-mask'
            button_all_sel.attr 'disabled', true
        catch error
            Console.error 'LayoutButtons._post_form', error


    _event_relevance: (parent) ->
        try
            self = @

            @_relevance_all_sel.hasParent(parent).find('button.btn-relevant, button.btn-irrelevant').click ->
                try
                    btn_sel = $ this
                    relevance_name = if (btn_sel.is '.btn-irrelevant') then 'irrelevant' else 'relevant'

                    self._post_relevance btn_sel, relevance_name
                catch _error
                    Console.error 'LayoutButtons._event_relevance[async]', _error
        catch error
            Console.error 'LayoutButtons._event_relevance', error


    _post_relevance: (button_sel, relevance_name) ->
        try
            self = @

            relevance_parent = button_sel.parents 'div.relevance'
            relevance_sel = @_relevance_all_sel.filter(
                '[data-item-id="' + relevance_parent.data('item-id') + '"][data-item-type="' + relevance_parent.data('item-type') + '"]'
            )

            form_relevance = relevance_sel.find 'form.form-relevance'
            button_all_sel = form_relevance.find "button.btn-#{relevance_name}"

            post_id = __.LayoutPage.get_id()

            form_relevance.find('input[name="relevance"]').val relevance_name
            form_relevance.ajaxSubmit (data) ->
                if post_id isnt __.LayoutPage.get_id()
                    return

                try
                    if $(data).is '.relevance'
                        relevance_sel.each ->
                            $(this).replaceWith data

                        self._relevance_all_sel = $ 'div.relevance:has(form.form-relevance)'
                        self._event_relevance()
                    else
                        form_relevance.find('button:disabled').removeAttr 'disabled'
                        relevance_sel.removeClass 'loading-mask'

                        if data.contents.redirect
                            __.LayoutMisc.authenticate_tooltip button_sel, data.contents.redirect

                    # Notify async system that DOM has been updated
                    __.LayoutPage.fire_dom_updated()
                catch _error
                    Console.error 'LayoutButtons._post_relevance[async]', _error

            relevance_sel.addClass 'loading-mask'
            form_relevance.find('button').attr 'disabled', true
        catch error
            Console.error 'LayoutButtons._post_relevance', error


    load_social: ->
        try
            try
                # Load Facebook widgets
                FB.XFBML.parse()
            catch _error
                Console.error 'LayoutButtons.load_social', 'Facebook script not ready!'

            try
                # Load Twitter widgets
                twttr.widgets.load()
            catch _error
                Console.error 'LayoutButtons.load_social', 'Twitter script not ready!'

            try
                # Load Google widgets
                gapi.plusone.go()
            catch _error
                Console.error 'LayoutButtons.load_social', 'Google script not ready!'
        catch error
            Console.error 'LayoutButtons.load_social', error


class LayoutComment
    init: ->
        try
            # Selectors
            @_document_sel = $ document
            @_block_comment_sel = $ '.block-comments'
            @_comments_sel = @_block_comment_sel.find '.comments'
            @_show_more_sel = @_block_comment_sel.find '.show-more'
            @_comments_load_sel = @_block_comment_sel.find '.comments-load'
            @_comments_load_error_sel = @_block_comment_sel.find '.comments-load-error'

            # Values
            @_last_hash = null

            # States
            @_page_size = 5
            @_cur_paging = 1
        catch error
            Console.error 'LayoutComment.init', error


    register: ->
        try
            __.LayoutRegistry.register_event 'comment:init', @init, @
            __.LayoutRegistry.register_event 'comment:events', @events, @
            __.LayoutRegistry.register_event 'comment:get_init', @get_init, @
            __.LayoutRegistry.register_event 'comment:submit_form', @event_submit_form, @
        catch error
            Console.error 'LayoutComment.register', error


    events: ->
        try
            self = @

            @_comments_load_error_sel.find('a.comment-load-retry').click ->
                self._get_all()
                return false
        catch error
            Console.error 'LayoutComment.events', error


    get_init: (parent) ->
        try
            self = @

            if @_block_comment_sel.hasParent(parent).size()
                @_get_all ->
                    try
                        self._wait_hash_change()
                    catch _error
                        Console.error 'LayoutComment.get_init[async]', _error
        catch error
            Console.error 'LayoutComment.get_init', error


    _get_all: (callback) ->
        try
            self = @

            if typeof callback isnt 'function'
                callback = (-> return)

            # Wait event
            @_comments_load_error_sel.hide()
            @_show_more_sel.hide()

            if @_comments_sel.is ':empty'
                @_comments_load_sel.show()

            # Get fetch URL
            fetch_url = @_block_comment_sel.attr 'data-fetch'
            get_id = __.LayoutPage.get_id()

            # Request comments
            $.ajax(
                url: fetch_url
                type: 'GET'

                success: (data) ->
                    (self._handle_get_all_success data, get_id, callback)
                error: (data) ->
                    (self._handle_get_all_error data, get_id)
            )
        catch error
            Console.error 'LayoutComment._get_all', error


    _handle_get_all_success: (data, get_id, callback) ->
        try
            if get_id isnt __.LayoutPage.get_id()
                return

            data_sel = $ data

            # Reset view
            @_show_more_sel.hide()
            @_comments_load_sel.hide()

            # Reset current paging
            @_cur_paging = 1

            # Append new comments
            if data_sel.is '.comments'
                @_block_comment_sel.find('.comments').replaceWith data_sel
                @_comments_sel = data_sel

                @_init_paging()
                @_event_next_paging()
                @_event_actions()
                @_event_editor()

                callback()

            # Notify async system that DOM has been updated
            __.LayoutPage.fire_dom_updated()
        catch _error
            Console.error 'LayoutComment._handle_get_all_success', _error


    _handle_get_all_error: (data, get_id) ->
        try
            @_comments_load_sel.hide()
            @_comments_load_error_sel.show()
            @_comments_sel.empty()
        catch _error
            Console.error 'LayoutComment._handle_get_all_error', _error


    reset_last_hash: ->
        try
            @_last_hash = null
        catch error
            Console.error 'LayoutComment.reset_last_hash', error


    get_hash_id: ->
        comment_id = null

        try
            hash = window.location.hash

            if hash and hash.match /^#comment\-(\d+)$/
                comment_id = RegExp.$1 or null
        catch error
            Console.error 'LayoutComment.get_hash_id', error
        finally
            return comment_id


    _wait_hash_change: ->
        try
            self = @

            @_document_sel.everyTime(
                100,
                ->
                    try
                        hash = window.location.hash

                        if hash and self._last_hash isnt hash
                            self._last_hash = hash
                            comment_id = self.get_hash_id()

                            if comment_id
                                self._go_to comment_id, 'pulse', 1000
                    catch _error
                        Console.error 'LayoutComment._wait_hash_change[async]', _error
            )
        catch error
            Console.error 'LayoutComment._wait_hash_change', error


    _go_to: (comment_id, effect, duration) ->
        try
            comment_sel = @_block_comment_sel.find "#comment-#{comment_id}"

            if typeof duration isnt 'number'
                duration = 250

            if comment_sel.size() and effect
                comment_flip = (sel) ->
                    sel.addClass('animated').addClass effect
                    sel.oneTime(
                        '2s',
                        -> sel.removeClass('animated').removeClass effect
                    )

                if comment_sel.is ':hidden'
                    @_all_paging()

                if comment_sel.is ':in-viewport'
                    comment_flip comment_sel
                else
                    $('html, body').animate(
                        scrollTop: (comment_sel.offset().top - $('header').height() - 40),
                        duration,
                        -> comment_flip comment_sel
                    )
        catch error
            Console.error 'LayoutComment._go_to', error


    _event_actions: ->
        try
            self = @

            # Show more comment content
            @_block_comment_sel.find('a.comment-trim-more.badge').click ->
                self._trim_expand $(this)
                return false

            # Relevant/Irrelevant/Flag buttons
            @_block_comment_sel.find('a.thumb-up, a.thumb-down, a.flag').click ->
                self._post_action $(this)
                return false

            # Reply link
            @_block_comment_sel.find('a.link-reply').click ->
                self._show_reply_form this
                return false

            # In-reply-to link
            @_block_comment_sel.find('.in-reply-to a').click ->
                self._go_to ($(this).attr 'data-rel-id'), 'pulse'
                return false

            # Comment hover event
            @_block_comment_sel.find('.comment').hover(
                ->
                    cur_comment_controls_sel = $(this).find '.comment-controls'

                    cur_comment_controls_sel.stopTime()
                    cur_comment_controls_sel.oneTime(
                        750,
                        -> cur_comment_controls_sel.stop(true).hide().fadeIn 250
                    )
                ->
                    cur_comment_controls_sel = $(this).find '.comment-controls'
                    cur_comment_controls_sel.stopTime()

                    if (cur_comment_controls_sel.find('.comment-delete').attr 'data-locked') isnt '1'
                        cur_comment_controls_sel.stop(true).show().fadeOut 250
            )

            # Comment edit click event
            @_block_comment_sel.find('button.comment-edit').click ->
                cur_comment_sel = $(this).parents '.comment'
                self._open_editor cur_comment_sel

            # Comment delete click event
            @_block_comment_sel.find('button.comment-delete').click ->
                cur_btn_delete_sel = $ this
                cur_comment_controls_sel = cur_btn_delete_sel.parents '.comment-controls'
                cur_btn_delete_sel.attr 'data-locked', '1'

                # Create tooltip
                cb_tooltip_fn = ->
                    cur_btn_delete_sel.removeAttr 'data-locked'
                    cur_comment_controls_sel.stop(true).show().fadeOut 250

                new Tooltip(
                    cur_btn_delete_sel,
                    (cur_btn_delete_sel.attr 'data-tooltip'),

                    [
                        [
                            'Remove',
                            'danger',
                            -> self._post_action cur_btn_delete_sel
                        ],

                        [
                            'Cancel',
                            ''
                        ]
                    ],

                    cb_tooltip_fn
                )
        catch error
            Console.error 'LayoutComment._event_actions', error


    _event_editor: ->
        try
            self = @

            comment_editor_sel = @_block_comment_sel.find '.comment-editor'

            # Comment edition textarea keypress event
            comment_editor_sel.keyup ->
                try
                    cur_comment_sel = $(this).parents '.comment'
                    cur_comment_editor_submit_sel = cur_comment_sel.find '.comment-editor .comment-submit'

                    if cur_comment_sel.find('textarea.comment-field').val()
                        cur_comment_editor_submit_sel.removeAttr 'disabled'
                    else
                        cur_comment_editor_submit_sel.attr 'disabled', true
                catch _error
                    Console.error 'LayoutHeader._event_editor[async]', _error

            # Comment edition cancel click event
            comment_editor_sel.find('.comment-cancel').click ->
                try
                    cur_comment_sel = $(this).parents '.comment'
                    self._close_editor cur_comment_sel
                catch _error
                    Console.error 'LayoutHeader._event_editor[async]', _error
                finally
                    return false

            # Comment edition form submit event
            comment_editor_sel.submit ->
                try
                    cur_comment_sel = $(this).parents '.comment'

                    cur_comment_new_val = cur_comment_sel.find('textarea.comment-field').val()
                    cur_comment_old_val = cur_comment_sel.find('textarea.comment-original').val()

                    if cur_comment_new_val
                        if cur_comment_new_val isnt cur_comment_old_val
                            self._submit_editor cur_comment_sel
                        else
                            self._close_editor cur_comment_sel
                catch _error
                    Console.error 'LayoutHeader._event_editor[async]', _error
                finally
                    return false

        catch error
            Console.error 'LayoutComment._event_editor', error


    _init_paging: ->
        try
            comments_overflow_sel = @_block_comment_sel.find('.comment').slice @_page_size

            if comments_overflow_sel.size()
                comments_overflow_sel.hide()
                @_show_more_sel.show()
            else
                @_show_more_sel.hide()
        catch error
            Console.error 'LayoutComment._init_paging', error


    _next_paging: ->
        try
            paging_start = (@_cur_paging++ * @_page_size) - 1
            paging_end = paging_start + @_page_size

            comments_next_sel = @_block_comment_sel.find('.comment').slice paging_start, paging_end
            comments_size = comments_next_sel.size()

            if(comments_size)
                comments_next_sel.show()

                # Hide the 'next comments' navigator?
                comment_next_last_sel = comments_next_sel.filter ':last'

                if comments_size < @_page_size or (comments_size is @_page_size and not
                   comment_next_last_sel.next('.comment, .comments-reply').size() and not
                   comment_next_last_sel.parent('.comment, .comments-reply').next())
                    @_show_more_sel.hide()
        catch error
            Console.error 'LayoutComment._next_paging', error


    _all_paging: ->
        try
            @_block_comment_sel.find('.comment:hidden').show()
            @_show_more_sel.hide()
        catch error
            Console.error 'LayoutComment._all_paging', error


    _event_next_paging: ->
        try
            self = @

            @_show_more_sel.click ->
                self._next_paging()
                return false
        catch error
            Console.error 'LayoutComment._event_next_paging', error


    _trim_expand: (expand_sel) ->
        try
            comment_content_sel = expand_sel.parents '.comment-content'

            comment_content_sel.find('.comment-trim-foot').hide()

            comment_content_sel.css(
                'max-height': 'none'
            )
        catch error
            Console.error 'LayoutComment._trim_expand', error


    _open_editor: (comment_sel) ->
        try
            comment_sel.find('.add-comment-form, .comment-content').hide()
            comment_sel.find('.comment-editor').show()
        catch error
            Console.error 'LayoutComment._open_editor', error


    _close_editor: (comment_sel) ->
        try
            comment_sel.find('.comment-editor').hide()
            comment_sel.find('.add-comment-form, .comment-content').show()

            @_reset_editor comment_sel
        catch error
            Console.error 'LayoutComment._close_editor', error


    _reset_editor: (comment_sel) ->
        try
            comment_editor_sel = comment_sel.find '.comment-editor'

            comment_initial_val = comment_editor_sel.find('textarea.comment-original').val()
            comment_editor_sel.find('textarea.comment-field').val comment_initial_val
        catch error
            Console.error 'LayoutComment._reset_editor', error


    _submit_editor: (comment_sel) ->
        try
            self = @

            comment_id = comment_sel.attr 'data-id'
            post_id = __.LayoutPage.get_id()

            comment_editor_sel = comment_sel.find '.comment-editor'
            comment_editor_items_sel = comment_editor_sel.find 'input, textarea, button'

            comment_editor_sel.ajaxSubmit(
                success: (data) ->
                    if post_id isnt __.LayoutPage.get_id()
                        return

                    try
                        if data.status is 'success'
                            # Reload all comments (preserves final sorting)
                            self._block_comment_sel.find('.comments').addClass 'loading-mask'
                            self._get_all ->
                                # Filter newcoming comments
                                self._all_paging()

                                # Action on newly published comment
                                if comment_id
                                    self._go_to comment_id, 'flipInX'
                        else
                            comment_editor_items_sel.removeAttr 'disabled'
                    catch _error
                        Console.error 'LayoutComment._submit_editor[async]', _error
            )

            comment_editor_items_sel.attr 'disabled', true
        catch error
            Console.error 'LayoutComment._submit_editor', error


    _show_reply_form: (el) ->
        try
            sel = $ el
            comment = sel.parents '.comment'

            # Can show?
            if not comment.next().is '.reply'
                # Hide other reply forms
                @_block_comment_sel.find('.reply:not(.reply-template)').filter( ->
                    return $(this).find('textarea').val() is ''
                ).find('a.comment-cancel').click()

                # Read reply data
                reply_val = comment.attr 'data-id'

                reply_template = sel.parents(@_block_comment_sel).find('.reply-template').eq(0).clone()

                reply_template.removeClass 'reply-template'
                reply_template.find('input[name="comment_in_reply_to"]').val reply_val

                comment.after reply_template
                reply_template.hide().slideDown 250

                # Apply subsequent events
                @event_submit_form null, (reply_template.find 'form')
                @_event_cancel_form reply_template
                @_event_key_form reply_template

            comment.next().find('textarea').focus()
        catch error
            Console.error 'LayoutComment._show_reply_form', error


    _handle_response_form: (form_sel, data) ->
        try
            self = @

            if(data.status is 'success')
                reenable_form = -> form_sel.find('textarea:disabled, button[type="submit"]:disabled').removeAttr 'disabled'

                if data.contents.please_login
                    form_submit_btn_sel = form_sel.find 'button.comment-submit'

                    # Create tooltip
                    new Tooltip(
                        form_submit_btn_sel,
                        (form_submit_btn_sel.attr 'data-tooltip-login'),

                        [
                            [
                                'Use Facebook',
                                'primary',
                                -> document.location.href = data.contents.next.facebook
                            ],

                            [
                                'Use Twitter',
                                'info',
                                -> document.location.href = data.contents.next.twitter
                            ],

                            [
                                'Register',
                                '',
                                -> document.location.href = data.contents.next.email
                            ]
                        ],

                        -> reenable_form(),
                        true
                    )

                else
                    comment_id = data.contents.id

                    # Reset form
                    form_sel.find('textarea').val ''

                    # Reload all comments (preserves final sorting)
                    @_block_comment_sel.find('.comments').addClass 'loading-mask'
                    @_get_all ->
                        # Filter newcoming comments
                        self._all_paging()

                        # Action on newly published comment
                        self._go_to comment_id, 'flipInX'

                    # Re-enables form
                    reenable_form()
        catch error
            Console.error 'LayoutComment._handle_response_form', error


    _handle_submit_form: (form_sel) ->
        try
            textarea_sel = form_sel.find 'textarea'
            textarea_val = textarea_sel.val()

            if textarea_val
                @_post_form form_sel, @_handle_response_form

                form_sel.find('button[type="submit"]').attr 'disabled', true
                textarea_sel.attr 'disabled', true
            else
                textarea_sel.focus()
        catch error
            Console.error 'LayoutComment._handle_submit_form', error


    event_submit_form: (parent, form_sel) ->
        try
            self = @

            if not form_sel?
                form_sel = @_block_comment_sel.find '.add-comment-form'

            form_sel.hasParent(parent).submit ->
                try
                    self._handle_submit_form form_sel
                catch _error
                    Console.error 'LayoutComment.event_submit_form', _error
                finally
                    return false
        catch error
            Console.error 'LayoutComment.event_submit_form', error


    _event_cancel_form: (reply_sel) ->
        try
            reply_sel.find('a.comment-cancel').click ->
                try
                    reply_sel.slideUp(
                        250,
                        -> $(this).remove()
                    )
                catch _error
                    Console.error 'LayoutComment._event_cancel_form', _error
                finally
                    return false
        catch error
            Console.error 'LayoutComment._event_cancel_form', error


    _event_key_form: (reply_sel) ->
        try
            reply_sel.find('textarea').keydown (e) ->
                switch e.keyCode
                    when 27
                        if not $(this).val()
                            reply_sel.find('a.comment-cancel').click()

                        return false
        catch error
            Console.error 'LayoutComment._event_key_form', error


    _post_form: (form_sel, callback) ->
        try
            self = @

            if typeof callback isnt 'function'
                callback = -> return

            post_id = __.LayoutPage.get_id()

            form_sel.ajaxSubmit(
                success: (data) ->
                    if post_id isnt __.LayoutPage.get_id()
                        return

                    (callback.bind self) form_sel, data

                    # Notify async system that DOM has been updated
                    __.LayoutPage.fire_dom_updated()
            )
        catch error
            Console.error 'LayoutComment._post_form', error


    _post_action: (action_sel) ->
        try
            btn_action = action_sel.attr 'data-action'
            form_sel = action_sel.parents 'form'
            comment_sel = form_sel.parents '.comment'
            comments_sel = comment_sel.parents '.comments'

            post_id = __.LayoutPage.get_id()

            if btn_action is 'delete'
                comment_sel.addClass 'action-mask'

            form_sel.find('input[name="comment_action"]').val btn_action

            form_sel.ajaxSubmit(
                success: (data) ->
                    if post_id isnt __.LayoutPage.get_id()
                        return

                    try
                        if data.status is 'success'
                            if btn_action is 'delete'
                                rm_comment_fn = (sel) ->
                                    sel.show().animate(
                                        height: 'toggle', opacity: 'toggle',
                                        250,
                                        ->
                                            $(this).remove()

                                            if not comments_sel.find('.comment').size()
                                                comments_sel.empty()
                                    )

                                if comment_sel.next().is '.comments-reply'
                                    rm_comment_fn (comment_sel.next '.comments-reply')

                                rm_comment_fn comment_sel

                            else if btn_action is 'flag'
                                action_sel.fadeOut(
                                    250,
                                    -> form_sel.find('.flag-done').fadeIn 250
                                )

                            else
                                if btn_action is 'relevant' or btn_action is 'irrelevant'
                                    # Update the relevance counter
                                    rank_number_sel = form_sel.find '.rank-number'
                                    count_relevant = parseInt (rank_number_sel.text() or 0), 10

                                    if btn_action is 'relevant'
                                        if form_sel.find('a.thumb-down.active').size()
                                            count_relevant += 2
                                        else if action_sel.hasClass 'active'
                                            count_relevant--
                                        else
                                            count_relevant++

                                    else if btn_action is 'irrelevant'
                                        if form_sel.find('a.thumb-up.active').size()
                                            count_relevant -= 2
                                        else if action_sel.hasClass 'active'
                                            count_relevant++
                                        else
                                            count_relevant--

                                    rank_number_sel.removeClass 'rank-positive rank-negative'

                                    if count_relevant < 0
                                        rank_number_sel.addClass 'rank-negative'
                                    else if count_relevant > 0
                                        rank_number_sel.addClass 'rank-positive'

                                    rank_number_sel.text (count_relevant or '')

                                # Update the thumb up/down state
                                if action_sel.hasClass 'active'
                                    action_sel.removeClass 'active'
                                else
                                    form_sel.find('a.thumb-up, a.thumb-down').removeClass 'active'
                                    action_sel.addClass 'active'

                        else if data.contents.redirect
                            __.LayoutMisc.authenticate_tooltip action_sel, data.contents.redirect

                        # Notify async system that DOM has been updated
                        __.LayoutPage.fire_dom_updated()
                    catch _error
                        Console.error 'LayoutComment._post_action[async]', _error
            )
        catch error
            Console.error 'LayoutComment._post_action', error


class LayoutEvents
    init: ->
        try
            # Variables
            @_events_url = $('html').attr 'data-url-events'

            # Configuration
            @_handlers =
                public: {}
                private:
                    notification: @_handle_notification_event
        catch error
            Console.error 'LayoutEvents.init', error


    go: ->
        try
            self = @

            if __.LayoutMisc.is_desktop()
                Console.info 'LayoutEvents.go', 'Connecting to Socket.IO server...'

                session_key = $.cookie 'sessionid'

                if session_key
                    socket = io.connect(
                        @_events_url,
                        query: "session_key=#{session_key}"
                    )

                    socket.on(
                        'connect',
                        ->
                            Console.debug 'LayoutEvents.go[async]', 'Socket.IO connected'

                            socket.on(
                                'public',
                                (data) -> self._handle_event('public', data)
                            )

                            socket.on(
                                'private',
                                (data) -> self._handle_event('private', data)
                            )

                            socket.on(
                                'disconnect',
                                -> Console.error 'LayoutEvents.go[async]', 'Socket.IO disconnected'
                            )
                    )
                else
                    Console.warn 'LayoutEvents.go', 'Not connecting to Socket.IO server (reason: empty session ID)'
            else
                Console.warn 'LayoutEvents.go', 'Not connecting to Socket.IO server (reason: not on desktop)'
        catch error
            Console.error 'LayoutEvents.go', error


    _handle_event: (channel, data) ->
        try
            if data.type? and @_handlers[channel][data.type]?
                @_handlers[channel][data.type] data

                Console.debug "LayoutEvents.go[async] >> (#{channel})", "Handled data for type: #{data.type}"
            else
                Console.warn "LayoutEvents.go[async] >> (#{channel})", "Could not find an handler for type: #{data.type}"
        catch error
            Console.error 'LayoutEvents._handle_event', error


    _handle_notification_event: (data) ->
        try
            Console.log 'LayoutEvents._handle_notification_event', 'Received data [notification]'
            Console.debug 'LayoutEvents._handle_notification_event', data

            if data.data.url
                __.LayoutNotification.receive_event_notification data.data.url
        catch error
            Console.error 'LayoutEvents._handle_notification_event', error


class LayoutFeed
    init: ->
        try
            # Selectors
            @_window_sel = $ window
            @_document_sel = $ document

            # Custom initialization
            @init_fetch_page()
        catch error
            Console.error 'LayoutFeed.init', error


    register: ->
        try
            __.LayoutRegistry.register_event 'feed:init_fetch_page', @init_fetch_page, @
            __.LayoutRegistry.register_event 'feed:fetch_page', @event_fetch_page, @
        catch error
            Console.error 'LayoutFeed.register', error


    init_fetch_page: ->
        try
            @_body_sel = @_document_sel.find '.body'
            @_timeline_sel = @_body_sel.find '.timeline'
            @_items_sel = @_timeline_sel.find '.items'
            @_load_more_btn_sel = @_timeline_sel.find '.show-more'

            # Variables
            @_times_auto_loaded = 0

            # States
            @_is_fetching = false
        catch error
            Console.error 'LayoutFeed.init_fetch_page', error


    event_fetch_page: ->
        try
            self = @

            if @._load_more_btn_sel isnt null
                @._load_more_btn_sel.find('a.more').click ->
                    self._fetch_page()
                    return false

            @._window_sel.scroll ->
                if (self._load_more_btn_sel isnt null and self._is_fetching isnt true and self._times_auto_loaded < 2) and
                   (self._window_sel.scrollTop() >= self._body_sel.height() - self._window_sel.height())
                    self._times_auto_loaded++
                    self._fetch_page()
        catch error
            Console.error 'LayoutFeed.event_fetch_page', error


    _fetch_page: ->
        try
            self = @

            if @_load_more_btn_sel is null
                Console.warn 'LayoutFeed._fetch_page', 'Nothing more to load...'
                return false

            if @_is_fetching is true
                Console.info 'LayoutFeed._fetch_page', 'Already fetching data!'
                return false

            @_is_fetching = true
            load_more_url = @_load_more_btn_sel.attr 'data-url'

            if not load_more_url
                Console.warn 'LayoutFeed._fetch_page', 'Looks like there is nothing to load!'
                return false

            @_load_more_btn_sel.addClass 'loading'
            page_id = __.LayoutPage.get_id()

            $.get(
                load_more_url,
                (data) ->
                    if page_id isnt __.LayoutPage.get_id()
                        return

                    data_sel = $ data

                    if data_sel.is '.page_content'
                        data_items_sel = data_sel.find '.items'
                        data_more_btn_sel = data_sel.find '.show-more'
                        data_page_end_sel = data_sel.find '.page-end'

                        if data_items_sel.size()
                            self._items_sel.append data_items_sel

                            if data_more_btn_sel.size()
                                self._load_more_btn_sel.replaceWith data_more_btn_sel

                                self._load_more_btn_sel = data_more_btn_sel
                                self.event_fetch_page()

                                self._load_more_btn_sel.removeClass 'loading'
                                self._is_fetching = false
                            else
                                self._load_more_btn_sel.replaceWith data_page_end_sel
                                self._load_more_btn_sel = null
                        else
                            self._load_more_btn_sel.replaceWith data_page_end_sel
                    else
                        Console.error 'LayoutFeed._fetch_page[async]', "#{data.status}:#{data.message}"

                    # Notify async system that DOM has been updated
                    __.LayoutPage.fire_dom_updated()
            )
        catch error
            Console.error 'LayoutFeed._fetch_page', error


class LayoutHeader
    init: ->
        try
            # Selectors
            @_body_sel = $ 'body'
            @_type_box_sel = $ '#typeBox'
            @_type_box_li_sel = @_type_box_sel.find 'li'
            @_type_input_sel = $ '#typeInput'
            @_result_type_sel = $ '#resultType'
            @_suggest_pane_sel = $ '#suggestPane'
            @_search_engine_form_sel = $ 'form.search-engine-form'
            @_search_engine_input_sel = @_search_engine_form_sel.find 'input.search-engine'
            @_notifications_deploy_sel = $ '.notifications-deploy'
            @_notifications_button_sel = $ '#notificationsButton'
            @_user_profile_sel = $ '.user-profile-header .profile'
            @_user_settings_sel = $ '#userSettings .arrow-deploy'
            @_user_settings_deploy_sel = $ '#userSettingsDeploy'
            @_search_mobile_tablet_sel = $ '#searchMobile, #searchTablet'
            @_search_mobile_tablet_btn_sel = $ '#searchMobileButton, #searchTabletButton'
            @_quick_sign_sel = $ '#quickSignBox'
            @_quick_sign_form_sel = @_quick_sign_sel.find '.qs-form'
            @_quick_sign_buttons_sel = @_quick_sign_sel.find '.qs-buttons'

            # States
            @_is_writing_opened = false
            @_is_suggest_pane_opened = false
            @_is_notifications_opened = false
            @_is_user_settings_opened = false

            # Constants
            @_suggest_pane_action = @_suggest_pane_sel.attr 'data-action'
        catch error
            Console.error 'LayoutHeader.init', error


    events: ->
        try
            @event_toggle_mobile_search()
            @event_deploy_result_type()
            @event_update_type_box()
            @event_search_form()
            @event_suggest_pane()
            @event_toggle_notifications()
            @event_toggle_user_settings()
            @event_toggle_quick_signin()
        catch error
            Console.error 'LayoutHeader.events', error


    _open_view: (status_bool, open_fn, close_fn) ->
        try
            if status_bool is false
                if @_has_view_open()
                    @_close_all()

                (open_fn.bind @)()
            else
                (close_fn.bind @)()
        catch error
            Console.error 'LayoutHeader._open_view', error


    _close_all: ->
        try
            if @_is_notifications_opened is true
                @_close_notifications()

            if @_is_user_settings_opened is true
                @_close_user_settings()
        catch error
            Console.error 'LayoutHeader._close_all', error


    _unbind_all: ->
        try
            @_body_sel.off 'click'
        catch error
            Console.error 'LayoutHeader._unbind_all', error


    _has_view_open: ->
        try
            return @_is_writing_opened or
                   @_is_notifications_opened or
                   @_is_user_settings_opened
        catch error
            Console.error 'LayoutHeader._has_view_open', error


    _toggle_mobile_search: ->
        try
            @_search_mobile_tablet_sel.stop(true).slideToggle()
        catch error
            Console.error 'LayoutHeader._toggle_mobile_search', error


    event_toggle_mobile_search: ->
        try
            self = @

            @_search_mobile_tablet_btn_sel.on(
                'click',
                ->
                    self._toggle_mobile_search()
                    return false
            )
        catch error
            Console.error 'LayoutHeader.event_toggle_mobile_search', error


    _deploy_result_type: ->
        try
            @_type_box_sel.fadeIn(100).addClass 'active'
            @_bind_close_result_type()
        catch error
            Console.error 'LayoutHeader._deploy_result_type', error


    event_deploy_result_type: ->
        try
            self = @

            @_result_type_sel.on(
                'click',
                ->
                    self._deploy_result_type()
                    return false
            )
        catch error
            Console.error 'LayoutHeader.event_deploy_result_type', error


    _bind_close_result_type: ->
        try
            self = @

            @_body_sel.on(
                'click',
                (evt) ->
                    try
                        tg = $ evt.target

                        if not (tg.parents('#resultType').size() or
                                (tg.is '#resultType') or
                                tg.parents('#typeBox').size() or
                                (tg.is '#typeBox'))
                            self._close_type_box()
                    catch _error
                        Console.error 'LayoutHeader._bind_close_result_type[event:click]', _error
            )
        catch error
            Console.error 'LayoutHeader._bind_close_result_type', error


    _unbind_close_result_type: ->
        try
            @_unbind_all()
        catch error
            Console.error 'LayoutHeader._unbind_close_result_type', error


    _update_type_box: (element_sel) ->
        try
            # Read picked type
            type_id = element_sel.data 'type'
            type_value = element_sel.text()

            # Apply new type
            @_result_type_sel.text type_value
            @_type_box_sel.children().prepend element_sel

            @_type_input_sel.val type_id
            @_close_type_box()

            # Update suggest pane
            if @_is_suggest_pane_opened
                @_search_suggest_pane()
        catch error
            Console.error 'LayoutHeader._update_type_box', error


    _close_type_box: ->
        try
            @_type_box_sel.fadeOut(100).removeClass 'active'
            @_unbind_close_result_type()
        catch error
            Console.error 'LayoutHeader._close_type_box', error


    event_update_type_box: ->
        try
            self = @

            @_type_box_li_sel.on(
                'click',
                ->
                    self._update_type_box $(this)
                    return false
            )
        catch error
            Console.error 'LayoutHeader.event_update_type_box', error


    event_search_form: ->
        try
            self = @

            @_search_engine_form_sel.submit ->
                # Virtually submit form (handles async page load)
                form_sel = $ this
                form_action = form_sel.attr 'action'

                q_val = form_sel.find('input[name="q"]').val()
                t_val = form_sel.find('input[name="t"]').val()

                __.LayoutPage.open_page (form_action + "?t=#{t_val}&q=#{q_val}")

                self._close_suggest_pane()
                self._prevent_sticky_suggest_pane()

                return false
        catch error
            Console.error 'LayoutHeader.event_search_form', error


    _open_suggest_pane: ->
        try
            if @_suggest_pane_sel.find('*').size() and
               (@_suggest_pane_sel.attr 'data-type') is @_type_input_sel.val() and
               (@_suggest_pane_sel.attr 'data-value') is @_search_engine_input_sel.val()
                @_is_suggest_pane_opened = true
                @_suggest_pane_sel.show()
                @_bind_close_suggest_pane()
            else
                Console.warn 'LayoutHeader._open_suggest_pane', 'Empty suggest pane, not opening it'
        catch error
            Console.error 'LayoutHeader._open_suggest_pane', error
        finally
            return true


    _close_suggest_pane: ->
        try
            @_is_suggest_pane_opened = false
            @_suggest_pane_sel.hide()
            @_unbind_close_suggest_pane()
        catch error
            Console.error 'LayoutHeader._close_suggest_pane', error
        finally
            return true


    _toggle_suggest_pane: ->
        try
            return @_open_view(
                @_is_suggest_pane_opened,
                @_open_suggest_pane,
                @_close_suggest_pane
            )
        catch error
            Console.error 'LayoutHeader._toggle_suggest_pane', error


    _prevent_sticky_suggest_pane: ->
        try
            self = @

            # Avoids the suggest pane from being sticky (because of async load)
            @_search_engine_input_sel.addClass 'locked'
            @_search_engine_input_sel.blur()

            @_search_engine_input_sel.one(
                'focus',
                -> self._search_engine_input_sel.removeClass 'locked'
            )
        catch error
            Console.error 'LayoutHeader._prevent_sticky_suggest_pane', error


    event_suggest_pane: ->
        try
            self = @

            @_search_engine_input_sel.keyup (e) ->
                # Escape?
                if e.keyCode is 27
                    self._search_engine_input_sel.val ''
                    self._close_suggest_pane()

            @_search_engine_input_sel.keydown (e) ->
                all_suggest_hoverable_sel = self._suggest_pane_sel.find 'div.item a.link'
                all_suggest_hoverable_size = all_suggest_hoverable_sel.size()
                selected_sel = all_suggest_hoverable_sel.filter '.selected'

                # Up/Down keys (navigate in search suggestions)
                if e.keyCode is 38 or e.keyCode is 40
                    if not selected_sel.size()
                        filter_sel

                        if e.keyCode is 38
                            filter_sel = all_suggest_hoverable_sel.filter ':last'
                        else
                            filter_sel = all_suggest_hoverable_sel.filter ':first'

                        filter_sel.addClass 'selected select-keyboard'

                    else if all_suggest_hoverable_size
                        hover_index = all_suggest_hoverable_sel.index selected_sel

                        if e.keyCode is 38
                            hover_index--
                        else
                            hover_index++

                        if hover_index < 0 or hover_index >= all_suggest_hoverable_size
                            hover_index = -1

                        if not all_suggest_hoverable_sel.eq(hover_index).size()
                            if e.keyCode is 38
                                hover_index = all_suggest_hoverable_sel.filter(':last').index()
                            else
                                hover_index = 0

                        selected_sel.removeClass 'selected select-keyboard'

                        if hover_index isnt -1
                            all_suggest_hoverable_sel.eq(hover_index).addClass 'selected select-keyboard'

                    return false

                # Enter key (go to the selected search suggestion)
                if e.keyCode is 13 and selected_sel.size() and (selected_sel.is '.select-keyboard')
                    selected_sel.click()
                    self._prevent_sticky_suggest_pane()

                    return false

            @_search_engine_input_sel.typeWatch(
                wait: 250,
                captureLength: 0,
                callback: self._search_suggest_pane.bind(self)
            )

            @_search_engine_input_sel.focus -> self._open_suggest_pane()
        catch error
            Console.error 'LayoutHeader.event_suggest_pane', error


    _search_suggest_pane: ->
        try
            self = @

            if @_search_engine_input_sel.hasClass 'locked'
                Console.warn 'LayoutHeader._search_suggest_pane', 'Search input locked'
                return

            type_value = @_type_input_sel.val() or 'all'
            search_value = @_search_engine_input_sel.val()

            if @_suggest_pane_sel.attr('data-type') is type_value and
               @_suggest_pane_sel.attr('data-value') is search_value
                @_open_suggest_pane()
                Console.warn 'LayoutHeader._search_suggest_pane', 'Suggested results already loaded, not reloading them!'
                return

            @_close_suggest_pane()

            if not type_value
                Console.warn 'LayoutHeader._search_suggest_pane', 'Type value is empty'
                return

            if not search_value
                Console.warn 'LayoutHeader._search_suggest_pane', 'Search value is empty'
                return

            action_url = @_suggest_pane_action +
                          '?t=' + encodeURIComponent(type_value) +
                          '&q=' + encodeURIComponent(search_value)

            $.get(
                action_url,
                (data) ->
                    try
                        data_sel = $ data
                        data_cont_html = $.trim data_sel.html()

                        if (data_sel.is '.suggest-pane') and data_cont_html
                            self._suggest_pane_sel.attr 'data-type', type_value
                            self._suggest_pane_sel.attr 'data-value', search_value

                            self._suggest_pane_sel.html data_cont_html
                            self._event_search_suggest_pane()

                            self._open_suggest_pane()
                    catch _error
                        Console.error 'LayoutHeader._search_suggest_pane[async]', _error

                    # Notify async system that DOM has been updated
                    __.LayoutPage.fire_dom_updated()
            )
        catch error
            Console.error 'LayoutHeader._search_suggest_pane', error


    _event_search_suggest_pane: ->
        try
            self = @

            all_suggest_link_sel = @_suggest_pane_sel.find 'a.link'

            all_suggest_link_sel.click -> self._close_suggest_pane()

            suggest_clean_fn = ->
                all_suggest_link_sel.removeClass 'selected select-keyboard'

            all_suggest_link_sel.hover(
                ->
                    suggest_clean_fn()
                    $(this).addClass 'selected'
                -> suggest_clean_fn()
            )

            @_suggest_pane_sel.find('a.more-results').click ->
                self._close_suggest_pane()
        catch error
            Console.error 'LayoutHeader._event_search_suggest_pane', error


    _bind_close_suggest_pane: ->
        try
            self = @

            @_body_sel.on(
                'click',
                (evt) ->
                    try
                        tg = $ evt.target

                        if not ((tg.is self._search_engine_input_sel) or
                                tg.parents('#suggestPane').size() or
                                (tg.is '#suggestPane'))
                            self._close_suggest_pane()
                    catch _error
                        Console.error 'LayoutHeader._bind_close_suggest_pane[event:click]', _error
            )
        catch error
            Console.error 'LayoutHeader._bind_close_suggest_pane', error


    _unbind_close_suggest_pane: ->
        try
            @_unbind_all()
        catch error
            Console.error 'LayoutHeader._unbind_close_suggest_pane', error


    _open_notifications: ->
        try
            @_is_notifications_opened = true
            @_notifications_deploy_sel.fadeIn 200
            @_bind_close_notifications()

            __.LayoutNotification.load_notifications()
            __.LayoutNotification.hide_growl_notification()
        catch error
            Console.error 'LayoutHeader._open_notifications', error


    _close_notifications: ->
        try
            @_is_notifications_opened = false
            @_unbind_close_notifications()

            @_notifications_deploy_sel.fadeOut(
                200,
                -> __.LayoutNotification.update_read_all_notification()
            )
        catch error
            Console.error 'LayoutHeader._close_notifications', error


    _toggle_notifications: ->
        try
            return @_open_view(
                @_is_notifications_opened,
                @_open_notifications,
                @_close_notifications
            )
        catch error
            Console.error 'LayoutHeader._toggle_notifications', error


    event_toggle_notifications: ->
        try
            self = @

            @_notifications_button_sel.on(
                'click',
                ->
                    self._toggle_notifications()
                    return false
            )
        catch error
            Console.error 'LayoutHeader.event_toggle_notifications', error


    _bind_close_notifications: ->
        try
            self = @

            @_body_sel.on(
                'click',
                (evt) ->
                    try
                        tg = $ evt.target

                        if not (tg.parents('#notificationsDeploy').size() or
                                (tg.is '#notificationsDeploy') or
                                tg.parents('#notificationsButton').size() or
                                (tg.is '#notificationsButton'))
                            self._close_notifications()
                    catch _error
                        Console.error 'LayoutHeader._bind_close_notifications[event:click]', _error
            )
        catch error
            Console.error 'LayoutHeader._bind_close_notifications', error


    _unbind_close_notifications: ->
        try
            @_unbind_all()
        catch error
            Console.error 'LayoutHeader._unbind_close_notifications', error


    _open_user_settings: ->
        try
            @_is_user_settings_opened = true
            @_user_settings_sel.addClass 'active'
            @_user_settings_deploy_sel.stop(true).show()
        catch error
            Console.error 'LayoutHeader._open_user_settings', error
        finally
            return true


    _close_user_settings: ->
        try
            @_is_user_settings_opened = false
            @_user_settings_sel.removeClass 'active'
            @_user_settings_deploy_sel.stop(true).hide()
        catch error
            Console.error 'LayoutHeader._close_user_settings', error
        finally
            return true


    _toggle_user_settings: ->
        try
            return @_open_view(
                @_is_user_settings_opened,
                @_open_user_settings,
                @_close_user_settings
            )
        catch error
            Console.error 'LayoutHeader._toggle_user_settings', error


    event_toggle_user_settings: ->
        try
            self = @

            @_user_settings_sel.mouseenter ->
                if not self._is_user_settings_opened
                    self._toggle_user_settings()
                return false

            @_user_profile_sel.mouseleave ->
                self._close_user_settings()
                return false
        catch error
            Console.error 'LayoutHeader.event_toggle_user_settings', error


    event_toggle_quick_signin: ->
        try
            self = @

            @_quick_sign_buttons_sel.find('a.qs-login').on(
                'click',
                ->
                    try
                        self._quick_sign_buttons_sel.fadeOut(
                            250,
                            ->
                                self._quick_sign_form_sel.fadeIn(
                                    250,
                                    -> $(this).find('input.qs-email').focus()
                                )
                        )
                    catch _error
                        Console.error 'LayoutHeader.event_toggle_quick_signin[async]', _error
                    finally
                        return false
            )

            @_quick_sign_form_sel.find('button.qs-cancel').on(
                'click',
                ->
                    try
                        self._quick_sign_form_sel.find('input.qs-email').blur()

                        self._quick_sign_form_sel.fadeOut(
                            250,
                            -> self._quick_sign_buttons_sel.fadeIn 250
                        )
                    catch _error
                        Console.error 'LayoutHeader.event_toggle_quick_signin[async]', _error
                    finally
                        return false
            )
        catch error
            Console.error 'LayoutHeader.event_toggle_quick_signin', error


class LayoutMisc
    init: ->
        try
            # Selectors
            @_window = $ window
            @_growl_notif = $ '.growl-notification'
            @_growl_notif_close = @_growl_notif.find '.close'

            # Values
            @_clipboard_flash = ($('html').attr 'data-url-static') + 'vendor/jquery/flashes/jquery.clipboard.swf'
            @_window_width = @_window.width()
            @_desktop_wide_width = 1200
            @_desktop_normal_width = 1024
            @_tablet_large_width = 768
            @_tablet_small_width = 600
            @_mobile_width = 320
            @_has_window_focus = true
            @_key_event = {}
        catch error
            Console.error 'LayoutMisc.init', error


    events: ->
        try
            # Remove Facebook Connect URL fragment
            @remove_facebook_connect_hash()
        catch error
            Console.error 'LayoutMisc.events', error


    register: ->
        try
            __.LayoutRegistry.register_event 'misc:focus_window', @event_focus_window, @
            __.LayoutRegistry.register_event 'misc:key', @events_key, @
            __.LayoutRegistry.register_event 'misc:clipboard_code', @event_clipboard_code, @
        catch error
            Console.error 'LayoutMisc.register', error


    has_focus_window: ->
        has_focus = @_has_window_focus

        try
            has_focus = document.hasFocus() and true
        catch error
            Console.error 'LayoutMisc.has_focus_window', error
        finally
            return has_focus


    event_focus_window: ->
        try
            self = @

            @_window.focus -> (self._has_window_focus = true)

            @_window.blur -> (self._has_window_focus = false)
        catch error
            Console.error 'LayoutMisc.event_focus_window', error


    remove_facebook_connect_hash: ->
        try
            # There is no way to get rid of this just after user logins, except using this...
            if window.location.hash and window.location.hash is '#_=_'
                try
                    window.history.pushState(
                        '',
                        document.title,
                        "#{window.location.pathname}#{window.location.search}"
                    )
                catch _error
                    window.location.hash = ''
        catch error
            Console.error 'LayoutMisc.remove_facebook_connect_hash', error


    apply_clipboard: (copy_sel, callback) ->
        try
            self = @

            if typeof copy_sel isnt 'object'
                Console.error 'LayoutMisc.apply_clipboard', 'You need to provide a valid jQuery selector'
                return

            if typeof callback isnt 'function'
                Console.error 'LayoutMisc.apply_clipboard', 'You need to provide a valid callback function'
                return

            copy_sel.on(
                'click',
                (e) -> e.preventDefault()
            )

            copy_sel.clipboard(
                path: self._clipboard_flash,
                copy: callback
            )
        catch error
            Console.error 'LayoutMisc.apply_clipboard', error


    event_clipboard_code: (parent) ->
        try
            self = @

            @apply_clipboard(
                ($('.block-code a.code-copy').hasParent parent),
                ->
                    this_sel = $ this

                    this_sel.find('.code-copy-first').hide()
                    this_sel.find('.code-copy-done').show()

                    return self._clipboard_code this_sel.closest '.block-code'
            )
        catch error
            Console.error 'LayoutMisc.event_clipboard_code', error


    _clipboard_code: (code_block_sel) ->
        try
            code_text = ''

            # Prepend copyright information
            #code_text += @_clipboard_copyright code_block_sel

            # Append lines of code (reformatted)
            code_block_sel.find('.code-line').each ->
                if code_text
                    code_text += '\n'

                code_text += $(this).text()

            return code_text
        catch error
            Console.error 'LayoutMisc._clipboard_code', error


    _clipboard_copyright: (code_block_sel) ->
        try
            code_text = ''
            code_copyright = code_block_sel.attr 'data-copyright'
            code_language = code_block_sel.attr 'data-language'

            if code_copyright and code_language
                code_copyright = _.str.sprintf code_copyright, window.location.href

                switch code_block_sel.attr 'data-language'
                    when 'html', 'xml'
                        code_text += "<!-- #{code_copyright} -->"
                    when 'php', 'js', 'css', 'sass', 'scss'
                        code_text += "/* #{code_copyright} */"
                    else
                        code_text += "##{code_copyright}"

                code_text += '\n'

            return code_text
        catch error
            Console.error 'LayoutMisc._clipboard_copyright', error


    authenticate_tooltip: (action_sel, redirect_data) ->
        try
            login_fn = ->
                if redirect_data.login
                    document.location.href = redirect_data.login

            register_fn = ->
                if redirect_data.register
                    document.location.href = redirect_data.register

            # Create tooltip
            new Tooltip(
                action_sel,
                (action_sel.attr 'data-tooltip'),

                [
                    [
                        'Sign In',
                        'info',
                        login_fn
                    ],

                    [
                        'Sign Up',
                        'primary',
                        register_fn
                    ]
                ]
            )
        catch error
            Console.error 'LayoutMisc.authenticate_tooltip', error


    events_key: ->
        try
            self = @

            @_window.keydown (evt) -> (self._key_event = evt)

            @_window.keyup -> (self._key_event = {})
        catch error
            Console.error 'LayoutMisc.events_key', error


    key_event: ->
        try
            return @_key_event
        catch error
            Console.error 'LayoutMisc.key_event', error


    is_desktop: ->
        try
            return @is_normal_desktop() or @is_wide_desktop()
        catch error
            Console.error 'LayoutMisc.is_desktop', error


    is_wide_desktop: ->
        try
            return @_window_width >= @_desktop_wide_width
        catch error
            Console.error 'LayoutMisc.is_wide_desktop', error


    is_normal_desktop: ->
        try
            return @_window_width >= @_desktop_normal_width and
                   @_window_width < @_desktop_wide_width
        catch error
            Console.error 'LayoutMisc.is_normal_desktop', error


    is_tablet: ->
        try
            return @is_small_tablet() or @is_large_tablet()
        catch error
            Console.error 'LayoutMisc.is_tablet', error


    is_large_tablet: ->
        try
            return @_window_width >= @_tablet_large_width and
                   @_window_width < @_desktop_normal_width
        catch error
            Console.error 'LayoutMisc.is_large_tablet', error


    is_small_tablet: ->
        try
            return @_window_width >= @_tablet_small_width and
                   @_window_width < @_tablet_large_width
        catch error
            Console.error 'LayoutMisc.is_small_tablet', error


    is_mobile: ->
        try
            return @_window_width >= @_mobile_width and
                   @_window_width < @_tablet_small_width
        catch error
            Console.error 'LayoutMisc.is_mobile', error


class LayoutNotification
    init: ->
        try
            # Selectors
            @_window_sel = $ window
            @_document_sel = $ document
            @_growl_wrapper_sel = $ '.growl-wrapper'
            @_notification_deploy_sel = $ '#notificationsDeploy'
            @_notification_box_sel = @_notification_deploy_sel.find '.notification-box'
            @_notification_more_sel = @_notification_deploy_sel.find '.more-notifications'
            @_notification_items_sel = @_notification_box_sel.find '.notification-items'
            @_notifications_button_sel = $ '#notificationsButton'
            @_notification_sel = null

            # States
            @_is_notifications_fetching = false
            @_is_notifications_fetched = false
        catch error
            Console.error 'LayoutNotification.init', error


    events: ->
        try
            @_notification_deploy_sel.find('a[href]').click -> __.LayoutHeader._close_notifications()
        catch error
            Console.error 'LayoutNotification.events', error


    load_notifications: ->
        try
            self = @

            check_read_notifications_fn = ->
                if self._notifications_button_sel.text() isnt '0'
                    self._read_all_notifications()

            if @_is_notifications_fetched is true
                check_read_notifications_fn()

                Console.warn 'LayoutNotification.load_notifications', 'Notifications already fetched!'
                return false

            if @_is_notifications_fetching is true
                Console.warn 'LayoutNotification.load_notifications', 'Already fetching notifications!'
                return false

            Console.info 'LayoutNotification.load_notifications', 'Loading notifications...'

            @_is_notifications_fetching = true

            load_url = @_notification_box_sel.attr 'data-url-fetch'
            @_notification_box_sel.addClass 'loading'

            $.get(
                load_url,
                (data) ->
                    data_sel = $ data

                    if data_sel.is '.notifications'
                        data_items_sel = data_sel.find '.notification'
                        self._notification_sel = data_items_sel

                        if data_items_sel.size()
                            self._notification_items_sel.append data_items_sel
                            self._notification_more_sel.show()

                            check_read_notifications_fn()
                        else
                            self._notification_box_sel.addClass 'empty'

                        self._is_notifications_fetched = true
                        self._is_notifications_fetching = false

                        # Apply async page load events
                        self._notification_box_sel.find('a[href]').click -> __.LayoutHeader._close_notifications()

                        Console.info 'LayoutNotification.load_notifications[async]', 'Notifications loaded.'
                    else
                        Console.error 'LayoutNotification.load_notifications[async]', "#{data.status}:#{data.message}"

                    self._notification_box_sel.removeClass 'loading'

                    # Notify async system that DOM has been updated
                    __.LayoutPage.fire_dom_updated()
            )
        catch error
            Console.error 'LayoutNotification.load_notifications', error


    _read_notifications: (read_type, url_read, callback_loading, callback_response) ->
        try
            @_notification_box_sel.attr 'action', url_read

            @_notification_box_sel.ajaxSubmit (data) ->
                if typeof callback_response is 'function'
                    callback_response (data.status is 'success')

                # Notify async system that DOM has been updated
                __.LayoutPage.fire_dom_updated()

            if typeof callback_loading is 'function'
                callback_loading()
        catch error
            Console.error 'LayoutNotification._read_notifications', error
        finally
            return true


    _read_all_notifications: ->
        return_value = false

        try
            self = @

            return_value = @_read_notifications(
                'all',
                (@_notification_box_sel.attr 'data-url-read'),
                -> return
                -> self._notifications_button_sel.removeClass('active').find('.number').text '0'
            )
        catch error
            Console.error 'LayoutNotification._read_all_notifications', error
        finally
            return return_value


    _read_single_notification: (notif_single_sel) ->
        return_value = false

        try
            self = @

            return_value = @_read_notifications(
                'single',
                (notif_single_sel.attr 'data-url-read'),
                -> return
                -> self._update_counter_notification -1
            )
        catch error
            Console.error 'LayoutNotification._read_single_notification', error
        finally
            return return_value


    update_read_all_notification: ->
        try
            if @_notification_sel isnt null
                @_notification_sel.removeClass('new').find('.label-new').remove()
        catch error
            Console.error 'LayoutNotification.update_read_all_notification', error


    _update_counter_notification: (value_add) ->
        try
            notif_number_sel = @_notifications_button_sel.find '.number'
            notif_number_count = notif_number_sel.text()

            notif_number_value = if not isNaN(notif_number_count) then ((parseInt notif_number_count, 10) + value_add) else 0

            if notif_number_value < 0
                notif_number_value = 0

            if notif_number_value is 0
                @_notifications_button_sel.removeClass 'active'
            else
                @_notifications_button_sel.addClass 'active'

            notif_number_sel.text notif_number_value
        catch error
            Console.error 'LayoutNotification._update_counter_notification', error


    receive_event_notification: (notif_url) ->
        try
            self = @

            $.get(
                notif_url,
                (data) ->
                    try
                        data_sel = $ data

                        if data_sel.is '.notifications'
                            data_items_sel = data_sel.find '.notification'

                            if data_items_sel.size() is 1
                                self._create_notification data_items_sel
                                self._create_growl_notification data_items_sel

                                self._update_counter_notification 1
                            else
                                Console.warn 'LayoutNotification.receive_event_notification[async]', 'Ignored received notifications (none or multiple received)'

                            Console.info 'LayoutNotification.receive_event_notification[async]', 'Single notification loaded.'
                        else
                            Console.error 'LayoutNotification.receive_event_notification[async]', 'Could not load single notification!'

                        # Notify async system that DOM has been updated
                        __.LayoutPage.fire_dom_updated()
                    catch _error
                        Console.error 'LayoutNotification.receive_event_notification[async]', _error
            )
        catch error
            Console.error 'LayoutNotification.receive_event_notification', error


    _create_notification: (notification_sel) ->
        try
            # No need to append notification if we don't have the list fetched...
            if @_is_notifications_fetched
                notification_clone_sel = notification_sel.clone true

                @_notification_items_sel.prepend notification_clone_sel
                @_notification_sel = @_notification_items_sel.find '.notification'
        catch error
            Console.error 'LayoutNotification._create_notification', error


    _create_growl_notification: (notification_sel) ->
        try
            notification_clone_sel = notification_sel.clone true

            @_growl_wrapper_sel.prepend notification_clone_sel

            @_events_growl_notification notification_clone_sel
            @show_growl_notification notification_clone_sel

            @hide_growl_notification(
                @_growl_wrapper_sel.find '.notification:gt(2)'
            )

            Console.info 'LayoutNotification._create_growl_notification', 'Created growl notification'
        catch error
            Console.error 'LayoutNotification._create_growl_notification', error


    show_growl_notification: (growl_notification_sel) ->
        try
            if typeof growl_notification_sel isnt 'object'
                growl_notification_sel = @_growl_wrapper_sel.find '.notification'

            growl_notification_sel.stop(true).hide().animate(
                height: 'toggle', opacity: 'toggle',
                400
            )
        catch error
            Console.error 'LayoutNotification.show_growl_notification', error


    hide_growl_notification: (growl_notification_sel) ->
        try
            if typeof growl_notification_sel isnt 'object'
                growl_notification_sel = @_growl_wrapper_sel.find '.notification'

            growl_notification_sel.each ->
                this_sel = $ this

                if this_sel.is ':visible'
                    this_sel.stopTime().stop(true).show().animate(
                        height: 'toggle', opacity: 'toggle',
                        250,
                        -> this_sel.remove()
                    )
                else
                    this_sel.stopTime().remove()
        catch error
            Console.error 'LayoutNotification.hide_growl_notification', error


    _events_growl_notification: (growl_notification_sel) ->
        try
            self = @

            if typeof growl_notification_sel isnt 'object'
                growl_notification_sel = @_growl_wrapper_sel.find '.notification'

            # Keep notification displayed if mouse is hover
            growl_notification_sel.hover(
                ->
                    this_sel = $ this

                    this_sel.stopTime()

                    # Mark as notification as read
                    if this_sel.hasClass 'new'
                        self._read_single_notification this_sel

                        this_all_sel = self._document_sel.find('.notification').filter( ->
                            this_sub_sel = $ this
                            return (this_sub_sel.attr 'data-type') is (this_sel.attr 'data-type') and
                                   (this_sub_sel.attr 'data-id') is (this_sel.attr 'data-id')
                        )

                        this_all_sel.removeClass 'new'
                        this_all_sel.find('.label-new:visible').fadeOut 250
                ->
                    this_sel = $ this

                    this_sel.stopTime()
                    this_sel.oneTime(
                        '2s',
                        -> self.hide_growl_notification this_sel
                    )
            )

            # Hide on notification close click
            growl_notification_sel.find('a.close').click ->
                self.hide_growl_notification growl_notification_sel
                return false

            # Hide notification after a while (if/when window has/gets focus)
            growl_autohide = ->
                growl_notification_sel.oneTime(
                    '15s',
                    -> self.hide_growl_notification $(this)
                )

            if __.LayoutMisc.has_focus_window()
                growl_autohide()
            else
                @_window_sel.focus growl_autohide
        catch error
            Console.error 'LayoutNotification._events_growl_notification', error


class LayoutPage
    init: ->
        try
            # Selectors
            @_window_sel = $ window
            @_document_sel = $ document
            @_head = $ 'head'
            @_header_sel = $ 'header.headers'
            @_bluelines_sel = @_header_sel.find '.bluelines'

            # States
            @_id_async = 0

            # Variables
            @_is_async_compatible = (window.history and history.pushState and true)
            @_http_protocol = document.location.protocol.replace ':', ''
            @_http_host = document.location.host
            @_state_url = document.location.pathname
        catch error
            Console.error 'LayoutPage.init', error


    register: ->
        try
            __.LayoutRegistry.register_event 'page:events_state_change', @events_state_change, @
            __.LayoutRegistry.register_event 'page:async_load', @events_async_load, @
        catch error
            Console.error 'LayoutPage.register', error


    purge_global_events: ->
        try
            @_window_sel.off()
            @_document_sel.off()
        catch error
            Console.error 'LayoutPage.purge_global_events', error


    open_page: (url) ->
        try
            if @_is_async_compatible
                @_run_async_load url
            else
                document.location.href = url
        catch error
            Console.error 'LayoutPage.open_page', error


    events_async_load: (parent) ->
        try
            self = @

            if @_is_async_compatible
                eligible_links = @_eligible_links_async_load().hasParent parent
                eligible_links_count = eligible_links.size()

                eligible_links.click (evt) ->
                    return_value = false

                    try
                        # Used by some to open up the target page in a new tab rather
                        if __.LayoutMisc.key_event().ctrlKey or __.LayoutMisc.key_event().metaKey
                            return_value = true
                        else
                            self._run_async_load ($(this).attr 'href')
                    catch _error
                        Console.error 'LayoutPage.events_async_load[async]', _error
                    finally
                        return return_value

                # Lock down further async load events on those links...
                eligible_links.attr 'data-async', 'active'

                if eligible_links_count
                    Console.debug 'LayoutPage.events_async_load', "Yay! #{eligible_links_count} internal links ajax-ified."
            else
                Console.error 'LayoutPage.events_async_load', 'Woops, your browser is not compatible with asynchronous page load!'
        catch error
            Console.error 'LayoutPage.events_async_load', error


    events_state_change: ->
        try
            self = @

            # State change callback function
            state_cb = (ev) ->
                new_state = document.location.pathname

                if new_state isnt self._state_url
                    self._state_url = new_state
                    self._run_async_load self._state_url

            # Unbind previous state handlers
            @_window_sel.off 'popstate'
            @_window_sel.off 'pushstate'

            # Re-bind state handlers
            @_window_sel.on 'popstate', state_cb
            @_window_sel.on 'pushstate', state_cb
        catch error
            Console.error 'LayoutPage.events_state_change', error


    fire_dom_updated: ->
        try
            @events_async_load 'body'
        catch error
            Console.error 'LayoutPage.fire_dom_updated', error


    get_id: ->
        try
            return @_id_async
        catch error
            Console.error 'LayoutPage.get_id', error


    _eligible_links_async_load: ->
        try
            http_base = "#{@_http_protocol}://#{@_http_host}/"
            r_match = new RegExp "^(#{http_base}|(/(?!https?://).*))", 'gi'

            return @_document_sel.find('a[href]:not([target="_blank"], [data-async="disabled"], [data-async="active"])').filter ->
                return $(this).attr('href').match r_match
        catch error
            Console.error 'LayoutPage._eligible_links_async_load', error


    _run_async_load: (url) ->
        try
            self = @

            @_begin_progress_bar()
            @_hide_error_alert()

            id = ++@_id_async

            req_cb = (data) ->
                self._handle_async_load id, url, data

            $.ajax(
                url: url
                headers:
                    'X-Requested-With': 'async_page_loader'
                type: 'GET'
                success: req_cb
                error: req_cb
            )

            Console.debug 'LayoutPage._run_async_load', "Loading page: #{url}"
        catch error
            Console.error 'LayoutPage._run_async_load', error


    _handle_async_load: (id, url, data) ->
        try
            self = @

            # Typical of a non-200 HTTP response (error response)
            if typeof data is 'object' and data.hasOwnProperty 'responseText'
                data = data.responseText

            if id is @_id_async
                data_sel = $ data
                new_dom = data_sel.filter '#body:first'

                # Valid response?
                if new_dom.size()
                    # Read some values
                    title = data_sel.filter 'title:first'

                    # Callback functions
                    callback_counter = 0
                    old_namespaced_script_sel = @_document_sel.find 'script:not([data-scope="common"])'
                    old_namespaced_stylesheet_sel = @_document_sel.find 'link[rel="stylesheet"]:not([data-scope="common"])'

                    cb_cleanup_fn = ->
                        # Purge old scripts
                        old_namespaced_script_sel.remove()
                        old_namespaced_stylesheet_sel.remove()

                        Console.debug 'LayoutPage._handle_async_load', "Done cleanup of old DOM before page: #{url}"

                    cb_post_display_fn = ->
                        # Finish load, happily! :)
                        self._end_progress_bar()
                        self._scroll_top()

                        # Reset other layout bundles
                        self._document_sel.oneTime(
                            250,
                            -> __.LayoutComment.reset_last_hash()
                        )

                        Console.debug 'LayoutPage._handle_async_load', "Done post display actions for page: #{url}"

                    cb_complete_fn = ->
                        # Wait a little bit (DOM rendering lag and other joys!)
                        self._document_sel.oneTime(
                            250,
                            ->
                                # Cleanup DOM
                                cb_cleanup_fn()

                                self._document_sel.find('title').replaceWith title
                                self._document_sel.find('#body').remove()
                                self._document_sel.find('#body_new').attr('id', 'body').show()

                                # Restore DOM events
                                __.LayoutRegistry.restore_events '#body'

                                # All done, now pushing to the history
                                if url isnt self._state_url
                                    self._state_url = url
                                    history.pushState null, title, url

                                # Trigger post-display events
                                cb_post_display_fn()

                                Console.debug 'LayoutPage._handle_async_load', "Loaded page: #{url}"
                        )

                    # Purge old environment
                    @purge_global_events()
                    __.LayoutRegistry.unload_bundles()

                    # Append new DOM (in a temporary-hidden fashion)
                    @_document_sel.find('#body_new').remove()

                    new_dom.attr 'id', 'body_new'
                    new_dom.hide()
                    new_dom.insertBefore(
                        @_document_sel.find '#body'
                    )

                    # Items to be appended directly
                    @_head.append(
                        data_sel.filter 'script:not([src]):not([data-scope="common"])'
                    )

                    @_head.append(
                        data_sel.filter 'link[rel="stylesheet"]:not([href]):not([data-scope="common"])'
                    )

                    # Items to load
                    load_list =
                        js: [],
                        css: []

                    data_sel.filter('script[src]:not([data-scope="common"])').each ->
                        script_src = $(this).attr 'src'

                        if script_src
                            load_list.js.push script_src

                    data_sel.filter('link[href][rel="stylesheet"]:not([data-scope="common"])').each ->
                        stylesheet_href = $(this).attr 'href'

                        if stylesheet_href
                            load_list.css.push stylesheet_href

                    if load_list.js.length or load_list.css.length
                        # Load new deps (finish page load once done)
                        if load_list.js.length
                            callback_counter++

                            Console.info 'LayoutPage._handle_async_load', 'Loading scripts...'

                            LazyLoad.js(
                                load_list.js,
                                ->
                                    Console.info 'LayoutPage._handle_async_load[async]', 'Scripts fully loaded'

                                    if --callback_counter is 0
                                        cb_complete_fn()
                            )

                        if load_list.css.length
                            callback_counter++

                            Console.info 'LayoutPage._handle_async_load', 'Loading stylesheets...'

                            LazyLoad.css(
                                load_list.css,
                                ->
                                    Console.info 'LayoutPage._handle_async_load[async]', 'Stylesheets fully loaded'

                                    if --callback_counter is 0
                                        cb_complete_fn()
                            )

                        Console.debug 'LayoutPage._handle_async_load', "Delayed page load (waiting for sources to be loaded first): #{url}"
                    else
                        cb_complete_fn()
                else
                    @_show_error_alert(10)
                    @_end_progress_bar()

                    Console.error 'LayoutPage._handle_async_load', "Got an abnormal or error response from: #{url}"
            else
                Console.warn 'LayoutPage._handle_async_load', "Dropped outpaced ID for page: #{url}"
        catch error
            Console.error 'LayoutPage._handle_async_load', error


    _begin_progress_bar: ->
        try
            # Reset progress bar
            @_bluelines_sel.stop true
            @_bluelines_sel.css
                width: 0

            # Animate progress bar!
            @_bluelines_sel.addClass 'animated'
            @_bluelines_sel.animate(
                width: '50%',
                600,
                'easeOutQuad'
            )
        catch error
            Console.error 'LayoutPage._begin_progress_bar', error


    _end_progress_bar: ->
        try
            self = @

            # Animate progress bar!
            @_bluelines_sel.animate(
                width: '100%',
                300,
                'linear',
                -> self._bluelines_sel.removeClass 'animated'
            )
        catch error
            Console.error 'LayoutPage._end_progress_bar', error


    _get_error_alert: ->
        try
            return @_document_sel.find '.alerts .async-load-error'
        catch error
            Console.error 'LayoutPage._get_error_alert', error


    _show_error_alert: (seconds=10) ->
        try
            error_alert_sel = @_get_error_alert()

            error_alert_sel.stop(true).hide()
            error_alert_sel.animate(
                height: 'toggle', opacity: 'toggle',
                400,
                -> $(this).oneTime(
                    "#{seconds}s",
                    -> $(this).animate(
                        height: 'toggle', opacity: 'toggle',
                        400
                    )
                )
            )
        catch error
            Console.error 'LayoutPage._show_error_alert', error


    _hide_error_alert: ->
        try
            error_alert_visible_sel = @_get_error_alert().filter ':visible'

            if error_alert_visible_sel.size()
                error_alert_visible_sel.stopTime()
                error_alert_visible_sel.stop(true).animate(
                    height: 'toggle', opacity: 'toggle',
                    250
                )
        catch error
            Console.error 'LayoutPage._hide_error_alert', error


    _scroll_top: ->
        try
            # Hack: do not interfere w/ other scroll events
            good_to_go = not __.LayoutComment.get_hash_id() and true

            if good_to_go
                @_window_sel.scrollTop 0
        catch error
            Console.error 'LayoutPage._scroll_top', error


class LayoutRegistry
    init: ->
        try
            # Variables
            @_registry_events = {}
            @_registry_bundles = []
        catch error
            Console.error 'LayoutRegistry.init', error


    events: ->
        try
            @_bind_events 'body'
        catch error
            Console.error 'LayoutRegistry.events', error


    _bind_events: (parent) ->
        try
            parent = (parent or 'body')

            is_init = (parent is 'body')
            cur_registry = null

            for ns, cur_registry of @_registry_events
                try
                    # Don't execute if we are in init mode + ignoring init
                    if not (is_init and cur_registry[2])
                        (cur_registry[0].bind cur_registry[1])(parent)

                    Console.debug 'LayoutRegistry._bind_events[loop]', "Bound callback function for #{ns}"
                catch _error
                    Console.error 'LayoutRegistry._bind_events[loop]', "Registry callback function execution failed for #{ns} with error message: #{_error}"
        catch error
            Console.error 'LayoutRegistry._bind_events', error


    register_event: (namespace, fn_callback, fn_context, ignore_init) ->
        try
            ignore_init = false or ignore_init
            @_registry_events[namespace] = [fn_callback, fn_context, ignore_init]

            Console.info 'LayoutRegistry.register_event', "Registered event: #{namespace}"
        catch error
            Console.error 'LayoutRegistry.register_event', error


    unregister_event: (namespace) ->
        try
            if namespace in @_registry_events
                delete @_registry_events[namespace]

                Console.info 'LayoutRegistry.unregister_event', "Unregistered event: #{namespace}"

                return true

            return false
        catch error
            Console.error 'LayoutRegistry.unregister_event', error


    init_events: ->
        try
            @_bind_events 'body'
        catch error
            Console.error 'LayoutRegistry.init_events', error


    restore_events: (parent) ->
        try
            @_bind_events parent
        catch error
            Console.error 'LayoutRegistry.restore_events', error


    register_bundle: (bundle) ->
        try
            @_registry_bundles.push(bundle)
        catch error
            Console.error 'LayoutRegistry.register_bundle', error


    unload_bundles: ->
        try
            count_unload = 0

            for cur_bundle in @_registry_bundles
                if __.hasOwnProperty(cur_bundle)
                    # Delete bundle, loaded in the current window
                    delete _[cur_bundle]
                    count_unload++

            Console.info 'LayoutRegistry.unload_bundles', "Unloaded #{count_unload} bundles"
        catch error
            Console.error 'LayoutRegistry.unload_bundles', error



@LayoutButtons          = new LayoutButtons
@LayoutComment          = new LayoutComment
@LayoutEvents           = new LayoutEvents
@LayoutFeed             = new LayoutFeed
@LayoutHeader           = new LayoutHeader
@LayoutMisc             = new LayoutMisc
@LayoutNotification     = new LayoutNotification
@LayoutPage             = new LayoutPage
@LayoutRegistry         = new LayoutRegistry



# Initialize registry before anything else
__.LayoutRegistry.init()



$(document).ready ->
    # Register events
    __.LayoutButtons.register()
    __.LayoutComment.register()
    __.LayoutFeed.register()
    __.LayoutMisc.register()
    __.LayoutPage.register()

    # Initialize controllers
    __.LayoutButtons.init()
    __.LayoutComment.init()
    __.LayoutEvents.init()
    __.LayoutFeed.init()
    __.LayoutHeader.init()
    __.LayoutMisc.init()
    __.LayoutNotification.init()
    __.LayoutPage.init()

    # Watch for events
    __.LayoutHeader.events()
    __.LayoutMisc.events()
    __.LayoutNotification.events()

    # Apply registry events
    __.LayoutRegistry.events()
