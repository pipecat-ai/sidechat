"""Search the Hugging Face Hub for datasets by many terms and aggregate the hits.

usage: hf_search.py OUT_JSON
Anonymous API calls only; no token and no user details are sent.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

TERMS = [
    # the task itself
    "addressee", "addressee detection", "addressee recognition", "multi-party", "multiparty",
    "multi party dialogue", "multi-user", "group chat", "group conversation", "turn-taking",
    "turn taking", "next speaker", "when to speak", "when to respond", "proactive dialogue",
    "device-directed", "device directed", "wake word", "barge-in", "backchannel", "interruption",
    "overhearing", "bystander", "side conversation", "human-robot", "multi-party human robot",
    # meetings and real multi-speaker talk
    "ami", "ami meeting", "icsi", "meeting transcripts", "meeting", "qmsum", "meetingbank", "elitr",
    "notsofar", "alimeeting", "aishell-4", "chime", "dipco", "dinner party", "voxconverse",
    "santa barbara", "sbcsae", "candor", "callhome", "callfriend", "fisher", "switchboard", "mrda",
    "talkbank", "earnings call", "earnings22", "podcast transcripts", "interview transcripts",
    "mediasum", "debate", "supreme court", "oyez", "parliament", "hansard", "city council",
    "diarization", "diarized", "speaker-attributed",
    # TV / chat / games with several speakers
    "meld", "emorynlp", "friends", "friendsqa", "friends-mmc", "tv show dialogue", "movie dialogue",
    "molweni", "ubuntu irc", "ubuntu dialogue", "irc", "discord", "slack", "telegram", "reddit conversation",
    "wikiconv", "convokit", "mpdd", "mpchat", "cped", "m3ed", "samsum", "dialogsum", "soda",
    "crd3", "critical role", "dungeons and dragons", "tabletop", "werewolf", "mafia", "avalon",
    "diplomacy", "among us", "roleplay group",
    # things people say to assistants (single user)
    "voice assistant", "smart speaker", "slurp", "massive", "snips", "clinc", "hwu64", "taskmaster",
    "schema guided", "multiwoz", "multi-user multiwoz", "in-car assistant", "kvret", "alexa",
    "fluent speech commands", "spoken language understanding",
    # dialogue acts / discourse that carry addressee links
    "dialogue act", "discourse parsing", "reply-to", "thread disentanglement", "conversation disentanglement",
    "response selection", "speaker identification",
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dataset-survey/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    out = sys.argv[1]
    hits = {}
    for i, term in enumerate(TERMS):
        url = ("https://huggingface.co/api/datasets?search=" + urllib.parse.quote(term)
               + "&sort=downloads&direction=-1&limit=40&full=true")
        try:
            rows = get(url)
        except Exception as e:  # noqa: BLE001
            print(f"!! {term}: {e}", file=sys.stderr)
            time.sleep(3)
            continue
        for d in rows:
            h = hits.setdefault(d["id"], {
                "id": d["id"], "downloads": d.get("downloads", 0), "likes": d.get("likes", 0),
                "lastModified": (d.get("lastModified") or "")[:10], "gated": d.get("gated"),
                "tags": d.get("tags", []), "terms": [],
            })
            h["terms"].append(term)
        print(f"{i + 1}/{len(TERMS)} {term}: {len(rows)}", file=sys.stderr)
        time.sleep(0.4)
    json.dump(list(hits.values()), open(out, "w"))
    print(f"{len(hits)} unique datasets from {len(TERMS)} terms")


if __name__ == "__main__":
    main()
