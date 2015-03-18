###
Bundle: Dashboard Tutorial Edit (assets)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Waaave
###

__ = window



class DashboardTutorialEdit
    init: ->
        try
            # Selectors
            @_document_sel = $ document
            @_window_sel = $ window
            @_dashboard_sel = $ '.dashboard'
            @_editor_form = @_dashboard_sel.find 'form#editorForm'
            @_label_online_sel = @_editor_form.find 'label[for="tutorialOnline"]'
            @_tutorial_online_sel = @_editor_form.find '#tutorialOnline'
            @_tutorial_content_sel = @_editor_form.find '#tutorialContent'
            @_tutorial_tag_sel = @_editor_form.find '#tutorialTags'
            @_bbcode_insert_btn_all_sel = @_editor_form.find '.tag-button, .emoticon'
            @_submit_button_all_sel = @_editor_form.find '.actions-moderation button, .actions button'
            @_editor_icon_picture = @_editor_form.find '.icon-picture'
            @_block_upload_sel = @_editor_form.find '.block-upload'
            @_input_file_sel = @_block_upload_sel.find '#fileInput'
            @_upload_message_sel = @_block_upload_sel.find '.upload-message'
            @_input_tag_sel = @_block_upload_sel.find '.input-tag'
            @_copy_tag_sel = @_block_upload_sel.find '.btn-copy-tag'
        catch error
            Console.error 'DashboardTutorialEdit.init', error


    event_toggle_state: ->
        try
            self = @

            @_tutorial_online_sel.change ->
                self._label_online_sel.find('.state-indicator').hide()

                if $(this).is ':checked'
                    self._label_online_sel.find('.state-online').show()
                else
                    self._label_online_sel.find('.state-offline').show()
        catch error
            Console.error 'DashboardTutorialEdit.event_toggle_state', error


    event_resize_textarea: ->
        try
            ev = LayoutMisc.adapt_sidebar_left

            @_document_sel.mouseup ev
            @_tutorial_content_sel.mousemove ev
        catch error
            Console.error 'DashboardTutorialEdit.event_resize_textarea', error


    _insert_tag: (element_sel) ->
        try
            textarea = @_tutorial_content_sel[0]
            selection = @_get_selection textarea
            scroll = textarea.scrollTop
            tag = element_sel.attr 'data-tag'
            tag_type = element_sel.attr 'data-tag-type'
            tag_builded = @_build_tag tag, tag_type, selection

            textarea.focus()
            textarea.value = "#{selection.start_selection}#{tag_builded}#{selection.end_selection}"
        catch error
            Console.error 'DashboardTutorialEdit._insert_tag', error


    event_insert_tag: ->
        try
            self = @

            @_bbcode_insert_btn_all_sel.click -> self._insert_tag $(this)
        catch error
            Console.error 'DashboardTutorialEdit.event_insert_tag', error


    _get_selection: (textarea_sel) ->
        selection = {}

        try
            if window.ActiveXObject
                text_range = document.selection.createRange()
                selection.current_selection = text_range.text
            else
                selection.start_selection = textarea_sel.value.substring 0, textarea_sel.selectionStart
                selection.end_selection = textarea_sel.value.substring textarea_sel.selectionEnd
                selection.current_selection = textarea_sel.value.substring textarea_sel.selectionStart, textarea_sel.selectionEnd
        catch error
            Console.error 'DashboardTutorialEdit._get_selection', error
        finally
            return selection


    _build_tag: (tag, tag_type, selection) ->
        string = null

        try
            tag_open = "[#{tag}]"
            tag_close = "[/#{tag}]"

            switch tag_type
                when 'classic'
                    string = "#{tag_open}#{selection.current_selection}#{tag_close}"
                when 'list'
                    tag_open = "[#{tag}]\n    [*] "
                    tag_close = "\n#{tag_close}"
                    string = "#{tag_open}#{selection.current_selection}#{tag_close}"
                when 'steps'
                    tag_open = "[#{tag}]\n    [step=1]"
                    tag_close = "[/step]\n#{tag_close}"
                    string = "#{tag_open}#{selection.current_selection}#{tag_close}"
                when 'url'
                    tag_open = "[#{tag}=link]"
                    string = "#{tag_open}#{selection.current_selection}#{tag_close}"
                when 'code'
                    tag_open = "[#{tag}=php]"
                    string = "#{tag_open}#{selection.current_selection}#{tag_close}"
                when 'img'
                    string = if (@_document_sel.width() < 1024) then "#{tag_open}#{selection.current_selection}#{tag_close}" \
                                                                else ''
                when 'quote'
                    tag_open = "[#{tag}=content_id]"
                    string = "#{tag_open}#{selection.current_selection}#{tag_close}"
                when 'emoticon'
                    string = tag
        catch error
            Console.error 'DashboardTutorialEdit._build_tag', error
        finally
            return string


    _update_form_buttons: (btn_sel) ->
        try
            action_ns = if (btn_sel.is '.btn-preview') then 'preview' else 'save'

            @_editor_form.attr
                'action': (@_editor_form.attr "data-#{action_ns}-action" or '')
                'target': (@_editor_form.attr "data-#{action_ns}-target" or '')
        catch error
            Console.error 'DashboardTutorialEdit._update_form_buttons', error


    event_form_buttons: ->
        try
            self = @

            @_submit_button_all_sel.click -> self._update_form_buttons $(this)
        catch error
            Console.error 'DashboardTutorialEdit.event_form_buttons', error


    tagit: ->
        try
            @_tutorial_tag_sel.tagit
                autocomplete: false
                caseSensitive: false
                removeConfirmation: true
        catch error
            Console.error 'DashboardTutorialEdit.tagit', error


    event_toggle_block_upload: ->
        try
            self = @

            @_editor_icon_picture.click ->
                if self._document_sel.width() >= 1024
                    self._block_upload_sel.slideToggle 'fast'

            @_window_sel.resize ->
                if self._document_sel.width() < 1024
                    self._block_upload_sel.hide()
        catch error
            Console.error 'DashboardTutorialEdit.event_toggle_block_upload', error


    event_copy_tag_to_clipboard: ->
        try
            self = @

            LayoutMisc.apply_clipboard(
                @_copy_tag_sel,
                ->
                    return self._build_tag(
                        'img',
                        'classic',
                        current_selection: self._input_tag_sel.val()
                    )
            )
        catch error
            Console.error 'DashboardTutorialEdit.event_copy_tag_to_clipboard', error


    event_ajax_uploader: ->
        try
            self = @

            @_input_file_sel.on(
                'change',
                ->
                    self._ajax_upload()
                    self._upload_message_sel.html 'Uploading...'
            )
        catch error
            Console.error 'DashboardTutorialEdit.event_ajax_uploader', error


    _ajax_upload: (file) ->
        try
            self = @

            page_id = LayoutPage.get_id()

            message = ''
            options =
                url: '/upload/uploader/',

                error: (response) ->
                    if page_id isnt LayoutPage.get_id()
                        return

                    message = '<span class="error">We\'re sorry, but something went wrong. Retry.</span>'
                    self._upload_message_sel.html message
                    self._input_file_sel.val ''

                    # Notify async system that DOM has been updated
                    LayoutPage.fire_dom_updated()

                success: (response) ->
                    if page_id isnt LayoutPage.get_id()
                        return

                    message = "<span class='#{response.status}'>#{response.result}</span> "
                    message = if (response.status is 'success') then "#{message}#{response.fileLink}" else message

                    self._upload_message_sel.html message
                    self._input_file_sel.val ''

                    # Notify async system that DOM has been updated
                    LayoutPage.fire_dom_updated()

            @_editor_form.ajaxSubmit options
        catch error
            Console.error 'DashboardTutorialEdit._ajax_upload', error



@DashboardTutorialEdit = new DashboardTutorialEdit



$(document).ready ->
    __.DashboardTutorialEdit.init()
    __.DashboardTutorialEdit.event_toggle_state()
    __.DashboardTutorialEdit.event_resize_textarea()
    __.DashboardTutorialEdit.event_insert_tag()
    __.DashboardTutorialEdit.event_form_buttons()
    __.DashboardTutorialEdit.tagit()
    __.DashboardTutorialEdit.event_toggle_block_upload()
    __.DashboardTutorialEdit.event_copy_tag_to_clipboard()
    __.DashboardTutorialEdit.event_ajax_uploader()

    LayoutRegistry.register_bundle 'DashboardTutorialEdit'
