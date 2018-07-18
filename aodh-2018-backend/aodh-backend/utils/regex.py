class regexEnJa():
    # regex set to grab english and japanese text
    # used in tokenization for example
    # updated: 20180531
    # ref: http://www.localizingjapan.com/blog/2012/01/20/regular-expressions-for-japanese-text/
    # ref: https://stackoverflow.com/questions/43657034/javascript-regex-alphanumeric-english-and-japanese

    def __init__(self):
        # ENGLISH
        # normal regex (without spacing)
        self.r_letters_en = r"[A-Za-z]+"
        self.r_punc_en = r'[.?\-",]+'

        # JAPANESE (and all kanji characters in chinese)
        self.r_katakana = r"[\u30A1-\u30FA\u30FD-\u30FF\u31F0-\u31FF\u32D0-\u32FE\u3300-\u3357\uFF66-\uFF6F\uFF71-\uFF9D]|\uD82C\uDC00]"
        self.r_hiragana = r"[\u3041-\u3096\u309D-\u309F]|\uD82C\uDC01|\uD83C\uDE00]"
        self.r_kanji = r"[\u2E80-\u2E99\u2E9B-\u2EF3\u2F00-\u2FD5\u3005\u3007\u3021-\u3029\u3038-\u303B\u3400-\u4DB5\u4E00-\u9FD5\uF900-\uFA6D\uFA70-\uFAD9]|[\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872][\uDC00-\uDFFF]|\uD869[\uDC00-\uDED6\uDF00-\uDFFF]|\uD86D[\uDC00-\uDF34\uDF40-\uDFFF]|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]|\uD873[\uDC00-\uDEA1]|\uD87E[\uDC00-\uDE1D]"
        # japanese formatted punctuations with a lot of edge cases
        self.r_punc_ja = r"[\uFF01-\uFF20\uFF3B-\uFF40\uFF5B-\uFF5E\u3000-\u303F\u2605-\u2606\u2190-\u2195\u203B]+"
        # japanese formatted english letters
        self.r_letters_ja = r"[\uFF21-\uFF3A\uFF41-\uFF5A]+"
        # combination of both above
        self.r_letters_and_punc_ja = r"[\uFF01-\uFF5E\u3000-\u303F\u2605-\u2606\u2190-\u2195\u203B]"
        # other miscellany (includes fancy characters)
        self.r_misc_ja = r"[\u31F0-\u31FF\u3220-\u3243\u3280-\u337F]"

        # different forms of whitespace
        self.r_space = r"[ ]+"
        self.r_tabs_newlines = "[\\t\\n\\r\\f\\v]+"

        # url
        self.r_url = r"""(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?"""

    def regex_en_ja_characters_set(self, whitespace=False, tabs_newlines=False, url=True):
        regex_output_set = []
        if url:
            regex_output_set.append(self.r_url)
        if whitespace:
            regex_output_set.append(self.r_space)
        if tabs_newlines:
            regex_output_set.append(self.r_tabs_newlines)

        base_set = [
            self.r_katakana,
            self.r_hiragana,
            self.r_kanji,
            self.r_letters_ja,
            self.r_letters_en
        ]

        [regex_output_set.append(x) for x in base_set]

        regex_en_ja = r'|'.join(regex_output_set)

        return regex_en_ja

    def regex_en_ja_punctuations_set(self):
        regex = r'|'.join([
            self.r_punc_ja,
            self.r_punc_en
        ])
        return regex


