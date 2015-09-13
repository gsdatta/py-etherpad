from etherpadlite.client import EtherpadClient, clean_url
import pytest


def test_url_cleaner():
    assert clean_url("http://google.com/") == "http://google.com"
    assert clean_url("http://google.com") == "http://google.com"


def test_groups(client):
    group_without_id = client.create_group()
    group_with_id = client.create_group(group_id=1)

    groups = client.list_groups()
    assert group_without_id in groups
    assert group_with_id in groups

    for group in groups:
        client.delete_group(group)

    groups = client.list_groups()
    assert group_without_id not in groups
    assert group_with_id not in groups


def test_authors(client):
    author_without_id = client.create_author(name='TESTER')
    author_with_id = client.create_author(name='TESTER', author_id=1)

    assert client.get_author_name(author_without_id) == 'TESTER'
    assert client.get_author_name(author_with_id) == 'TESTER'


def test_sessions(client):
    author = client.create_author(name='EtherpadLite Test User')
    group = client.create_group()
    import time
    valid = int(time.time()) + 200
    session = client.create_session(author_id=author, group_id=group, valid_until=valid)

    session_info = client.get_session_details(session)
    assert session_info['groupID'] == group
    assert session_info['authorID'] == author
    assert session_info['validUntil'] == valid

    with pytest.raises(ValueError):
        sessions = client.list_sessions()

    sessions = client.list_sessions(group_id=group)
    assert session in sessions

    sessions = client.list_sessions(author_id=author)
    assert session in sessions

    sessions = client.list_sessions(author_id=author, group_id=group)
    assert session in sessions

    client.delete_session(session_id=session)

    sessions = client.list_sessions(author_id=author, group_id=group)
    assert session not in sessions


def test_exceptions(client):
    from etherpadlite.client import EtherpadParamsException, EtherpadException

    with pytest.raises(EtherpadException):
        client.send_request(function='someFakeFunction')

    with pytest.raises(EtherpadParamsException):
        client.send_request(function='deleteGroup')


def test_pads(client):
    try:
        client.delete_pad(pad_id='ETHERPADLITE-PY-TEST')
    except Exception:
        pass

    pad = client.create_pad(pad='ETHERPADLITE-PY-TEST', text='TESTING')
    assert pad.id in client.list_pads()

    assert pad.id == 'ETHERPADLITE-PY-TEST'
    assert pad.text.strip() == 'TESTING'
    assert pad.revisions_count == 0

    pad.text = 'TESTING REVISED'
    assert pad.text.strip() == 'TESTING REVISED'
    assert pad.revisions_count == 1

    pad.save_revision(revision=1)
    assert pad.saved_revisions_count == 1
    assert 1 in pad.saved_revisions

    assert pad.users_count == 0
