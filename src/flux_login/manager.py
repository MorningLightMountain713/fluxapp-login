import hashlib
from secrets import token_bytes
from urllib.parse import urlencode

from bitcoin.core.key import CPubKey
from bitcoin.signmessage import BitcoinMessage, SignMessage
from bitcoin.wallet import (
    CBitcoinSecret,
    CBitcoinSecretError,
    P2PKHBitcoinAddress,
)
from rich.pretty import pprint
from yarl import URL

from .http_helper import do_http


class PrivateKeyError(Exception): ...


class FluxAppManager:
    base_url = URL("https://api.runonflux.io")

    @staticmethod
    def generate_key_hex() -> str:
        digest = hashlib.sha256(token_bytes(64)).hexdigest()

        return digest

    @staticmethod
    def generate_key() -> CBitcoinSecret:
        h = hashlib.sha256(token_bytes(64)).digest()
        pkey = CBitcoinSecret.from_secret_bytes(h)

        return pkey

    @staticmethod
    def key_from_hex(private_hex: str) -> CBitcoinSecret:
        private_bytes = bytes.fromhex(private_hex)

        try:
            private_key = CBitcoinSecret.from_secret_bytes(private_bytes)
        except CBitcoinSecretError:
            raise PrivateKeyError("Unable to convert hex to key") from None

        return private_key

    @staticmethod
    async def get_login_phrase() -> str | None:
        url = FluxAppManager.base_url / "id/loginphrase"
        res: dict[str, str] | None = await do_http(url)

        if not res:
            return None

        if res.get("status") != "success":
            return None

        phrase: str | None = res.get("data")

        return phrase

    @property
    def public_key(self) -> CPubKey:
        return self.private_key.pub

    @property
    def address(self) -> P2PKHBitcoinAddress:
        return P2PKHBitcoinAddress.from_pubkey(self.public_key)

    @property
    def auth_payload(self) -> dict[str, str]:
        msg = {
            "zelid": str(self.address),
            "signature": self.signature or "",
            "loginPhrase": self.login_phrase or "",
        }

        return msg

    @property
    def auth_header(self) -> dict[str, str]:
        return {"zelidauth": urlencode(self.auth_payload)}

    def __init__(
        self,
        private_hex: str | None = None,
    ) -> None:
        self.private_key: CBitcoinSecret = (
            self.key_from_hex(private_hex)
            if private_hex
            else self.generate_key()
        )

        self.login_phrase: str | None = None
        self.signature: str | None = None

    def sign_message(self, msg: str) -> bytes:
        message = BitcoinMessage(msg)
        signed = SignMessage(self.private_key, message)

        return signed

    async def sign_loginphrase(self) -> bool:
        self.login_phrase = await self.get_login_phrase()

        if not self.login_phrase:
            return False

        signed = self.sign_message(self.login_phrase)

        self.signature = signed.decode("utf-8")

        return True

    async def login(self, force: bool = False) -> None:
        if force or not self.signature:
            await self.sign_loginphrase()

        url = FluxAppManager.base_url / "id/verifylogin"

        res = await do_http(url, "post", data=self.auth_payload)

        print("Login Response:\n")
        pprint(res)
        print("\nAuth header for future api calls:\n")
        pprint(self.auth_header)
