
import spacy
import json
import time
from spacy.pipeline import EntityRuler
TEST = """

Facebook CEO Mark Zuckerburg, owner of the popular website myspace.com, emailed from mark@facebook.com to give me his phone number +15717890987.
This was quite unexpected since just last Wednesday Mark noted Sheila was not interested in meeting us for lunch. I will email Mark back from jeffrey@will.go.com.

"""


def document_to_dict(raw_text=TEST, pattern_help=True):
    nlp = spacy.load("en_core_web_sm")
    if pattern_help:
        ruler = EntityRuler(nlp)
        # matcher = Matcher(nlp.vocab)
        phone_reg = r"^\+?\(?0{0,2}((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|9[0-58]|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\W*\d){0,13}\d$"
        email_reg = r"((?:[A-z0-9\.\-\_\$\!\?]\w+){1,5}\@(?:[A-z0-9\.\-\_\$\!\?]\w+){1,5})"
        ipv4_reg = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        domain_reg = r"^(https?:\/\/)?([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.?){1,20}\.[a-zA-Z]{2,}$"
        # it may need to get more compliated than this
        easy_url_reg = r"(https?:\/\/).*?\s"
        # PATTERNS = [
        #     {"label": "PHONE", "pattern": [{"TEXT": {"REGEX": phone_reg}}]},
        #     {"label": "EMAIL", "pattern": [{"TEXT": {"REGEX": email_reg}}]},
        #     {"label": "IPV4", "pattern": [{"TEXT": {"REGEX": ipv4_reg}}]},
        #     {"label": "DOMAIN", "pattern": [{"TEXT": {"REGEX": domain_reg}}]}
        # ]
        with open("")
        for l in PATTERNS:
            nlp.vocab.strings.add(l["label"])
        ruler.add_patterns(PATTERNS)
        nlp.add_pipe(ruler, before='ner')
    doc = nlp(raw_text)
    json_doc = doc.to_json()

    DATASET = {"text": [], "spans": {}, "deps": {}}
    for token in json_doc["tokens"]:
        DATASET["text"].append({"id": int(token["start"]), "word": json_doc["text"][int(token["start"]):int(
            token["end"])], "start": token["start"], "end": token["end"]})
        try:
            if token["dep"] != "":
                if token["dep"] in DATASET["deps"].keys():
                    DATASET["deps"][token["dep"]].append(
                        str(token["start"]) + ":" + str(token["end"]))
                else:
                    DATASET["deps"][token["dep"]] = [
                        str(token["start"]) + ":" + str(token["end"])]
        except:
            pass

    for ents in json_doc["ents"]:
        if ents["label"] in DATASET["spans"].keys():
            DATASET["spans"][ents["label"]].append(
                str(ents["start"]) + ":" + str(ents["end"]))
        else:
            DATASET["spans"][ents["label"]] = [
                str(ents["start"]) + ":" + str(ents["end"])]
    return DATASET
    # for sent in json_doc["sents"]:
    # sent_dict = {"uuid": uuid}
    # start = sent["start"]
    # end = sent["end"]
    #
    # sent_list = []
    # for token in json_doc["tokens"]:
    #     if token["end"] > end:
    #         break
    #     elif token["start"] >= start:
    #         sent_list.append(
    #             {'id': i, 'word': json_doc["text"][token["start"]:token["end"]]})
    #         i += 1
    #
    # spans = {}
    # for ents in json_doc["ents"]:
    #     if ents["end"] > end:
    #         break
    #     elif ents["start"] >= start:
    #         if ents["label"] in spans.keys():
    #             spans[ents["label"]].append(
    #                 str(ents["start"] - start) + ":" + str(ents["end"] - start))
    #         else:
    #             spans.update(
    #                 {ents["label"]: [str(ents["start"] - start) + ":" + str(ents["end"] - start)]})
    #     deps = {}
    #     for token in json_doc["tokens"]:
    #         if token["end"] > end:
    #             break
    #         elif token["start"] >= start:
    #             if token["dep"] in deps.keys():
    #                 deps[token["dep"]].append(
    #                     str(token["start"] - start) + ":" + str(token["end"] - start))
    #             else:
    #                 deps.update(
    #                     {token["dep"]: [str(token["start"] - start) + ":" + str(token["end"] - start)]})
    # sent_dict.update(
    #     {"sentence": sent_list, "spans": spans, "deps": deps})
    # DATASET.append(sent_dict)
    # uuid += 1
    # print(DATASET)


def convert_to_training(tags):
    print()
