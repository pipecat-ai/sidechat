"""Vet Hugging Face datasets: licence, gating, size, card excerpt and one sample row.

usage: hf_vet.py OUT_JSON README_CHARS ROW_CHARS ID [ID ...]
An ID prefixed with '?' is looked up by name first. Anonymous calls only.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def fetch(url, as_json=True, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "dataset-survey/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read()
            return json.loads(data) if as_json else data.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(8 * (i + 1))
                continue
            return {"_error": f"HTTP {e.code}"} if as_json else f"[HTTP {e.code}]"
        except Exception as e:  # noqa: BLE001
            return {"_error": str(e)[:80]} if as_json else f"[{str(e)[:80]}]"
    return {"_error": "rate limited"} if as_json else "[rate limited]"


def clean_card(text):
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)       # YAML front matter
    text = re.sub(r"<[^>]+>", " ", text)                            # html
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)               # images
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)            # links
    text = re.sub(r"[#*`|>]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def short(v, n):
    s = json.dumps(v, ensure_ascii=False, default=str)
    return s if len(s) <= n else s[: n - 3] + "..."


def tagv(tags, p):
    return ",".join(t.split(":", 1)[1] for t in tags if t.startswith(p + ":")) or "-"


def main():
    out_path, readme_chars, row_chars = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    results = []
    for raw in sys.argv[4:]:
        ds = raw
        if raw.startswith("?"):
            hits = fetch("https://huggingface.co/api/datasets?search=" + urllib.parse.quote(raw[1:]) + "&sort=downloads&direction=-1&limit=3")
            if not isinstance(hits, list) or not hits:
                print(f"\n### {raw}: not found by name")
                continue
            ds = hits[0]["id"]
        info = fetch("https://huggingface.co/api/datasets/" + ds)
        if "_error" in info:
            print(f"\n### {ds}: {info['_error']}")
            continue
        tags = info.get("tags", [])
        card = clean_card(fetch(f"https://huggingface.co/datasets/{ds}/raw/main/README.md", as_json=False))
        files = [s["rfilename"] for s in info.get("siblings", [])]
        size = fetch("https://datasets-server.huggingface.co/size?dataset=" + urllib.parse.quote(ds, safe=""))
        nrows = (size.get("size", {}).get("dataset", {}) or {}).get("num_rows") if "_error" not in size else None
        sample, feats = None, None
        splits = fetch("https://datasets-server.huggingface.co/splits?dataset=" + urllib.parse.quote(ds, safe=""))
        if "_error" not in splits and splits.get("splits"):
            s0 = splits["splits"][0]
            fr = fetch("https://datasets-server.huggingface.co/first-rows?dataset=" + urllib.parse.quote(ds, safe="")
                       + "&config=" + urllib.parse.quote(s0["config"]) + "&split=" + urllib.parse.quote(s0["split"]))
            if "_error" not in fr and fr.get("rows"):
                feats = [f["name"] for f in fr.get("features", [])]
                sample = fr["rows"][0]["row"]
        rec = {"id": ds, "license": tagv(tags, "license"), "gated": info.get("gated"), "downloads": info.get("downloads"),
               "likes": info.get("likes"), "modified": (info.get("lastModified") or "")[:10], "lang": tagv(tags, "language"),
               "rows": nrows, "n_files": len(files), "features": feats, "card": card[:4000], "sample": sample}
        results.append(rec)
        print(f"\n### {ds}  lic={rec['license']} gated={rec['gated']} rows={nrows} dl={rec['downloads']} likes={rec['likes']} upd={rec['modified']} lang={rec['lang'][:20]} files={len(files)}")
        print("card:", card[:readme_chars] or "(no card)")
        if feats:
            print("cols:", ", ".join(feats)[:300])
        if sample is not None:
            print("row :", short(sample, row_chars))
        time.sleep(0.6)
    json.dump(results, open(out_path, "w"))


if __name__ == "__main__":
    main()
