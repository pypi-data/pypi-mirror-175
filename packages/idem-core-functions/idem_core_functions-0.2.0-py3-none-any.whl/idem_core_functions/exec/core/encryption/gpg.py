"""Core function to encrypt and decrypt message with gpg"""
from typing import Any
from typing import Dict
from typing import List
from typing import Union

import gnupg

__contracts__ = ["soft_fail"]


async def encrypt(
    hub,
    data: str,
    recipients: List[str] = [],
    sign: str = None,
    always_trust: bool = False,
    passphrase: str = None,
    armor: bool = True,
    output: str = None,
    symmetric: Union[bool, str] = False,
    extra_args: List[str] = None,
) -> Dict[str, Any]:
    """
    Encrypt the message contained in the string 'data'.

    Args:
        data(str):
            The data or message that needs to be encrypted.
        recipients(list[str], Optional):
            A list of key fingerprints for recipients.
        sign(str, Optional):
            Either the Boolean value True, or the fingerprint of a key which is used to sign the encrypted data.
        always_trust(bool, Optional):
            Skip key validation and assume that used keys are always fully trusted.
        passphrase(str, Optional):
            A passphrase to use when accessing the keyrings.
        armor(bool, Optional):
            Whether to use ASCII armor. If False, binary data is produced.
        output(str, Optional):
            The name of an output file to write to.
        symmetric(Union[bool, str], Optional):
            If specified, symmetric encryption is used. In this case, specify recipients as None.
            If True is specified, then the default cipher algorithm (CAST5) is used.
            The cipher-algorithm to use (for example, 'AES256') can also be specified.
        extra_args(list[str], Optional):
            A list of additional arguments to pass to the gpg executable.
            For example, Pass extra_args=['-z', '0'] to disable compression
    """
    result = dict(comment=[], ret=None, result=True)
    if not data:
        result["result"] = False
        result["comment"].append("data for gpg_encrypt is empty")
        return result

    try:
        gpg = gnupg.GPG()
        response = gpg.encrypt(
            data=data,
            recipients=recipients,
            sign=sign,
            always_trust=always_trust,
            passphrase=passphrase,
            armor=armor,
            output=output,
            symmetric=symmetric,
            extra_args=extra_args,
        )

        if not response.ok:
            result["result"] = False
            result["comment"].append(response.status)
            return result

        result["comment"].append(response.status)
        # decode is to remove b' prefix
        result["ret"] = {"data": str(response.data.decode("utf-8"))}
    except Exception as e:
        result["result"] = False
        hub.log.debug(f"gpg_encrypt failed {e}")
        result["comment"] = (f"{e.__class__.__name__}: {e}",)

    return result


async def decrypt(
    hub,
    message: str,
    always_trust: bool = False,
    passphrase: str = None,
    output: str = None,
    extra_args: List[str] = None,
) -> Dict[str, Any]:
    """
    Decrypt the message.

    Args:
        message(str):
            The encrypted message.
        always_trust(bool, Optional):
            Skip key validation and assume that used keys are always fully trusted.
        passphrase(str, Optional):
            A passphrase to use when accessing the keyrings.
        output(str, Optional):
            The name of an output file to write to.
        extra_args(list[str], Optional):
            A list of additional arguments to pass to the gpg executable.
    """
    result = dict(comment=[], ret=None, result=True)
    if not message:
        result["result"] = False
        result["comment"].append("message for gpg_decrypt is empty")
        return result

    try:
        gpg = gnupg.GPG()
        response = gpg.decrypt(
            message=message,
            always_trust=always_trust,
            passphrase=passphrase,
            output=output,
            extra_args=extra_args,
        )

        if not response.ok:
            result["result"] = False
            result["comment"].append(response.status)
            return result

        result["comment"].append(response.status)
        # decode is to remove b' prefix
        result["ret"] = {"data": str(response.data.decode("utf-8"))}
    except Exception as e:
        result["result"] = False
        hub.log.debug(f"gpg_decrypt failed {e}")
        result["comment"] = (f"{e.__class__.__name__}: {e}",)

    return result
