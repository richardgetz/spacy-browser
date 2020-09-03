
#
# TEST = """Facebook CEO Mark Zuckerburg, owner of the popular website myspace.com, emailed from mark@facebook.com to give me his phone number +15717890987, but also noted his secrtary's number is 398-498-4847.
# This was quite unexpected since just last Wednesday Mark noted Sheila was not interested in meeting us for lunch. I will email Mark back from jeffrey@will.go.com.
# He also sent me a the links for our dashboard https://dfsfsfsff.ru/dashboard/overview:4040. He said there was something fishy going on.
# It had the normal IP he was used to 192.156.3.345, but the ipv6 was completely off (2001:0db8:85a3:0000:0000:8a2e:0370:7334). This is something we need to look into.
# Oh, also. Steve mentioned in may be in Germany this week. He plans to travel back to the US in a few days.
# The IMSI: 334384724034918 and IMEI: 572393739374467, are linked to xxxxx.
# """
#
#
# def get_doc(text, pattern_help=True):
#     nlp = spacy.load("en_core_web_md")
#     if pattern_help:
#         ruler = EntityRuler(nlp)
#         with open("configs/custom_patterns.json", 'r') as f:
#             PATTERNS = json.load(f)
#         # phone regex is overlapping too much. need to find a better way without messing up others
#         # "^\\+?\\(?0{0,2}((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|9[0-58]|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\\W*\\d){0,13}\\d$"
#         for l in PATTERNS:
#             nlp.vocab.strings.add(l["label"])
#         ruler.add_patterns(PATTERNS)
#         nlp.add_pipe(ruler, before='ner')
#     return nlp(text)


def fix_imsi_imei(end, json_doc):
    new_start = None
    for token in json_doc['tokens']:
        if token["end"] == end:
            if token["pos"] == "NUM":
                return token["start"]
                break
            else:
                return None
