class DownListObj:
    def __init__(self, char, language):
        self.char = char
        self.is_punctuation = self.is_punctuation(char)
        self.is_shengmu = self.is_shengmu()
        self.is_yunmu =  self.is_yunmu()
        self.is_shengmuyunmu = self.is_shengmu or self.is_yunmu
        self.language = language

    def is_shengmu(self):
        if self.char in ['sh', 'o', 'l', 'x',
                         'q', 'w', 'e', 'r', 't', 'y','ch', 'p',
                         'a', 's', 'd', 'f', 'g', 'h', 'j', 'k',
                         'z', 'c', 'zh', 'b', 'n', 'm']:
            return 1
        else:
            return 0

    def is_yunmu(self):
        if self.char in ['u', 'uo\no', 'uang\niang', 'ua\nia',
                         'iu', 'ei', 'e', 'uan\ner', 'ue', 'un', 'i', 'ie',
                         'a', 'ong\niong', 'ai', 'en', 'eng', 'ang', 'an', 'uai\ning',
                         'ou', 'ao', 'ui\nv', 'in', 'iao', 'ian']:
            return 1
        else:
            return 0

    def is_punctuation(self, char):
        if char in [',', '.', ';', ':', "'", '"', '!', '`', '@', '(', ')',' ']:
            return 1
        else:
            return 0

    # def is_shengmuyunmu(self, char):
    #     if char in ['sh', 'o', 'l', 'x', 'q', 'w', 'e', 'r', 't', 'y', 'ch', 'p',
    #                 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'z', 'c', 'zh', 'b',
    #                 'n','u', 'uo\no', 'uang\niang', 'ua\nia', 'iu', 'ei', 'e',
    #                 'uan\ner', 'ue', 'un', 'i', 'ie', 'ong\niong', 'ai',
    #                 'en', 'eng', 'ang', 'an', 'uai\ning', 'ou', 'ao', 'ui\nv',
    #                 'in', 'iao', 'ian']:
    #         return 1
    #     else:
    #         return 0

