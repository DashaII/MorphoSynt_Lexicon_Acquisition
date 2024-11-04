from utils import *
from lexeme import Lexeme


def check_verb(word):
    if word[-3:] in ['ать', 'ять', 'еть']:
        tag = "VERB_2CONJ_INF-NREF" if word in VERB_EXC_2_CONJUGATION else "VERB_1CONJ_INF-NREF"
        lex = Lexeme(lexeme=word, lemma=word, stem=word[:-3], tag=tag)
        return lex
    if word[-3:] == 'ить':
        tag = "VERB_1CONJ_INF-NREF" if word in VERB_EXC_1_CONJUGATION else "VERB_2CONJ_INF-NREF"
        lex = Lexeme(lexeme=word, lemma=word, stem=word[:-3], tag=tag)
        return lex
    return ""


def define_gender_noun_tag(key, words):
    tag = ''
    for word in words:
        lk = len(key)
        if lk == len(word) and key[:lk - 2] == word[:lk - 2] and key != word:
            if word[-1:] in ['я']:
                tag = "NOUN_MAS_2DEC"
                break
            elif word[-1:] == 'и':
                tag = "NOUN_FEM_3DEC"
    return tag


def is_noun(key, words):
    noun_set = [key[:-1]+'ей', key[:-1]+'ем', key[:-1]+'ам', key[:-1]+'у', key[:-1]+'ы', key[:-1]+'ами', key[:-1]+'ов',
                key[:-1]+'е', key[:-1]+'ом', key[:-1]+'ями', key[:-1]+'ь']
    verb_set = [key[:-2]+'ть', key[:-2]+'ться']
    if any(word in words for word in noun_set):
        return True
    else:
        return False


def is_noun_2(key, words):
    noun_set = [key[:-1]+'ей', key[:-1]+'ем', key[:-1]+'ам', key[:-1]+'у', key[:-1]+'ы', key[:-1]+'ами', key[:-1]+'ов',
                key[:-1]+'ом', key[:-1]+'ями', key[:-1]+'ь', key[:-1]+'и', key[:-1]+'я']
    if any(word in words for word in noun_set):
        return True
    else:
        return False


# ending -> size of adjective ending
def is_adj(key, words, ending: int):
    key_stem = key[:-ending]
    adj_set = [key_stem+'ого', key_stem+'его', key_stem+'ому', key_stem+'ыми', key_stem+'его', key_stem+'ему',
               key_stem+'ом', key_stem+'ым', key_stem+'ые', key_stem+'ых', key_stem+'ую', key_stem+'ой', key_stem+'им',
               key_stem+'ем', key_stem+'ый', key_stem+'ая', key_stem+'ое', key_stem+'ий']
    adj_set.remove(key)

    if any(word in words for word in adj_set):
        return True
    else:
        return False


def predefined_lists(word_list, lexicon):
    for word in word_list:
        if word in PARTICLES:
            lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="PART")
            lexicon.append(lex)
            continue
        if word in PRONOUNS:
            lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="PRON")
            lexicon.append(lex)
            continue
        if word in DETERMINERS:
            lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="DET")
            lexicon.append(lex)
            continue
        if word in ADPOSITIONS:
            lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="ADP")
            lexicon.append(lex)
            continue
        if word in CONJUNCTIONS:
            lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="CONJ")
            lexicon.append(lex)
            continue
    return lexicon

def apply_heuristics(word_groups):
    lexicon = []
    masc_adj = []
    inf_verbs = []

    for i, (key_word, words) in enumerate(word_groups.items()):
        for word in words:

            if word in PARTICLES:
                lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="PART")
                lexicon.append(lex)
                continue
            if word in PRONOUNS:
                lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="PRON")
                lexicon.append(lex)
                continue
            if word in DETERMINERS:
                lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="DET")
                lexicon.append(lex)
                continue
            if word in ADPOSITIONS:
                lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="ADP")
                lexicon.append(lex)
                continue
            if word in CONJUNCTIONS:
                lex = Lexeme(lexeme=word, lemma=word, stem=word, tag="CONJ")
                lexicon.append(lex)
                continue

            if word[-7:] == 'енность':
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-7], tag="NOUN_FEM_3DEC")
                lexicon.append(lex)
                continue
            if word[-6:] == 'нность':
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-6], tag="NOUN_FEM_3DEC")
                lexicon.append(lex)
                continue
            if word[-5:] == 'ность':
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-5], tag="NOUN_FEM_3DEC")
                lexicon.append(lex)
                continue
            if word[-4:] == 'ость':
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-4], tag="NOUN_FEM_3DEC")
                lexicon.append(lex)
                continue

            lex = check_verb(word)
            if lex != "":
                if word not in inf_verbs:
                    lexicon.append(lex)
                    inf_verbs.append(word)

                verb_ref = word + "ся"
                if verb_ref not in inf_verbs:
                    ref_tag = lex.tag[:-4] + "REF"
                    ref_lex = Lexeme(lexeme=verb_ref, lemma=verb_ref, stem=lex.stem, tag=ref_tag)
                    lexicon.append(ref_lex)
                    inf_verbs.append(verb_ref)
                continue

            if word[-2:] == 'ся' and word[-5:-2] in ['ать', 'ять', 'еть']:
                if word not in inf_verbs:
                    tag = "VERB_2CONJ_INF-REF" if word in VERB_EXC_2_CONJUGATION_REF else "VERB_1CONJ_INF-REF"
                    lex = Lexeme(lexeme=word, lemma=word, stem=word[:-5], tag=tag)
                    lexicon.append(lex)
                    inf_verbs.append(word)
                    continue
            if word[-2:] == 'ся' and word[-5:-2] == 'ить':
                if word not in inf_verbs:
                    tag = "VERB_1CONJ_INF-REF" if word in VERB_EXC_1_CONJUGATION_REF else "VERB_2CONJ_INF-REF"
                    lex = Lexeme(lexeme=word, lemma=word, stem=word[:-5], tag=tag)
                    lexicon.append(lex)
                    inf_verbs.append(word)
                    continue

            if word[-4:] in ['тель']:
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-4], tag="NOUN_MAS_2DEC")
                lexicon.append(lex)
                continue
            if word[-3:] == 'ица':
                lex = Lexeme(lexeme=word, lemma=word, stem="___", tag="NOUN_FEM_1DEC")
                lexicon.append(lex)
                continue
            if word[-2:] == 'ик':
                stem = word[:-3] if word[-3:] in ['ник', 'щик', 'чик'] else word[:-2]
                lex = Lexeme(lexeme=word, lemma=word, stem=stem, tag="NOUN_MAS_2DEC")
                lexicon.append(lex)
                continue

            if word[-2:] in ['рь', 'ль', 'нь']:
                tag = define_gender_noun_tag(word, words)
                if tag != "":
                    lex = Lexeme(lexeme=word, lemma=word, stem=word, tag=tag)
                    lexicon.append(lex)
                continue
            if word[-2:] in ['жь', 'щь']:
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-7], tag="NOUN_FEM_3DEC")
                lexicon.append(lex)
                continue

            if word[-2:] in ['ый']:
                # н в м т л р с д з п б
                if word not in masc_adj:
                    lex = Lexeme(lexeme=word, lemma=word, stem="___", tag="ADJ_MAS")
                    lexicon.append(lex)
                    masc_adj.append(word)
                continue
            if word[-4:] in ['нний'] or word[-3:] in ['кий', 'хий', 'чий', 'жий']:
                # прилаг к х ч ж
                if word not in masc_adj:
                    lex = Lexeme(lexeme=word, lemma=word, stem="___", tag="ADJ_MAS")
                    lexicon.append(lex)
                    masc_adj.append(word)
                continue
            if word[-2:] in ['ое', 'ая']:
                if (word[-3:-2] in VOICELESS) and ((word[:-2] + "ий") not in masc_adj):
                    lex_word = word[:-2] + "ий"
                    lex = Lexeme(lexeme=lex_word, lemma=lex_word, stem="___", tag="ADJ_MAS")
                    lexicon.append(lex)
                    masc_adj.append(lex_word)
                elif (word[-3:-2] in VOICED) and (
                        (word[:-2] + "ый") not in masc_adj):
                    lex_word = word[:-2] + "ый"
                    lex = Lexeme(lexeme=lex_word, lemma=lex_word, stem="___", tag="ADJ_MAS")
                    lexicon.append(lex)
                    masc_adj.append(lex_word)
                continue

            if word[-5:] == "ество":
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-5], tag="NOUN_NEU_2DEC")
                lexicon.append(lex)
                continue
            if word[-8:] == "тельство":
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-9], tag="NOUN_NEU_2DEC")
                lexicon.append(lex)
                continue
            if word[-4:] == "ство":
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-4], tag="NOUN_NEU_2DEC")
                lexicon.append(lex)
                continue
            if word[-6:] == "тельно":
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-7], tag="ADV")
                lexicon.append(lex)
                continue

            if word[-3:] in ["шно", "вно", "йно", "чно", "мно", "жно", "тно", "рно", "дно", "зно", "бно", "сно", "пно",
                             "щно", "лно"]:
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-2], tag="ADV")
                lexicon.append(lex)
                continue
            if word[-4:] in ["льно"]:
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-3], tag="ADV")
                lexicon.append(lex)
                continue
            if word[-3:] in ["нно"]:
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-4], tag="ADV")
                lexicon.append(lex)
                continue

            # hard to get feminine ["ана", "ена"] and masculine ["ан", "ен"] (plural ["аны", "ены"] is also hard),
            # so I use neutral only
            if word[-3:] in ["ено", "ано", "яно"]:
                lex = Lexeme(lexeme=word[:-1], lemma=word[:-1], stem=word[:-1], tag="VERB_---_PART_MAS")
                lexicon.append(lex)
                continue
            # DO NOT CHANGE THE ORDER
            if word[-2:] == "но":
                lex = Lexeme(lexeme=word, lemma=word, stem=word[:-1], tag="NOUN_NEU_2DEC")
                lexicon.append(lex)
                continue

            if word[-2:] in ["ло", "ла", "ли"] and word[-3:-2] in ["а", "и", "е", "я", "у"]:
                flag = is_noun(word, words)
                if not flag:
                    inf_verb = word[:-2] + "ть"
                    if inf_verb not in inf_verbs:
                        lex = check_verb(inf_verb)
                        if lex != "":
                            lexicon.append(lex)
                            inf_verbs.append(inf_verb)

                            inf_verb_ref = inf_verb + "ся"
                            if inf_verb_ref not in inf_verbs:
                                ref_tag = lex.tag[:-4] + "REF"
                                ref_lex = Lexeme(lexeme=inf_verb_ref, lemma=inf_verb_ref, stem=lex.stem, tag=ref_tag)
                                lexicon.append(ref_lex)
                                inf_verbs.append(inf_verb_ref)
                            continue

            if word[-3:] in ["ого", "его", "ому", "ыми", "его", "ему"]:
                ending = 3
            elif word[-2:] in ["ом", "ым", "ые", "ых", "ую", "ой", "им", "ем"]:
                ending = 2
            else:
                ending = 0
            if ending != 0:
                masc_adj_word = ''
                if word[-(ending+1):-ending] in VOICELESS:
                    masc_adj_word = word[:-ending] + "ий"
                elif masc_adj_word[-(ending+1):-ending] in VOICED:
                    masc_adj = word[:-ending] + "ый"

                if masc_adj_word != '' and masc_adj_word not in masc_adj:
                    flag = is_adj(word, words, ending)
                    if flag:
                        lex = Lexeme(lexeme=masc_adj_word, lemma=masc_adj_word, stem="___", tag="ADJ_MAS")
                        lexicon.append(lex)
                        masc_adj.append(masc_adj_word)
                        continue

            if word[-2:] in ['ий'] and word[-3:-2] in ["в", "н", "л", "т", "б"]:
                ending = "е"
            elif word[-2:] in ['ий'] and word[-3:-2] in ["д", "ф", "ц", "г", "м", "з",  "с"]:
                ending = "я"
            else:
                ending = ""
            if ending != "":
                flag = is_noun_2(word, words)
                if flag:
                    if ending == "е":
                        lex = Lexeme(lexeme=word[:-1]+ending, lemma=word[:-1]+ending, stem=word[:-2], tag="NOUN_NEU_2DEC")
                        lexicon.append(lex)
                    elif ending == "я":
                        lex = Lexeme(lexeme=word[:-1] + ending, lemma=word[:-1] + ending, stem=word[:-2],
                                     tag="NOUN_FEM_1DEC")
                        lexicon.append(lex)
                    continue
    return lexicon
