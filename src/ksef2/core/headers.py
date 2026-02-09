class KSeFHeaders:
    @staticmethod
    def session(token: str) -> dict[str, str]:
        return {"SessionToken": token}

    @staticmethod
    def bearer(token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}
