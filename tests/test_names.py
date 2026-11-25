"""Other spellings of the agent's name, added as aliases at runtime."""

from __future__ import annotations

from sidechat.names import variants, with_variants
from sidechat.schema import Agent, SidechatRequest
from sidechat.train import features


def test_spellings_of_the_final_sound_and_doubled_letters():
    v = variants("Olly")
    assert {"Oli", "Ollie", "Olli", "Oly"} <= set(v) and "Olly" not in v and len(v) <= 8
    assert "Remmy" in variants("Remy") and "Alfie" in variants("alfi") and "Novah" in variants("Nova")


def test_no_lower_case_name_and_nothing_for_short_or_odd_names():
    assert all(x[0].isupper() for x in variants("Penny")) and "penny" not in [x.lower() for x in variants("Penny")]
    assert variants("Max") == [] and variants("Al") == [] and variants("the assistant") == []


def test_aliases_kept_first_and_not_repeated():
    req = SidechatRequest(agent=Agent(name="Olly", aliases=["Oli", "holly"]), text="x")
    got = with_variants(req).agent.aliases
    assert got[:2] == ["Oli", "holly"] and got.count("Oli") == 1 and "Ollie" in got


def test_a_misheard_name_now_counts_as_calling_the_agent():
    req = SidechatRequest(agent=Agent(name="Olly"), text="Oli, what's the weather tomorrow?")
    assert features._calls(req.text, req) == (False, False, False)
    assert features._calls(req.text, with_variants(req))[:2] == (True, True)
