import hypothesis.strategies as st
from hypothesis import given


def valid_match_history_links():
    return st.from_regex(r'.*(ESPORTSTMNT).*(\?).*')


def invalid_match_historoy_links_sports():
    return st.from_regex(r'.*(?!ESPORTSTMNT).*(\?).*')


def invalid_match_historoy_links_q():
    return st.from_regex(r'.*(ESPORTSTMNT).*(?!\?).*')
