###
Bundle: Moderation Comments (assets)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Waaave
###

__ = window



class ModerationComments
    init: ->
        try
            # Selectors
            @_moderation_sel = $ '.body-central.moderation'
            @_comments_sel = @_moderation_sel.find '.comments'
            @_comment_all_sel = @_comments_sel.find '.comment'
            @_actions_all = @_comment_all_sel.find '.actions'
        catch error
            Console.error 'ModerationComments.init', error


    event_actions: ->
        try
            self = @

            # Relevant/Irrelevant/Flag buttons
            @_actions_all.find('a').click ->
                this_sel = $ this
                this_action = this_sel.attr 'data-action'

                if this_action
                    if this_action is 'delete'
                        new Tooltip(
                            this_sel,
                            (this_sel.attr 'data-tooltip'),

                            [
                                [
                                    'Remove',
                                    'danger',
                                    -> (self._post_action.bind self) this_sel
                                ]

                                ['Cancel', '']
                            ]
                        )
                    else
                        self._post_action this_sel

                    return false
        catch error
            Console.error 'ModerationComments.event_actions', error


    _post_action: (action_sel) ->
        try
            btn_action = action_sel.attr 'data-action'
            form_sel = action_sel.parents 'form'
            comment_sel = form_sel.parents '.comment'

            page_id = LayoutPage.get_id()

            form_sel.find('input[name="comment_action"]').val btn_action

            form_sel.ajaxSubmit
                success: (data) ->
                    if page_id isnt LayoutPage.get_id()
                        return

                    try
                        if data.status is 'success'
                            if btn_action is 'delete'
                                rm_comment_fn = (sel) ->
                                    sel.show().animate(
                                        height: 'toggle',
                                        opacity: 'toggle',
                                        250,
                                        -> $(this).remove()
                                    )

                                rm_comment_fn comment_sel

                            else if btn_action is 'hide'
                                comment_sel.addClass 'comment-hidden'

                            else if btn_action is 'unhide'
                                comment_sel.removeClass 'comment-hidden'

                        # Notify async system that DOM has been updated
                        LayoutPage.fire_dom_updated()
                    catch _error
                        Console.error 'ModerationComments._post_action[async]', _error
        catch error
            Console.error 'ModerationComments._post_action', error



@ModerationComments = new ModerationComments



$(document).ready ->
    __.ModerationComments.init()
    __.ModerationComments.event_actions()

    LayoutRegistry.register_bundle 'ModerationComments'
