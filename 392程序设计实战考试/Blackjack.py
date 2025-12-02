import random

class Deck:
    def __init__(self):
        self.cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        self.shuffle()

    def reset(self):
        self.cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    def shuffle(self):
        random.shuffle(self.cards)
    def fapai(self):
        return  self.cards.pop()

class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.player_cards = []
        self.zhuangjia_cards = []

    def get_card_value(self, card_str):
        if card_str in ('J', 'Q', 'K'):
            return 10
        elif card_str == 'A':
            return 11
        else:
            return int(card_str)

    def get_sum(self, hand):
        total = 0
        aces = 0
        for _ in hand:
            val = self.get_card_value(_)
            if val == 11:
                aces += 1
            total += val
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def check(self):
        if self.get_sum(self.player_cards) > 21:
            print('你爆了!')
            return True
        if self.get_sum(self.zhuangjia_cards) > 21:
            print('庄家爆了!')
            return True
    def battle(self):
        player = self.get_sum(self.player_cards)
        zhuangjia = self.get_sum(self.zhuangjia_cards)
        if player > zhuangjia :
            print("你赢了！")
        if player == zhuangjia:
            print("平局")
        else :
            print("你输了!")
        return True
    def play(self):
        start = input('Blackjack y(开始游戏) n(退出)')
        if start == 'y':
            print('初始发牌...')
            for _ in range(2):
                self.player_cards.append(self.deck.fapai())
                self.zhuangjia_cards.append(self.deck.fapai())
                self.check()
            print("你的手牌：",self.player_cards)
            print("庄家的手牌: ["+self.zhuangjia_cards[0]+", ? ]")

        if start == 'n':
            print('游戏退出')
            return True
        if start != 'y' and start != 'n':
            print("你的输入有误请重新输入")
            self.play()
        while (True):
            choupai = input("你要继续抽牌吗？ y(继续) n(退出)")

            if choupai == 'n':
                while self.get_sum(self.zhuangjia_cards) < 17:
                    print('庄家正在抽牌...')
                    self.zhuangjia_cards.append(self.deck.fapai())
                    print("你的手牌：", self.player_cards)
                    print("庄家的手牌: [" + self.zhuangjia_cards[0] + ", ? ]")
                if self.check():
                    print("你的手牌：", self.player_cards)
                    print("庄家的手牌: ", self.zhuangjia_cards)
                    print("对局重新生成中...")
                    break
                self.battle()
                print("你的手牌：", self.player_cards)
                print("庄家的手牌: ", self.zhuangjia_cards)
                print("对局重新生成中...")
                break
            if choupai == 'y':
                self.player_cards.append(self.deck.fapai())
                self.zhuangjia_cards.append(self.deck.fapai())
                print("你的手牌：", self.player_cards)
                print("庄家的手牌: [" + self.zhuangjia_cards[0] + ", ? ]")
                if self.check():
                    print("你的手牌：", self.player_cards)
                    print("庄家的手牌: ", self.zhuangjia_cards)
                    print("对局重新生成中...")
                    break
        self.deck.reset()

if __name__ == '__main__':
    while(True):
        blackjack = Blackjack()
        blackjack.play()

