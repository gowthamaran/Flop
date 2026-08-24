from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import technocore_agent as agent


class EncodingTests(unittest.TestCase):
    def test_base58_round_trip_preserves_leading_zeroes(self) -> None:
        original = b"\x00\x00\x01\xff\x10"
        self.assertEqual(agent.base58btc_decode(agent.base58btc_encode(original)), original)

    def test_generated_did_is_canonical_and_verifiable(self) -> None:
        private_key = Ed25519PrivateKey.generate()
        did = agent.did_from_private_key(private_key)
        self.assertTrue(did.startswith("did:key:z6Mk"))
        payload = b"technocore-test"
        signature = agent.sign_bytes(private_key, payload)
        agent.verify_bytes(did, signature, payload)

    def test_message_normalization_matches_signed_payload(self) -> None:
        normalized, payload = agent.message_payload("lobby", 123, "  hello\nworld  ")
        self.assertEqual(normalized, "hello world")
        self.assertEqual(payload, b"lobby|123|hello world")

    def test_invalid_room_is_rejected(self) -> None:
        with self.assertRaises(agent.ProtocolError):
            agent.validate_name("../private")


class IdentityTests(unittest.TestCase):
    def test_encrypted_identity_round_trip_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "identity.pem"
            passphrase = "correct horse battery staple"
            did = agent.create_identity(path, passphrase)
            loaded = agent.load_identity(
                path, passphrase=passphrase.encode("utf-8"), allow_prompt=False
            )
            self.assertEqual(agent.did_from_private_key(loaded), did)
            with self.assertRaises(agent.IdentityError):
                agent.create_identity(path, passphrase)
            if os.name != "nt":
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)


class ProofTests(unittest.TestCase):
    def test_contribution_proof_verifies_and_tampering_fails(self) -> None:
        private_key = Ed25519PrivateKey.generate()
        proof = agent.create_contribution_proof(
            private_key,
            "https://github.com/gowthamaran/Flop",
            "a" * 40,
        )
        agent.verify_contribution_proof(proof)
        proof["commit"] = "b" * 40
        with self.assertRaises(agent.IdentityError):
            agent.verify_contribution_proof(proof)


class DoctorTests(unittest.TestCase):
    def test_doctor_is_machine_readable_and_offline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing_key = Path(directory) / "identity.pem"
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = agent.main(["doctor", "--key", str(missing_key)])
            report = json.loads(output.getvalue())
            self.assertEqual(status, 0)
            self.assertTrue(report["python_supported"])
            self.assertFalse(report["identity_exists"])
            self.assertTrue(report["ready_for_init"])


if __name__ == "__main__":
    unittest.main()
