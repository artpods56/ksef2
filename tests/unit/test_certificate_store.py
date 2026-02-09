"""Tests for CertificateStore."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta

import pytest

from ksef2.core import exceptions
from ksef2.core.stores import CertificateStore
from ksef2.domain.models.encryption import CertUsage

from tests.unit.conftest import make_certificate


class TestLoad:
    def test_load_replaces_existing(self) -> None:
        store = CertificateStore()
        store.load([make_certificate()])
        store.load([make_certificate(), make_certificate()])

        assert len(store.all()) == 2

    def test_load_empty_clears(self) -> None:
        store = CertificateStore()
        store.load([make_certificate()])
        store.load([])

        assert store.all() == []


class TestAdd:
    def test_add_appends(self) -> None:
        store = CertificateStore()
        store.add(make_certificate())
        store.add(make_certificate())

        assert len(store.all()) == 2


class TestGetValid:
    def test_returns_matching_cert(self) -> None:
        store = CertificateStore()
        cert = make_certificate(usage=[CertUsage.SYMMETRIC_KEY_ENCRYPTION])
        store.load([cert])

        result = store.get_valid(CertUsage.SYMMETRIC_KEY_ENCRYPTION)

        assert result is not None
        assert result.certificate == cert.certificate

    def test_raises_when_no_matching_usage(self) -> None:
        store = CertificateStore()
        store.load([make_certificate(usage=[CertUsage.KSEF_TOKEN_ENCRYPTION])])

        with pytest.raises(exceptions.NoCertificateAvailableError):
            store.get_valid(CertUsage.SYMMETRIC_KEY_ENCRYPTION)

    def test_raises_when_cert_expired(self) -> None:
        now = datetime.now(tz=timezone.utc)
        store = CertificateStore()
        store.load(
            [
                make_certificate(
                    usage=[CertUsage.SYMMETRIC_KEY_ENCRYPTION],
                    valid_from=now - timedelta(days=60),
                    valid_to=now - timedelta(days=1),
                )
            ]
        )

        with pytest.raises(exceptions.NoCertificateAvailableError):
            store.get_valid(CertUsage.SYMMETRIC_KEY_ENCRYPTION)

    def test_raises_when_cert_not_yet_valid(self) -> None:
        now = datetime.now(tz=timezone.utc)
        store = CertificateStore()
        store.load(
            [
                make_certificate(
                    usage=[CertUsage.SYMMETRIC_KEY_ENCRYPTION],
                    valid_from=now + timedelta(days=1),
                    valid_to=now + timedelta(days=60),
                )
            ]
        )

        with pytest.raises(exceptions.NoCertificateAvailableError):
            store.get_valid(CertUsage.SYMMETRIC_KEY_ENCRYPTION)


class TestListValid:
    def test_filters_by_date(self) -> None:
        now = datetime.now(tz=timezone.utc)
        valid = make_certificate(
            valid_from=now - timedelta(days=10),
            valid_to=now + timedelta(days=10),
        )
        expired = make_certificate(
            valid_from=now - timedelta(days=60),
            valid_to=now - timedelta(days=1),
        )
        store = CertificateStore()
        store.load([valid, expired])

        result = store.list_valid()

        assert len(result) == 1
        assert result[0].certificate == valid.certificate

    def test_filters_at_custom_time(self) -> None:
        check_time = datetime(2025, 6, 1, tzinfo=timezone.utc)
        cert = make_certificate(
            valid_from=datetime(2025, 5, 1, tzinfo=timezone.utc),
            valid_to=datetime(2025, 7, 1, tzinfo=timezone.utc),
        )
        store = CertificateStore()
        store.load([cert])

        assert len(store.list_valid(at=check_time)) == 1

    def test_empty_when_all_expired(self) -> None:
        now = datetime.now(tz=timezone.utc)
        store = CertificateStore()
        store.load(
            [
                make_certificate(
                    valid_from=now - timedelta(days=60),
                    valid_to=now - timedelta(days=1),
                )
            ]
        )

        assert store.list_valid() == []


class TestByUsage:
    def test_filters_by_usage(self) -> None:
        sym = make_certificate(usage=[CertUsage.SYMMETRIC_KEY_ENCRYPTION])
        tok = make_certificate(usage=[CertUsage.KSEF_TOKEN_ENCRYPTION])
        store = CertificateStore()
        store.load([sym, tok])

        result = store.by_usage(CertUsage.SYMMETRIC_KEY_ENCRYPTION)

        assert len(result) == 1
        assert CertUsage.SYMMETRIC_KEY_ENCRYPTION in result[0].usage

    def test_cert_with_multiple_usages_matches_both(self) -> None:
        both = make_certificate(
            usage=[CertUsage.SYMMETRIC_KEY_ENCRYPTION, CertUsage.KSEF_TOKEN_ENCRYPTION],
        )
        store = CertificateStore()
        store.load([both])

        assert len(store.by_usage(CertUsage.SYMMETRIC_KEY_ENCRYPTION)) == 1
        assert len(store.by_usage(CertUsage.KSEF_TOKEN_ENCRYPTION)) == 1
