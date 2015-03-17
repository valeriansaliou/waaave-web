###
Bundle: Account (assets)
Project: Waaave
Authors: Julien Le Coupanec, Valerian Saliou
Copyright: 2014, Hakuma Holdings Ltd.
###

__ = window



class Account
    init: ->
        try
            @_input_all = $ 'input'
            @_body = $ '#body'
            @_form_invalid_sel = $ 'form.is_invalid'
        catch error
            Console.error 'Account.init', error


    shake_invalid_form: ->
        try
            @_form_invalid_sel.effect(
                'shake',
                times: 2,
                350
            )
        catch error
            Console.error 'Account.shake_invalid_form', error


    focus_required_input: ->
        try
            @_body.find('input.input-error:visible, input:not([value]):visible').filter(':first').focus()
        catch error
            Console.error 'Account.focus_required_input', error



@Account = new Account



$(document).ready ->
    __.Account.init()
    __.Account.shake_invalid_form()
    __.Account.focus_required_input()

    LayoutRegistry.register_bundle 'Account'
