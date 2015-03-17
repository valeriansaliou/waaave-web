# -*- coding: utf-8 -*- 

import re, unicodedata


class StringsHelper(object):
    """
    An helper on strings operations
    """

    """
    Characters association all_maps
    """
    __latin_map = {
        u'À': 'A', u'Á': 'A', u'Â': 'A', u'Ã': 'A', u'Ä': 'A', u'Å': 'A', u'Æ': 'AE', u'Ç':'C', 
        u'È': 'E', u'É': 'E', u'Ê': 'E', u'Ë': 'E', u'Ì': 'I', u'Í': 'I', u'Î': 'I',
        u'Ï': 'I', u'Ð': 'D', u'Ñ': 'N', u'Ò': 'O', u'Ó': 'O', u'Ô': 'O', u'Õ': 'O', u'Ö':'O', 
        u'Ő': 'O', u'Ø': 'O', u'Ù': 'U', u'Ú': 'U', u'Û': 'U', u'Ü': 'U', u'Ű': 'U',
        u'Ý': 'Y', u'Þ': 'TH', u'ß': 'ss', u'à':'a', u'á':'a', u'â': 'a', u'ã': 'a', u'ä':'a', 
        u'å': 'a', u'æ': 'ae', u'ç': 'c', u'è': 'e', u'é': 'e', u'ê': 'e', u'ë': 'e',
        u'ì': 'i', u'í': 'i', u'î': 'i', u'ï': 'i', u'ð': 'd', u'ñ': 'n', u'ò': 'o', u'ó':'o', 
        u'ô': 'o', u'õ': 'o', u'ö': 'o', u'ő': 'o', u'ø': 'o', u'ù': 'u', u'ú': 'u',
        u'û': 'u', u'ü': 'u', u'ű': 'u', u'ý': 'y', u'þ': 'th', u'ÿ': 'y'
    }

    __latin_symbols_map = {
        u'©':'(c)'
    }

    __greek_map = {
        u'α':'a', u'β':'b', u'γ':'g', u'δ':'d', u'ε':'e', u'ζ':'z', u'η':'h', u'θ':'8',
        u'ι':'i', u'κ':'k', u'λ':'l', u'μ':'m', u'ν':'n', u'ξ':'3', u'ο':'o', u'π':'p',
        u'ρ':'r', u'σ':'s', u'τ':'t', u'υ':'y', u'φ':'f', u'χ':'x', u'ψ':'ps', u'ω':'w',
        u'ά':'a', u'έ':'e', u'ί':'i', u'ό':'o', u'ύ':'y', u'ή':'h', u'ώ':'w', u'ς':'s',
        u'ϊ':'i', u'ΰ':'y', u'ϋ':'y', u'ΐ':'i',
        u'Α':'A', u'Β':'B', u'Γ':'G', u'Δ':'D', u'Ε':'E', u'Ζ':'Z', u'Η':'H', u'Θ':'8',
        u'Ι':'I', u'Κ':'K', u'Λ':'L', u'Μ':'M', u'Ν':'N', u'Ξ':'3', u'Ο':'O', u'Π':'P',
        u'Ρ':'R', u'Σ':'S', u'Τ':'T', u'Υ':'Y', u'Φ':'F', u'Χ':'X', u'Ψ':'PS', u'Ω':'W',
        u'Ά':'A', u'Έ':'E', u'Ί':'I', u'Ό':'O', u'Ύ':'Y', u'Ή':'H', u'Ώ':'W', u'Ϊ':'I',
        u'Ϋ':'Y'
    }

    __turkish_map = {
        u'ş':'s', u'Ş':'S', u'ı':'i', u'İ':'I', u'ç':'c', u'Ç':'C', u'ü':'u', u'Ü':'U',
        u'ö':'o', u'Ö':'O', u'ğ':'g', u'Ğ':'G'
    }

    __russian_map = {
        u'а':'a', u'б':'b', u'в':'v', u'г':'g', u'д':'d', u'е':'e', u'ё':'yo', u'ж':'zh',
        u'з':'z', u'и':'i', u'й':'j', u'к':'k', u'л':'l', u'м':'m', u'н':'n', u'о':'o',
        u'п':'p', u'р':'r', u'с':'s', u'т':'t', u'у':'u', u'ф':'f', u'х':'h', u'ц':'c',
        u'ч':'ch', u'ш':'sh', u'щ':'sh', u'ъ':'', u'ы':'y', u'ь':'', u'э':'e', u'ю':'yu',
        u'я':'ya',
        u'А':'A', u'Б':'B', u'В':'V', u'Г':'G', u'Д':'D', u'Е':'E', u'Ё':'Yo', u'Ж':'Zh',
        u'З':'Z', u'И':'I', u'Й':'J', u'К':'K', u'Л':'L', u'М':'M', u'Н':'N', u'О':'O',
        u'П':'P', u'Р':'R', u'С':'S', u'Т':'T', u'У':'U', u'Ф':'F', u'Х':'H', u'Ц':'C',
        u'Ч':'Ch', u'Ш':'Sh', u'Щ':'Sh', u'Ъ':'', u'Ы':'Y', u'Ь':'', u'Э':'E', u'Ю':'Yu',
        u'Я':'Ya'
    }

    __ukrainian_map = {
        u'Є':'Ye', u'І':'I', u'Ї':'Yi', u'Ґ':'G', u'є':'ye', u'і':'i', u'ї':'yi', u'ґ':'g'
    }

    __czech_map = {
        u'č':'c', u'ď':'d', u'ě':'e', u'ň':'n', u'ř':'r', u'š':'s', u'ť':'t', u'ů':'u',
        u'ž':'z', u'Č':'C', u'Ď':'D', u'Ě':'E', u'Ň':'N', u'Ř':'R', u'Š':'S', u'Ť':'T',
        u'Ů':'U', u'Ž':'Z'
    }

    __polish_map = {
        u'ą':'a', u'ć':'c', u'ę':'e', u'ł':'l', u'ń':'n', u'ó':'o', u'ś':'s', u'ź':'z',
        u'ż':'z', u'Ą':'A', u'Ć':'C', u'Ę':'e', u'Ł':'L', u'Ń':'N', u'Ó':'o', u'Ś':'S',
        u'Ź':'Z', u'Ż':'Z'
    }

    __latvian_map = {
        u'ā':'a', u'č':'c', u'ē':'e', u'ģ':'g', u'ī':'i', u'ķ':'k', u'ļ':'l', u'ņ':'n',
        u'š':'s', u'ū':'u', u'ž':'z', u'Ā':'A', u'Č':'C', u'Ē':'E', u'Ģ':'G', u'Ī':'i',
        u'Ķ':'k', u'Ļ':'L', u'Ņ':'N', u'Š':'S', u'Ū':'u', u'Ž':'Z'
    }


    """
    Cached values
    """
    __mappings = None
    __regex = None



    @classmethod
    def __make_regex(_class):
        """
        Builds the characters mapping regex
        """
        all_maps = {}
        all_maps.update(_class.__latin_map)
        all_maps.update(_class.__latin_symbols_map)
        all_maps.update(_class.__greek_map)
        all_maps.update(_class.__turkish_map)
        all_maps.update(_class.__russian_map)
        all_maps.update(_class.__ukrainian_map)
        all_maps.update(_class.__czech_map)
        all_maps.update(_class.__polish_map)
        all_maps.update(_class.__latvian_map)
        
        s = u"".join(all_maps.keys())
        regex = re.compile(u"[%s]|[^%s]+" % (s,s))
        
        return all_maps, regex

    @classmethod
    def downcode(_class, string):
        """
        Downcodes special characters to their Latin equivalents (useful when slugifying special chars)
        """
        
        if not _class.__regex:
            _class.__mappings, _class.__regex = _class.__make_regex()    
        
        downcoded = ''

        for piece in _class.__regex.findall(string):
            if _class.__mappings.has_key(piece):
                downcoded += _class.__mappings[piece]
            else:
                downcoded += piece

        return downcoded


    @staticmethod
    def strip_accents(s):
        """
        Remove accents from a string
        """
        s = unicode(s)
        return ''.join(c for c in unicodedata.normalize('NFD', s)\
                              if unicodedata.category(c) != 'Mn')
