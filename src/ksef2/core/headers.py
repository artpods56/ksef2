class KSeFHeaders:
    @staticmethod
    def session(
        token: str,
    ) -> dict[str, str]:  # TODO: remove, unused — API uses bearer auth
        return {"SessionToken": token}

    @staticmethod
    def bearer(token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}
