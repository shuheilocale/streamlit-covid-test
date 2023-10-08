import pandas as pd

from . import monster as m


class EncountMonsters:

    def __init__(self, monster_factory: m.MonsterFactory, monster_no_list: list):

        try:
            monster_list = [monster_factory.create_monster_by_no(
                int(monster_no)) for monster_no in monster_no_list]
            self.monster_list = self.construct(monster_list)
        except Exception as err:
            raise ValueError(f'おかしなモンスターの組み合わせです：{str(err)}')

    def construct(self, monster_list: list):
        # とても良く　= 4体
        # よく = 3体
        # ときどき = 2体
        # あまり = 1体
        # めったに = 1体
        # メタル = 1体

        n_monsters = [4, 3, 2, 1, 1, 1]

        if len(monster_list) != sum(n_monsters):
            raise ValueError('invalid monster num')

        def extract_findability(array: list, val: m.Findability):
            return [item for item in array if item.findability == val]

        ret = {}

        for findability_elem, n_monster in zip(m.Findability, n_monsters):
            ret[findability_elem] = extract_findability(
                monster_list, findability_elem)

            if len(ret[findability_elem]) != n_monster:
                raise ValueError(
                    f'{findability_elem.short_str()}の数が{len(ret[findability_elem])}体です。{n_monster}体のはずです。')

        return ret

    def judge_mass(self):

        # ① とてもよく枠に等倍がいる
        very_oftens = self.monster_list[m.Findability.VERY_OFTEN]
        n_very_oftens = sum(
            1 for monster in very_oftens if monster.exp_ratio == m.ExpRatio.P_ZERO)

        # 1匹だけいる→よく枠が全て１．１倍以上なら大量発生
        if n_very_oftens == 1:
            oftens = self.monster_list[m.Findability.OFTEN]
            if all(monster.exp_ratio == m.ExpRatio.P_ONE or monster.exp_ratio == m.ExpRatio.P_TWO for monster in oftens):
                target_monster = [
                    monster for monster in very_oftens if monster.exp_ratio == m.ExpRatio.P_ZERO][0]
                return f'大量発生 : {target_monster.name}'

        # 2匹以上いる→普通の地図
        if n_very_oftens >= 2:
            return '普通の地図 : とてもよく枠に等倍が2匹以上いる'

        # いない　→　②へ

        # ②よく枠に等倍がいる
        oftens = self.monster_list[m.Findability.OFTEN]
        n_oftens = sum(
            1 for monster in oftens if monster.exp_ratio == m.ExpRatio.P_ZERO)

        # 1匹だけいる　→大量発生
        if n_oftens == 1:
            target_monster = [
                monster for monster in oftens if monster.exp_ratio == m.ExpRatio.P_ZERO][0]
            return f'大量発生:{target_monster.name}'

        # 2匹以上いる　→　普通の地図
        if n_oftens >= 2:
            return '普通の地図 : よく枠に等倍が2匹以上いる'

        # いない　→　③へ

        # ③ときどき枠に等倍がいる
        sometimes = self.monster_list[m.Findability.SOMETIMES]
        n_sometimes = sum(
            1 for monster in sometimes if monster.exp_ratio == m.ExpRatio.P_ZERO)

        # 1匹だけいる→大量発生
        if n_sometimes == 1:
            target_monster = [
                monster for monster in sometimes if monster.exp_ratio == m.ExpRatio.P_ZERO][0]
            return f'大量発生:{target_monster.name}'

        # 2匹以上いる→普通の地図
        if n_sometimes >= 2:
            return '普通の地図 ときどき枠に等倍が2匹以上いる'

        # いない　→　検証中
        return '検証中'

    def to_df(self, hide_monster_no: bool = True):

        if hide_monster_no:
            columns = ['見かけやすさ', '経験値倍率', 'モンスター名']
        else:
            columns = ['見かけやすさ', '経験値', '図鑑No.', 'モンスター名']
        data = []

        for findability, monsters in self.monster_list.items():
            for monster in monsters:
                if hide_monster_no:
                    data.append(
                        [findability.short_str(),
                            monster.exp_ratio.short_str(),
                            monster.name]
                    )
                else:
                    data.append(
                        [findability.short_str(),
                         monster.exp_ratio.value,
                         monster.no,
                         monster.name]
                    )

        return pd.DataFrame(data, columns=columns).set_index('見かけやすさ')
