
import spacy
import json
import time
from spacy.pipeline import EntityRuler
from custom_pattern_override import fix_imsi_imei
TEST = """Facebook CEO Mark Zuckerburg, owner of the popular website myspace.com, emailed from mark@facebook.com to give me his phone number +15717890987, but also noted his secrtary's number is 398-498-4847.
This was quite unexpected since just last Wednesday Mark noted Sheila was not interested in meeting us for lunch. I will email Mark back from jeffrey@will.go.com.
He also sent me a the links for our dashboard https://dfsfsfsff.ru/dashboard/overview:4040. He said there was something fishy going on.
It had the normal IP he was used to 192.156.3.345, but the ipv6 was completely off (2001:0db8:85a3:0000:0000:8a2e:0370:7334). This is something we need to look into.
Oh, also. Steve mentioned in may be in Germany this week. He plans to travel back to the US in a few days.
The phone number is zzzzzzzzzzzz, the imsi is 334384724034918, and the imei is 572393739374467.
"""


def document_to_dict(raw_text=TEST, pattern_help=True):
    nlp = spacy.load("en_core_web_md")
    if pattern_help:
        ruler = EntityRuler(nlp, overwrite_ents=True)
        # matcher = Matcher(nlp.vocab)

        # it may need to get more compliated than this

        with open("configs/custom_patterns.json", 'r') as f:
            PATTERNS = json.load(f)
        # "^\\+?\\(?0{0,2}((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|9[0-58]|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\\W*\\d){0,13}\\d$"
        for l in PATTERNS:
            nlp.vocab.strings.add(l["label"])
        ruler.add_patterns(PATTERNS)
        nlp.add_pipe(ruler, before='ner')
    doc = nlp(raw_text)
    json_doc = doc.to_json()
    with open("spacy_json_example.json", "w") as f:
        json.dump(json_doc, f, indent=4)
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
        if ents["label"] == "IMEI" or ents["label"] == "IMSI":
            new_start = fix_imsi_imei(ents["end"], json_doc)
            if new_start:
                if DATASET["spans"].get(ents["label"]):
                    DATASET["spans"][ents["label"]].append(
                        str(new_start) + ":" + str(ents["end"]))
                else:
                    DATASET["spans"][ents["label"]] = [
                        str(new_start) + ":" + str(ents["end"])]
                continue

        if DATASET["spans"].get(ents["label"]):
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
